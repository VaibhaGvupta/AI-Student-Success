import sqlite3


# =========================================================
# GET STUDENT ACADEMIC DATA
# =========================================================

def get_student_data(student_id):

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            subject,
            marks,
            attendance,
            semester
        FROM academic_data
        WHERE student_id = ?
        ORDER BY semester, id
        """,
        (student_id,)
    )

    data = cursor.fetchall()

    conn.close()

    return data


# =========================================================
# CALCULATE GRADE
# =========================================================

def get_grade(marks):

    if marks >= 90:
        return "A+"

    elif marks >= 80:
        return "A"

    elif marks >= 70:
        return "B+"

    elif marks >= 60:
        return "B"

    elif marks >= 50:
        return "C"

    else:
        return "Needs Improvement"


# =========================================================
# CHATBOT RESPONSE
# =========================================================

def chatbot_response(student_id, message):

    message = message.lower().strip()

    # Get student's academic data
    data = get_student_data(student_id)


    # =====================================================
    # NO ACADEMIC DATA
    # =====================================================

    if not data:

        return (
            "I don't have any academic data for you yet. "
            "Please add your subjects, marks and attendance "
            "from the dashboard so I can analyze your performance."
        )


    # =====================================================
    # CALCULATE OVERALL PERFORMANCE
    # =====================================================

    total_marks = sum(
        row[1]
        for row in data
    )

    average_marks = round(
        total_marks / len(data)
    )


    total_attendance = sum(
        row[2]
        for row in data
    )

    average_attendance = round(
        total_attendance / len(data)
    )


    overall_grade = get_grade(
        average_marks
    )


    # =====================================================
    # FIND BEST SUBJECT
    # =====================================================

    best_subject = max(
        data,
        key=lambda row: row[1]
    )

    best_subject_name = best_subject[0]
    best_subject_marks = best_subject[1]


    # =====================================================
    # FIND WEAKEST SUBJECT
    # =====================================================

    weakest_subject = min(
        data,
        key=lambda row: row[1]
    )

    weakest_subject_name = weakest_subject[0]
    weakest_subject_marks = weakest_subject[1]


    # =====================================================
    # ATTENDANCE SUBJECT
    # =====================================================

    lowest_attendance_subject = min(
        data,
        key=lambda row: row[2]
    )

    lowest_attendance_name = lowest_attendance_subject[0]
    lowest_attendance_value = lowest_attendance_subject[2]


    # =====================================================
    # PERFORMANCE QUESTION
    # =====================================================

    if (
        "performance" in message
        or "performing" in message
        or "how am i doing" in message
        or "how am i doing" in message
    ):

        return (
            f"Based on your academic data, your average marks are "
            f"{average_marks}% and your overall grade is {overall_grade}. "
            f"Your average attendance is {average_attendance}%. "
            f"Your strongest subject is {best_subject_name} "
            f"with {best_subject_marks} marks, while your weakest "
            f"subject is {weakest_subject_name} with "
            f"{weakest_subject_marks} marks."
        )


    # =====================================================
    # MARKS QUESTION
    # =====================================================

    if (
        "marks" in message
        or "score" in message
        or "average" in message
        or "percentage" in message
    ):

        return (
            f"Your current average marks are {average_marks}%. "
            f"Your overall grade is {overall_grade}. "
            f"Your best subject is {best_subject_name} "
            f"({best_subject_marks} marks), and your weakest "
            f"subject is {weakest_subject_name} "
            f"({weakest_subject_marks} marks)."
        )


    # =====================================================
    # ATTENDANCE QUESTION
    # =====================================================

    if (
        "attendance" in message
        or "present" in message
        or "absent" in message
    ):

        if average_attendance >= 75:

            attendance_advice = (
                "Your attendance is currently in a good range."
            )

        else:

            attendance_advice = (
                "Your attendance is below 75%, so you should "
                "focus on attending classes more regularly."
            )

        return (
            f"Your average attendance is {average_attendance}%. "
            f"{attendance_advice} "
            f"Your lowest-attendance subject is "
            f"{lowest_attendance_name} with "
            f"{lowest_attendance_value}% attendance."
        )


    # =====================================================
    # BEST SUBJECT QUESTION
    # =====================================================

    if (
        "best subject" in message
        or "strongest subject" in message
        or "good at" in message
        or "strong subject" in message
    ):

        return (
            f"Your strongest subject is {best_subject_name} "
            f"with {best_subject_marks} marks. "
            f"You are currently performing best in this subject."
        )


    # =====================================================
    # WEAK SUBJECT QUESTION
    # =====================================================

    if (
        "weak subject" in message
        or "weakest subject" in message
        or "improve" in message
        or "improvement" in message
    ):

        return (
            f"Your weakest subject is {weakest_subject_name} "
            f"with {weakest_subject_marks} marks. "
            f"I recommend giving this subject additional study "
            f"time and practicing more questions from this area."
        )


    # =====================================================
    # GRADE QUESTION
    # =====================================================

    if (
        "grade" in message
        or "result" in message
    ):

        return (
            f"Your current average marks are {average_marks}%, "
            f"which corresponds to an overall grade of "
            f"{overall_grade}."
        )


    # =====================================================
    # ADVICE QUESTION
    # =====================================================

    if (
        "advice" in message
        or "suggest" in message
        or "study" in message
        or "what should i do" in message
    ):

        if average_marks >= 80 and average_attendance >= 75:

            return (
                f"Your academic performance is strong. "
                f"Your average is {average_marks}% with "
                f"{average_attendance}% attendance. "
                f"Keep maintaining your current study routine "
                f"and continue focusing on {weakest_subject_name} "
                f"to improve further."
            )

        elif average_marks >= 60:

            return (
                f"Your average is {average_marks}% and your "
                f"attendance is {average_attendance}%. "
                f"You have a good foundation, but you should "
                f"focus more on {weakest_subject_name} and "
                f"maintain regular attendance."
            )

        else:

            return (
                f"Your current average is {average_marks}%. "
                f"I recommend creating a regular study schedule, "
                f"focusing first on {weakest_subject_name}, "
                f"and improving your class attendance."
            )


    # =====================================================
    # HELP QUESTION
    # =====================================================

    if (
        "help" in message
        or "hello" in message
        or "hi" in message
        or "hey" in message
    ):

        return (
            "Hello! 👋 I'm your AI Student Assistant. "
            "You can ask me things like: "
            "'How am I performing?', "
            "'What is my attendance?', "
            "'Which is my best subject?', "
            "'Which subject should I improve?', or "
            "'Give me study advice.'"
        )


    # =====================================================
    # DEFAULT RESPONSE
    # =====================================================

    return (
        "I can help you understand your academic performance. "
        "Try asking me about your marks, attendance, grade, "
        "best subject, weakest subject, or study advice."
    )