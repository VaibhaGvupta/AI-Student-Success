import sqlite3

# Connect to the database
conn = sqlite3.connect("students.db")

cursor = conn.cursor()

# Add semester column to academic_data
cursor.execute("""
ALTER TABLE academic_data
ADD COLUMN semester INTEGER NOT NULL DEFAULT 1
""")

# Save changes
conn.commit()

# Close database
conn.close()

print("Semester column added successfully!")