import sqlite3
import os

db_path = 'data/db.sqlite3'
old_prefix = 'C:\\ai-video-tool-2'
new_prefix = 'C:\\ai-video-tool'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Update file_path
cursor.execute(f"""
UPDATE videos 
SET file_path = REPLACE(file_path, ?, ?) 
WHERE file_path LIKE ?
""", (old_prefix, new_prefix, f"{old_prefix}%"))

print(f"Updated {cursor.rowcount} file_paths.")

# Update thumbnail_path
cursor.execute(f"""
UPDATE videos 
SET thumbnail_path = REPLACE(thumbnail_path, ?, ?) 
WHERE thumbnail_path LIKE ?
""", (old_prefix, new_prefix, f"{old_prefix}%"))

print(f"Updated {cursor.rowcount} thumbnail_paths.")

conn.commit()

# Verify
cursor.execute("SELECT file_path FROM videos LIMIT 5")
print("\nUpdated paths:")
for row in cursor.fetchall():
    print(row[0])

conn.close()
