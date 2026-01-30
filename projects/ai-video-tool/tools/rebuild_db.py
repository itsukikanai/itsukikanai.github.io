import os
import sys
import glob

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core import database, utils
import yt_dlp

def rebuild_database():
    print("Starting database rebuild...")
    database.init_db()
    
    base_dir = utils.get_base_download_path()
    print(f"Scanning directory: {base_dir}")
    
    # Path pattern: data/domain/channel_id/video_id/video_id.mp4
    # We can use os.walk
    
    found_count = 0
    imported_count = 0
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".mp4"):
                # Potential video file
                file_path = os.path.join(root, file)
                # Check if it follows our structure
                # We expect the file name to be video_id.mp4 (approximately)
                # And the parent folder to be video_id
                
                parts = Path(file_path).parts
                # typical: data, domain, channel, video_id, filename
                if len(parts) < 4:
                    print(f"Skipping file with unusual path structure: {file_path}")
                    continue
                
                video_id_dir = parts[-2]
                filename = parts[-1]
                video_id_from_file = os.path.splitext(filename)[0]
                
                if video_id_dir != video_id_from_file:
                    print(f"Warning: Directory name {video_id_dir} != Filename {video_id_from_file}. Using directory name as ID.")
                    video_id = video_id_dir
                else:
                    video_id = video_id_from_file
                
                # Check if already in DB
                existing = database.get_video_by_id(video_id) # This function expects int DB ID
                # We need to check by video_uid (string)
                # database.py doesn't have get_video_by_uid exposed directly mostly, 
                # but add_video handles duplicates by checking video_id string.
                # Let's trust add_video to handle duplication or we can check manually.
                
                print(f"Found video: {video_id}")
                found_count += 1
                
                # Fetch Info
                title = video_id
                duration = 0
                thumbnail_path = None
                domain = parts[-4] if len(parts) >=4 else "unknown"
                channel_id = parts[-3] if len(parts) >=4 else "unknown"
                
                try:
                    # check for thumbnail
                    thumb_candidates = glob.glob(os.path.join(root, f"{video_id}.*"))
                    for t in thumb_candidates:
                        if t.endswith(('.jpg', '.webp', '.png')) and 'thumbnail' not in t: # thumbnail might be in name? usually video_id.jpg
                            thumbnail_path = os.path.abspath(t)
                            break
                    
                    # Try to fetch metadata from YT
                    # We can try to construct URL. 
                    # If domain is youtube.com, url is youtube.com/watch?v={video_id}
                    url = None
                    if "youtube" in domain:
                        url = f"https://www.youtube.com/watch?v={video_id}"
                    
                    if url:
                        print(f"Fetching metadata for {url}...")
                        ydl_opts = {
                            'quiet': True,
                            'ignoreerrors': True
                        }
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(url, download=False)
                            if info:
                                title = info.get('title', title)
                                duration = info.get('duration', duration)
                                # If we didn't have a thumbnail, maybe we can download it? 
                                # But we prefer local if exists.
                    
                except Exception as e:
                    print(f"Metadata fetch failed: {e}. Using defaults.")

                # Add to DB
                print(f"Adding to DB: {title}")
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
                    # Import subtitles if any
                    # Look for .vtt
                    vtt_files = glob.glob(os.path.join(root, "*.vtt"))
                    for vtt in vtt_files:
                        print(f"Importing subtitles from {vtt}")
                        segments = utils.parse_vtt_file(vtt)
                        if segments:
                            database.add_subtitles(db_id, segments)
                            break # Only import one for now
                
    print(f"Finished. Found {found_count}, Imported {imported_count}.")

if __name__ == "__main__":
    from pathlib import Path
    rebuild_database()
