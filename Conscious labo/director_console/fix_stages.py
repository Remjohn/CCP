import sqlite3

conn = sqlite3.connect('cmf_database.db')
cursor = conn.cursor()

# Update all projects to scripts stage
cursor.execute("UPDATE projects SET current_stage = 'scripts'")
conn.commit()

# Verify
cursor.execute("SELECT project_id, name, current_stage FROM projects")
for row in cursor.fetchall():
    print(row)

conn.close()
print("Done - all projects set to scripts stage")
