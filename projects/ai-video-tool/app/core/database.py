import sqlite3
import os
from typing import List, Dict, Optional, Tuple

DB_PATH = os.path.join("data", "db.sqlite3")

def get_db_connection():
    if not os.path.exists("data"):
        os.makedirs("data")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Enable Foreign Keys
    c.execute("PRAGMA foreign_keys = ON;")

    # Videos Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT,
            channel_id TEXT,
            video_id TEXT UNIQUE,
            title TEXT,
            file_path TEXT,
            thumbnail_path TEXT,
            duration REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            analysis_result TEXT
        )
    ''')
    
    # Subtitles Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS subtitles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id INTEGER,
            start_time REAL,
            end_time REAL,
            text TEXT,
            FOREIGN KEY (video_id) REFERENCES videos (id) ON DELETE CASCADE
        )
    ''')

    # FTS5 Virtual Table for Subtitles
    c.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS subtitles_fts USING fts5(
            text,
            content='subtitles',
            content_rowid='id'
        )
    ''')

    # Triggers for FTS5
    c.execute('''
        CREATE TRIGGER IF NOT EXISTS subtitles_ai AFTER INSERT ON subtitles BEGIN
            INSERT INTO subtitles_fts(rowid, text) VALUES (new.id, new.text);
        END;
    ''')
    c.execute('''
        CREATE TRIGGER IF NOT EXISTS subtitles_ad AFTER DELETE ON subtitles BEGIN
            INSERT INTO subtitles_fts(subtitles_fts, rowid, text) VALUES('delete', old.id, old.text);
        END;
    ''')
    c.execute('''
        CREATE TRIGGER IF NOT EXISTS subtitles_au AFTER UPDATE ON subtitles BEGIN
            INSERT INTO subtitles_fts(subtitles_fts, rowid, text) VALUES('delete', old.id, old.text);
            INSERT INTO subtitles_fts(rowid, text) VALUES (new.id, new.text);
        END;
    ''')

    # Tags Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')

    # VideoTags Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS video_tags (
            video_id INTEGER,
            tag_id INTEGER,
            PRIMARY KEY (video_id, tag_id),
            FOREIGN KEY (video_id) REFERENCES videos (id) ON DELETE CASCADE,
            FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()

def add_video(domain, channel_id, video_id, title, file_path, duration, thumbnail_path=None):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO videos (domain, channel_id, video_id, title, file_path, thumbnail_path, duration)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (domain, channel_id, video_id, title, file_path, thumbnail_path, duration))
        new_id = c.lastrowid
        conn.commit()
        return new_id
    except sqlite3.IntegrityError:
        # Video might already exist, get its ID
        c.execute('SELECT id FROM videos WHERE video_id = ?', (video_id,))
        row = c.fetchone()
        if row:
            return row['id']
        return None
    finally:
        conn.close()

def add_subtitles(video_id: int, segments: List[Dict]):
    conn = get_db_connection()
    c = conn.cursor()
    data = [(video_id, s['start'], s['end'], s['text']) for s in segments]
    c.execute('DELETE FROM subtitles WHERE video_id = ?', (video_id,))
    c.executemany('''
        INSERT INTO subtitles (video_id, start_time, end_time, text)
        VALUES (?, ?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()

def get_subtitles(video_id: int) -> List[Dict]:
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM subtitles WHERE video_id = ? ORDER BY start_time ASC', (video_id,))
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def search_subtitles(query: str) -> List[Dict]:
    conn = get_db_connection()
    c = conn.cursor()
    sql = '''
        SELECT 
            s.id as subtitle_id,
            s.video_id,
            s.start_time,
            s.end_time,
            s.text,
            v.title as video_title,
            v.file_path,
            v.video_id as video_uid
        FROM subtitles_fts f
        JOIN subtitles s ON f.rowid = s.id
        JOIN videos v ON s.video_id = v.id
        WHERE subtitles_fts MATCH ?
        ORDER BY rank
        LIMIT 100
    '''
    clean_query = f'"{query}"'
    try:
        c.execute(sql, (clean_query,))
        rows = c.fetchall()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"Search error: {e}")
        return []
    finally:
        conn.close()

