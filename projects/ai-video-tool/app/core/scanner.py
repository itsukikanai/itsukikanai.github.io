import os
import glob
from pathlib import Path
from app.core import database, utils
import yt_dlp

def scan_and_import_videos(progress=None):
    """
    Scans the data directory for videos and imports them into the database if missing.
    """
    base_dir = utils.get_base_download_path()
    if not os.path.exists(base_dir):
        return "Data directory not found."

    found_count = 0
    imported_count = 0
    errors = []

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".mp4"):
                file_path = os.path.join(root, file)
                
                parts = Path(file_path).parts
                if len(parts) < 4:
                    continue
                
                # Assumes structure: data/domain/channel/video_id/filename.mp4
                video_id_dir = parts[-2]
                filename = parts[-1]
                video_id = os.path.splitext(filename)[0]
                
                if video_id != video_id_dir:
                    # Fallback to directory name as ID
                    video_id = video_id_dir

                found_count += 1
                
                # Fetch Info (only if truly needed? add_video checks existence but fetching metadata is slow)
                # Optimization: Check if video exists in DB by string ID first?
                # database.py doesn't expose it easily, but we can assume add_video is fast if it exists.
                # BUT fetching metadata from YouTube is SLOW. We should skip if already in DB.
                # We need a check function in database.py or just try adding with dummy title first?
                # No, we can't update title easily if we insert dummy.
                
                # Let's add a helper to database.py to check existence by string ID? 
                # Or just execute query here.
                conn = database.get_db_connection()
                c = conn.cursor()
                c.execute("SELECT id FROM videos WHERE video_id = ?", (video_id,))
                row = c.fetchone()
                conn.close()
                
                if row:
                    # Already exists, skip expensive metadata fetch
                    continue
                
                # Prepare metadata
                title = video_id
                duration = 0
                thumbnail_path = None
                domain = parts[-4] if len(parts) >=4 else "unknown"
                channel_id = parts[-3] if len(parts) >=4 else "unknown"
                
                # Thumbnail check
                thumb_candidates = glob.glob(os.path.join(root, f"{video_id}.*"))
                for t in thumb_candidates:
                    if t.endswith(('.jpg', '.webp', '.png')):
                        thumbnail_path = os.path.abspath(t)
                        break
                
                # Metadata Fetch
                try:
                    url = None
                    if "youtube" in domain:
                        url = f"https://www.youtube.com/watch?v={video_id}"
                    
                    if url:
                        if progress: progress(0.5, desc=f"Fetching info for {video_id}...")
                        ydl_opts = {'quiet': True, 'ignoreerrors': True}
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(url, download=False)
                            if info:
                                title = info.get('title', title)
                                duration = info.get('duration', duration)
                except Exception as e:
                    errors.append(f"Metadata error for {video_id}: {str(e)}")

                
                # Add
                db_id = database.add_video(
                    domain=domain,
                    channel_id=channel_id,
                    video_id=video_id,
                    title=title,
                    file_path=os.path.abspath(file_path),
                    duration=duration,
                    thumbnail_path=thumbnail_path
                )
                
                if db_id:
                    imported_count += 1
                    # Import subtitles
                    vtt_files = glob.glob(os.path.join(root, "*.vtt"))
                    for vtt in vtt_files:
                        try:
                            segments = utils.parse_vtt_file(vtt)
                            if segments:
                                database.add_subtitles(db_id, segments)
                        except:
                            pass

    return f"Scan complete. Found {found_count} videos, Imported {imported_count} new videos."
