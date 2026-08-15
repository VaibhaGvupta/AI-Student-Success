import sqlite3

# Connect to database
conn = sqlite3.connect("students.db")

cursor = conn.cursor()


# Find the first registered student
cursor.execute("SELECT id, name FROM students LIMIT 1")

student = cursor.fetchone()


if student:

    student_id = student[0]
    student_name = student[1]

    # Academic data
    subjects = [
        ("Python", 85, 75),
        ("Database", 78, 75),
        ("Web Development", 72, 75),
        ("Mathematics", 68, 75)
    ]

    # Add academic records
    for subject, marks, attendance in subjects:

        cursor.execute("""
        INSERT INTO academic_data
        (student_id, subject, marks, attendance)
        VALUES (?, ?, ?, ?)
        """, (student_id, subject, marks, attendance))


    conn.commit()

    print("Academic data added successfully!")
    print("Student:", student_name)

else:

    print("No student found.")
    print("Please create an account first.")


conn.close()