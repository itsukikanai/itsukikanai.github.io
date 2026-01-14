import sqlite3
import yaml
import os
import datetime

# Configure safe dumping for YAML
def str_presenter(dumper, data):
    if len(data.splitlines()) > 1:  # for multiline strings
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, str_presenter)

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'db.sqlite3')
EXPORT_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'db_export.yaml')

def export_db():
    if not os.path.exists(DB_PATH):
        print(f"Database not found: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    data = {}
    
    # Export Tags
    c.execute("SELECT * FROM tags ORDER BY id")
    tags = [dict(row) for row in c.fetchall()]
    data['tags'] = tags
    
    # Export Videos and their tags/analysis
    c.execute("SELECT * FROM videos ORDER BY id")
    videos = []
    for row in c.fetchall():
        vid = dict(row)
        # Get tags for this video
        c.execute("""
            SELECT t.name 
            FROM tags t
            JOIN video_tags vt ON t.id = vt.tag_id
            WHERE vt.video_id = ?
        """, (vid['id'],))
        vid_tags = [r[0] for r in c.fetchall()]
        vid['tags'] = vid_tags
        videos.append(vid)
        
    data['videos'] = videos
    
    conn.close()
    
    with open(EXPORT_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)
        
    print(f"Database exported to {EXPORT_FILE}")
    print("You can edit this file and run 'python tools/import_db_from_yaml.py' to apply changes.")

if __name__ == "__main__":
    export_db()
