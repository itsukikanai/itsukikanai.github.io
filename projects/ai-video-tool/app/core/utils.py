import os
import json
import re
from pathlib import Path

CONFIG_PATH = "config.json"

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)

def sanitize_filename(name):
    """
    Sanitize a string to be safe for filenames.
    """
    return re.sub(r'[\\/*?:"<>|]', "", name)

def get_base_download_path():
    config = load_config()
    return config.get("download_path", "data")

def format_timestamp(seconds: float, as_srt: bool = False) -> str:
    """
    Format seconds into HH:MM:SS.mmm (or HH:MM:SS,mmm for SRT)
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    formatted = "{:02d}:{:02d}:{:06.3f}".format(int(h), int(m), s)
    if as_srt:
        return formatted.replace('.', ',')
    return formatted

def parse_timestamp(timestamp_str: str) -> float:
    """
    Parse HH:MM:SS.mmm to seconds.
    """
    parts = timestamp_str.split(':')
    if len(parts) == 3:
        h, m, s = parts
        return int(h) * 3600 + int(m) * 60 + float(s)
    elif len(parts) == 2:
        m, s = parts
        return int(m) * 60 + float(s)
    else:
        return float(parts[0])

def parse_vtt_file(file_path: str):
    """
    Parse a WebVTT file into a list of segments:
    [{'start': 0.0, 'end': 10.0, 'text': 'Hello'}, ...]
    """
    segments = []
    if not os.path.exists(file_path):
        return segments
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # Simple State Machine
    # VTT files have 'WEBVTT' header, then blocks.
    # Block:
    # (Optional ID)
    # 00:00:00.000 --> 00:00:05.000
    # Text line 1
    # Text line 2
    
    current_segment = None
    
    # Regex for timestamp line: 00:00:00.000 --> 00:00:05.000
    # Also handles SRT comma format just in case
    time_pattern = re.compile(r'(\d{2}:\d{2}:\d{2}[\.,]\d{3})\s-->\s(\d{2}:\d{2}:\d{2}[\.,]\d{3})')
    
    for line in lines:
        line = line.strip()
        if not line:
            if current_segment:
                segments.append(current_segment)
                current_segment = None
            continue
            
        if line == 'WEBVTT':
            continue
            
        # Check for timing
        match = time_pattern.search(line)
        if match:
            if current_segment:
                segments.append(current_segment)
                
            start_str = match.group(1).replace(',', '.')
            end_str = match.group(2).replace(',', '.')
            
            try:
                start = parse_timestamp(start_str)
                end = parse_timestamp(end_str)
                current_segment = {'start': start, 'end': end, 'text': ''}
            except:
                current_segment = None
            continue
            
        # If inside segment, append text
        if current_segment:
            if current_segment['text']:
                current_segment['text'] += " " + line
            else:
                current_segment['text'] = line
    
    # Add last one
    if current_segment:
        segments.append(current_segment)
    
    # De-duplicate segments (fix for rolling captions)
    clean_segments = []
    last_text = ""
    for seg in segments:
        text = seg['text'].strip()
        # Clean up text (optional: remove HTML tags if any)
        text = re.sub(r'<[^>]+>', '', text)
        seg['text'] = text
        
        if not text:
            continue
            
        # Strategy 1: Exact match with previous
        if text == last_text:
            continue
            
        # Strategy 2: If text starts with last_text (common in accumulative captions)
        # e.g. "Hello" -> "Hello World"
        # We might want to keep the longer one.
        # But simpler logic for rolling captions (User wants to avoid duplication):
        # Often: "Hello" (0-2s) -> "Hello" (2-3s).
        # Or: "Hello" -> "Hello world".
        # Let's just use strict equality filter for now, which is the most common annoyance.
        
        # Strategy 3: Overlap check?
        # If segments overlap significantly and text is same, it's definitely a dupe.
        
        clean_segments.append(seg)
        last_text = text
        
    return clean_segments