def get_all_videos():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM videos ORDER BY created_at DESC')
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_video_by_id(db_id: int):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM videos WHERE id = ?', (db_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def update_video_analysis(video_id: int, analysis_json: str):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('UPDATE videos SET analysis_result = ? WHERE id = ?', (analysis_json, video_id))
    conn.commit()
    conn.close()

def delete_video(db_id: int):
    conn = get_db_connection()
    c = conn.cursor()
    
    # Get file paths first
    c.execute('SELECT file_path, thumbnail_path FROM videos WHERE id = ?', (db_id,))
    row = c.fetchone()
    
    if row:
        file_path = row['file_path']
        thumbnail_path = row['thumbnail_path']
        
        # Delete Video File
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except OSError as e:
                print(f"Error deleting file {file_path}: {e}")

        # Delete Thumbnail
        if thumbnail_path and os.path.exists(thumbnail_path):
            try:
                os.remove(thumbnail_path)
                print(f"Deleted thumbnail: {thumbnail_path}")
            except OSError as e:
                print(f"Error deleting thumbnail {thumbnail_path}: {e}")

    c.execute('DELETE FROM videos WHERE id = ?', (db_id,))
    conn.commit()
    conn.close()
    
    # Cleanup unused tags
    delete_unused_tags()

def delete_unused_tags():
    """
    Delete tags that are not associated with any video.
    """
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute('DELETE FROM tags WHERE id NOT IN (SELECT DISTINCT tag_id FROM video_tags)')
        if c.rowcount > 0:
            print(f"Cleaned up {c.rowcount} unused tags.")
        conn.commit()
    except Exception as e:
        print(f"Error cleaning tags: {e}")
    finally:
        conn.close()

def add_tags(video_id: int, tags: List[str]):
    conn = get_db_connection()
    c = conn.cursor()
    for tag_name in tags:
        tag_name = tag_name.strip()
        if not tag_name: continue
        try:
            c.execute('INSERT INTO tags (name) VALUES (?)', (tag_name,))
            tag_db_id = c.lastrowid
        except sqlite3.IntegrityError:
            c.execute('SELECT id FROM tags WHERE name = ?', (tag_name,))
            res = c.fetchone()
            if res: tag_db_id = res[0]
            else: continue
            
        try:
            c.execute('INSERT INTO video_tags (video_id, tag_id) VALUES (?, ?)', (video_id, tag_db_id))
        except sqlite3.IntegrityError:
            pass
            
    conn.commit()
    conn.close()

def get_video_tags(video_id: int) -> List[str]:
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        SELECT t.name 
        FROM tags t
        JOIN video_tags vt ON t.id = vt.tag_id
        WHERE vt.video_id = ?
    ''', (video_id,))
    rows = c.fetchall()
    conn.close()
    return [r['name'] for r in rows]

def get_all_tags() -> List[str]:
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT name FROM tags ORDER BY name')
    rows = c.fetchall()
    conn.close()
    return [r['name'] for r in rows]

def get_videos_by_tags(tags: List[str]) -> List[Dict]:
    if not tags:
        return get_all_videos()
        
    conn = get_db_connection()
    c = conn.cursor()
    placeholders = ',' .join(['?'] * len(tags))
    # Find videos that have ALL the specified tags? Or ANY?
    # Usually "Filter" means AND logic roughly, or partial match.
    # Let's do ANY for now (OR logic) or maybe AND.
    # If user selects [Action, Funny], they usually want videos that are Action OR Funny?
    # Or videos that are both?
    # Let's stick to "videos that have at least one of these tags" for now (OR).
    
    sql = f'''
        SELECT DISTINCT v.*
        FROM videos v
        JOIN video_tags vt ON v.id = vt.video_id
        JOIN tags t ON vt.tag_id = t.id
        WHERE t.name IN ({placeholders})
        ORDER BY v.created_at DESC
    '''
    c.execute(sql, tags)
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

init_db()

