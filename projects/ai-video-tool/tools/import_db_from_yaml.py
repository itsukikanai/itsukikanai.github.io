import sqlite3
import yaml
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'db.sqlite3')
IMPORT_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'db_export.yaml')

def import_db():
    if not os.path.exists(IMPORT_FILE):
        print(f"Import file not found: {IMPORT_FILE}")
        return

    with open(IMPORT_FILE, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    try:
        # 1. Update Tags
        # Since tags are unique by name, we can update or insert.
        # However, if user renames "Vtuber" to "VTuber" in YAML, we want to unify.
        # For simplicity in this script:
        # We will iterate videos and their tags in the YAML, and ensure those tags exist.
        
        # But first, let's look at the 'tags' list in YAML if user added something there.
        if 'tags' in data:
            for tag in data['tags']:
                # user might have changed 'name' for a given 'id'
                if 'id' in tag and 'name' in tag:
                    # Update name
                    try:
                        c.execute("UPDATE tags SET name = ? WHERE id = ?", (tag['name'], tag['id']))
                    except sqlite3.IntegrityError:
                        print(f"Skipping duplicate tag name: {tag['name']}")
        
        # 2. Update Videos
        if 'videos' in data:
            for vid in data['videos']:
                vid_id = vid.get('id')
                if not vid_id: continue
                
                # Update basic fields if they changed (title, analysis_result)
                c.execute("""
                    UPDATE videos 
                    SET title = ?, analysis_result = ?
                    WHERE id = ?
                """, (vid.get('title'), vid.get('analysis_result'), vid_id))
                
                # Update Tags for this video
                # First delete existing associations
                c.execute("DELETE FROM video_tags WHERE video_id = ?", (vid_id,))
                
                # Re-insert tags
                current_tags = vid.get('tags', [])
                for tag_name in current_tags:
                    tag_name = tag_name.strip()
                    if not tag_name: continue
                    
                    # Ensure tag exists
                    c.execute("SELECT id FROM tags WHERE name = ?", (tag_name,))
                    row = c.fetchone()
                    if row:
                        tag_db_id = row[0]
                    else:
                        c.execute("INSERT INTO tags (name) VALUES (?)", (tag_name,))
                        tag_db_id = c.lastrowid
                    
                    # Link
                    try:
                        c.execute("INSERT INTO video_tags (video_id, tag_id) VALUES (?, ?)", (vid_id, tag_db_id))
                    except sqlite3.IntegrityError:
                        pass

        conn.commit()
        print("Database updated successfully from YAML.")
        
    except Exception as e:
        conn.rollback()
        print(f"Error updating database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    import_db()
