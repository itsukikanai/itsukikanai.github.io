import os
import json
from google import genai
from dotenv import load_dotenv
from app.core import database
from app.core import utils

load_dotenv()

def get_gemini_client():
    api_key = os.getenv("API_KEY_GEMINI")
    if not api_key:
        raise ValueError("API_KEY_GEMINI not found in .env")
    
    return genai.Client(api_key=api_key)

def get_model_name():
    config = utils.load_config()
    return config.get("model_gemini", "gemini-2.0-flash-exp")

def analyze_video(video_db_id: int, progress=None):
    """
    Analyze video transcript using Gemini.
    Generates tags, summary, and highlights.
    Updates DB with tags and analysis result.
    """
    
    # 1. Fetch Transcript
    if progress: progress(0.1, desc="Fetching transcript...")
    subtitles = database.get_subtitles(video_db_id)
    if not subtitles:
        raise ValueError("No subtitles found for this video. Please transcribe first.")
    
    # Construct Transcript Text
    transcript_text = ""
    for s in subtitles:
        # Optimization: Use simple integer seconds and minimal separators.
        # Format: "START:Text" (e.g. "12:Hello world")
        start_sec = int(s['start_time'])
        transcript_text += f"{start_sec}:{s['text']}\n"
        
    # 2. Call AI
    if progress: progress(0.3, desc="Calling Gemini API...")
    
    # Get duration to calculate target highlights
    video = database.get_video_by_id(video_db_id)
    duration_min = video.get('duration', 0) / 60.0 if video.get('duration') else 0
    
    # Target: 1 highlight per 10 minutes, min 3
    target_count = max(3, int(duration_min / 10))
    
    existing_tags = database.get_all_tags()
    existing_tags_str = ", ".join(existing_tags)
    
    # Load Comments/Chat Context
    comments_context = ""
    # Usually we save it in the same directory as the video file
    video_path = video.get('file_path')
    if video_path:
        video_dir = os.path.dirname(video_path)
        comments_file = os.path.join(video_dir, "comments.json")
        if os.path.exists(comments_file):
            try:
                with open(comments_file, 'r', encoding='utf-8') as f:
                    comments_data = json.load(f)
                    
                # Summarize comments for context
                # E.g. "Here are some top comments/live chat messages for context:"
                # Just take a random sample or first 50 to avoid token overflow
                sample_comments = [c.get('message', '') for c in comments_data[:50] if c.get('message')]
                comments_text = "\n".join(sample_comments)
                if comments_text:
                    comments_context = f"Relevant Viewer Comments/Chat:\n{comments_text}\n"
            except Exception as e:
                print(f"Failed to load comments: {e}")

    prompt = f"""
    Analyze the transcript and comments (if any) to provide:
    1. 5 relevant tags (Japanese/English). PRIORITIZE EXISTING: [{existing_tags_str}].
    2. Concise Japanese summary.
    3. List of {target_count} highlights (approx 3 min each).
       - 'description': Japanese.
       - 'start_time' < 'end_time' (seconds).
    
    {comments_context}

    Return strictly JSON:
    {{
      "tags": ["..."],
      "summary": "...",
      "highlights": [
        {{"start_time": 100.0, "end_time": 280.0, "score": 90, "description": "..."}},
        ...
      ]
    }}
    
    Transcript (Format: Seconds:Text):
    """
    
    try:
        client = get_gemini_client()
        model_name = get_model_name()
        
        response = client.models.generate_content(
            model=model_name,
            contents=[prompt, transcript_text]
        )
        response_text = response.text.strip()
        
        # Strip markdown if present
        if response_text.startswith("```"):
            response_text = response_text.strip("`")
            if response_text.startswith("json"):
                response_text = response_text[4:]
        
        response_text = response_text.strip()
        
        result = json.loads(response_text)
        
        # Post-process highlights
        valid_highlights = []
        if 'highlights' in result:
            for h in result['highlights']:
                s = float(h.get('start_time', 0))
                e = float(h.get('end_time', 0))
                
                # Fix inverted times
                if s > e:
                    s, e = e, s
                
                # Filter very short clips (less than 3 seconds), arguably 5s
                # User complained about < 1s clips.
                # If it is < 3s, it's likely noise or error, reject it or pad it?
                # Let's reject clips smaller than 2 seconds, and for 2-5s maybe pad?
                # For now, simplistic filter: MUST be > 3s.
                if (e - s) < 3.0:
                    continue
                
                h['start_time'] = s
                h['end_time'] = e
                valid_highlights.append(h)
        
        result['highlights'] = valid_highlights
        
    except Exception as e:
        raise RuntimeError(f"AI Analysis Failed: {e}")
        
    # 3. Save Tags
    if progress: progress(0.8, desc="Saving results...")
    
    tags = result.get("tags", [])
    if tags:
        database.add_tags(video_db_id, tags)
        
    # 4. Save Analysis JSON
    # We might want to save summary/highlights in a structured way, but JSON column is flexible.
    analysis_json_str = json.dumps(result, ensure_ascii=False)
    database.update_video_analysis(video_db_id, analysis_json_str)
    
    # Save to file in video directory
    try:
        if video.get('file_path'):
            video_dir = os.path.dirname(video['file_path'])
            if os.path.exists(video_dir):
                analysis_path = os.path.join(video_dir, "analysis.json")
                with open(analysis_path, "w", encoding="utf-8") as f:
                    # Write formatted JSON
                    json.dump(result, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Failed to save analysis file: {e}")
    
    if progress: progress(1.0, desc="Analysis Complete.")
    
    return result
