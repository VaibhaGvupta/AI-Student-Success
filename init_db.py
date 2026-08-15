import sqlite3

# Connect to the database
conn = sqlite3.connect("students.db")

cursor = conn.cursor()


# --------------------------------
# Create Students Table
# --------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")


# --------------------------------
# Create Academic Data Table
# --------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS academic_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    semester INTEGER NOT NULL,
    subject TEXT NOT NULL,
    marks INTEGER NOT NULL,
    attendance INTEGER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id)
)
""")


# Save changes
conn.commit()

# Close database
conn.close()

print("Database setup completed successfully!")