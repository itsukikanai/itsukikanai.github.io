import ffmpeg
import os
from app.core import utils

def create_montage(clips, output_filename="montage.mp4", progress=None, fast_preview=False):
    """
    Stitch multiple clips together.
    clips: List of dicts {'video_path': str, 'start': float, 'end': float}
    fast_preview: If True, downscale video and use very fast presets.
    """
    
    if not clips:
        raise ValueError("No clips provided.")
        
    # Output path
    # Output path
    if output_filename.startswith("preview_"):
        temp_dir = "temp"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        output_path = os.path.join(temp_dir, output_filename)
    else:
        base_dir = utils.get_base_download_path()
        output_path = os.path.join(base_dir, output_filename)
    
    if fast_preview and len(clips) == 1:
        # SUPER FAST PREVIEW for single clip: Stream Copy
        # This avoids re-encoding entirely. 
        # Note: Precision might be slightly off (keyframe snap), but for preview it's acceptable.
        clip = clips[0]
        path = clip['video_path']
        start = float(clip['start'])
        end = float(clip['end'])
        duration = end - start
        
        if os.path.exists(path):
            # Input with seek
            inp = ffmpeg.input(path, ss=start, t=duration)
            out = ffmpeg.output(inp, output_path, c='copy')
            
            if progress: progress(0.5, desc="Quick Copying...")
            try:
                out.run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
                if progress: progress(1.0, desc="Preview Ready.")
                return output_path
            except ffmpeg.Error as e:
                print(f"Stream copy failed: {e.stderr.decode('utf-8')}, falling back to encode.")
                # Fallthrough to normal encoding if copy fails
    
    # Build filter complex for multiple clips or if copy not requested/failed
    streams = []
    
    for clip in clips:
        path = clip['video_path']
        start = float(clip['start'])
        end = float(clip['end'])
        duration = end - start
        
        # Check file exists
        if not os.path.exists(path):
            print(f"Warning: File not found {path}, skipping.")
            continue
            
        # FAST SEEKING: Use 'ss' before input (-ss) to jump directly to keyframe.
        input_file = ffmpeg.input(path, ss=start, t=duration)
        
        # Trim video
        v = input_file.video.filter('setpts', 'PTS-STARTPTS')
        
        if fast_preview:
             # Scale to 480p height (keeping aspect ratio) for speed
            v = v.filter('scale', -2, 480)
            
        # Trim audio
        a = input_file.audio.filter('asetpts', 'PTS-STARTPTS')
        
        streams.append(v)
        streams.append(a)
    
    if not streams:
        raise ValueError("No valid clips found.")
        
    joined = ffmpeg.concat(*streams, v=1, a=1).node
    
    if fast_preview:
        # Super fast logic for re-encoding
        out = ffmpeg.output(joined[0], joined[1], output_path, vcodec='libx264', preset='ultrafast', crf=35)
    else:
        # Normal export logic
        out = ffmpeg.output(joined[0], joined[1], output_path, vcodec='libx264', preset='ultrafast', crf=23)
    
    if progress: progress(0.5, desc="Rendering Montage...")
    
    try:
        out.run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
    except ffmpeg.Error as e:
        # print stderr
        print(e.stderr.decode('utf-8'))
        raise RuntimeError("FFmpeg processing failed.")
        
    if progress: progress(1.0, desc="Montage Created.")
    
    return output_path
