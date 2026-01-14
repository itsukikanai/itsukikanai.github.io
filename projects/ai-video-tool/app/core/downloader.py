import os
import yt_dlp
from app.core import database
from app.core import utils

def download_video(url: str, format_mode: str = 'video', resolution: str = 'best', progress=None):
    """
    Download video using yt_dlp.
    format_mode: 'video' or 'audio'
    resolution: 'best', '1080p', '720p', '480p'
    """
    
    # Base options
    ydl_opts = {
        'outtmpl': '%(id)s.%(ext)s', 
        'quiet': True,
        'no_warnings': True,
        'writethumbnail': True,
        # Subtitle Options
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['ja', 'en'], # Prioritize Japanese
        'subtitlesformat': 'vtt', # Download as VTT for easier parsing
        # Do not fail if subtitles (or other formats) are missing/error 429
        'ignoreerrors': True,
    }
    
    # Configure Format
    if format_mode == 'audio':
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    else:
        # Video
        if resolution == 'best':
            ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        else:
            # parsing '1080p' -> 1080
            try:
                height = int(resolution.replace('p', ''))
                # Format selector for specific height, fallback to best if not available is tricky in one line string
                # bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]
                ydl_opts['format'] = f'bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/best[height<={height}][ext=mp4]/best'
            except:
                ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'


    # Hook for progress
    def progress_hook(d):
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%').replace('%','')
            try:
                val = float(p) / 100.0
                if progress:
                    progress(val, desc=f"Downloading: {d.get('_percent_str')}")
            except:
                pass
        elif d['status'] == 'finished':
            if progress:
                progress(1.0, desc="Download complete, processing...")

    ydl_opts['progress_hooks'] = [progress_hook]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 1. Extract Info
            info = ydl.extract_info(url, download=False)
            
            domain = utils.sanitize_filename(info.get('webpage_url_domain', 'unknown'))
            channel_id = utils.sanitize_filename(info.get('channel_id', info.get('uploader_id', 'unknown')))
            video_id = info.get('id')
            title = info.get('title')
            duration = info.get('duration')
            
            # Defines paths
            base_dir = utils.get_base_download_path()
            save_dir = os.path.join(base_dir, domain, channel_id, video_id)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            ydl_opts['outtmpl'] = os.path.join(save_dir, f"{video_id}.%(ext)s")
            
    except Exception as e:
        raise Exception(f"Failed to fetch info: {e}")

    # Re-instantiate with correct path
    ydl_opts['outtmpl'] = os.path.join(save_dir, f"{video_id}.%(ext)s")
    
    # Ensure merge to mp4 for better compatibility with browser
    ydl_opts['merge_output_format'] = 'mp4'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        if progress: progress(0, desc="Starting download...")
        ydl.download([url])
        
    # Check what file was created.
    expected_path = os.path.join(save_dir, f"{video_id}.mp4")
    
    final_path = expected_path
    if not os.path.exists(expected_path):
        for f in os.listdir(save_dir):
            if f.startswith(video_id) and f.endswith('.mp4'):
                final_path = os.path.join(save_dir, f)
                break
    
    # Check for thumbnail
    thumbnail_path = None
    # yt-dlp saves thumbnail as video_id.jpg or .webp
    # We should look for it.
    possible_exts = ['.jpg', '.jpeg', '.webp', '.png']
    for ext in possible_exts:
        t_path = os.path.join(save_dir, f"{video_id}{ext}")
        if os.path.exists(t_path):
            thumbnail_path = os.path.abspath(t_path)
            break

    # Add to Database
    db_id = database.add_video(
        domain=domain,
        channel_id=channel_id,
        video_id=video_id,
        title=title,
        file_path=os.path.abspath(final_path), # Absolute path is safer
        duration=duration,
        thumbnail_path=thumbnail_path
    )

    # Check for subtitles and import
    subtitle_path = None
    # Preferences: ja.vtt > en.vtt > any.vtt
    # Check simple lang codes first
    for lang in ['ja', 'en', 'live_chat']: 
        s_path = os.path.join(save_dir, f"{video_id}.{lang}.vtt")
        if os.path.exists(s_path):
            subtitle_path = s_path
            break
            
    # Fallback to any vtt starting with video_id
    if not subtitle_path:
        for f in os.listdir(save_dir):
            if f.startswith(video_id) and f.endswith(".vtt"):
                subtitle_path = os.path.join(save_dir, f)
                break
    
    extracted_subs_count = 0
    if subtitle_path and db_id:
        if progress: progress(0.95, desc="Importing subtitles...")
        try:
            segments = utils.parse_vtt_file(subtitle_path)
            if segments:
                database.add_subtitles(db_id, segments)
                extracted_subs_count = len(segments)
        except Exception as e:
            print(f"Failed to parse subtitles: {e}")
    
    # Download Comments/Chat
    chat_file = os.path.join(save_dir, "comments.json")
    chat_log_count = 0
    
    # Try chat-downloader specifically if possible, otherwise rely on yt-dlp if it were enabled (but it's slow).
    # The user specifically asked for chat-downloader.
    try:
        from chat_downloader import ChatDownloader
        if progress: progress(0.98, desc="Downloading Chat/Comments...")
        
        # Limit to top N or first N to avoid getting stuck on 10h streams
        # Or maybe filter by time?
        # For now, let's grab top 500 messages or so if possible.
        # ChatDownloader iterates.
        
        chat_data = []
        downloader_chat = ChatDownloader()
        try:
            # We need the URL again.
            chat_stream = downloader_chat.get_chat(url, message_groups=['messages', 'superchat']) # get messages
            
            count = 0
            for message in chat_stream:
                chat_data.append({
                    'time_text': message.get('time_text'),
                    'time_in_seconds': message.get('time_in_seconds'),
                    'message': message.get('message'),
                    'author': message.get('author', {}).get('name')
                })
                count += 1
                if count >= 1000: # Limit to 1000 comments for performance
                    break
            
            if chat_data:
                with open(chat_file, 'w', encoding='utf-8') as f:
                    json.dump(chat_data, f, indent=4, ensure_ascii=False)
                chat_log_count = len(chat_data)
                
        except Exception as e_chat:
            print(f"Chat download (stream) failed: {e_chat}")
            # Fallback to simple requests if video? ChatDownloader handles VODs too.
            
    except ImportError:
        print("chat-downloader not installed. subprocess call?")
    except Exception as e:
        print(f"Chat download error: {e}")

    return f"Successfully downloaded: {title}. Imported {extracted_subs_count} subtitle segments. Saved {chat_log_count} comments.", db_id
