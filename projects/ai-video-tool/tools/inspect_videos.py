import sqlite3

conn = sqlite3.connect('data/db.sqlite3')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(videos)")
columns = cursor.fetchall()
print("Columns in 'videos' table:")
for col in columns:
    print(col)

print("-" * 20)
cursor.execute("SELECT * FROM videos LIMIT 1")
row = cursor.fetchone()
print("First row:", row)
conn.close()
