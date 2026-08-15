import sqlite3


def analyze_student(student_id, semester):

    # --------------------------------
    # Connect to database
    # --------------------------------

    conn = sqlite3.connect("students.db")

    cursor = conn.cursor()


    # --------------------------------
    # Get academic data
    # --------------------------------

    cursor.execute("""
        SELECT subject, marks, attendance
        FROM academic_data
        WHERE student_id = ?
        AND semester = ?
    """, (
        student_id,
        semester
    ))

    academic_data = cursor.fetchall()

    conn.close()


    # --------------------------------
    # No academic data
    # --------------------------------

    if not academic_data:

        return {
            "average": 0,
            "strongest_subject": "No data",
            "strongest_marks": 0,
            "weakest_subject": "No data",
            "weakest_marks": 0,
            "attendance": 0,
            "performance_level": "No Data",
            "attendance_status": "No Data",
            "student_status": "No Data",
            "status_message": "Add academic data to receive your student success status.",
            "subject_status": "No Data",
            "subject_status_message": "No subject data is available yet.",
            "recommendation": f"No academic data is available for Semester {semester} yet.",
            "goal": "Add your academic subjects and marks to receive an AI analysis.",
            "study_recommendations": [],
            "study_plan": []
        }


    # --------------------------------
    # Calculate average
    # --------------------------------

    total_marks = sum(
        row[1]
        for row in academic_data
    )

    average = round(
        total_marks / len(academic_data)
    )


    # --------------------------------
    # Strongest subject
    # --------------------------------

    strongest = max(
        academic_data,
        key=lambda x: x[1]
    )

    strongest_subject = strongest[0]
    strongest_marks = strongest[1]


    # --------------------------------
    # Lowest-scoring subject
    # --------------------------------

    weakest = min(
        academic_data,
        key=lambda x: x[1]
    )

    weakest_subject = weakest[0]
    weakest_marks = weakest[1]


    # --------------------------------
    # Average attendance
    # --------------------------------

    attendance = round(
        sum(row[2] for row in academic_data)
        / len(academic_data)
    )


    # --------------------------------
    # Performance level
    # --------------------------------

    if average >= 90:

        performance_level = "Excellent"

    elif average >= 80:

        performance_level = "Very Good"

    elif average >= 70:

        performance_level = "Good"

    elif average >= 60:

        performance_level = "Average"

    elif average >= 50:

        performance_level = "Needs Improvement"

    else:

        performance_level = "At Risk"


    # --------------------------------
    # Attendance status
    # --------------------------------

    if attendance >= 85:

        attendance_status = "Excellent"

    elif attendance >= 75:

        attendance_status = "Good"

    elif attendance >= 65:

        attendance_status = "Needs Attention"

    else:

        attendance_status = "Critical"


    # --------------------------------
    # Student status
    # --------------------------------

    if average >= 70 and attendance >= 75:

        student_status = "On Track"

        status_message = (
            "Your academic performance and attendance "
            "are currently at a healthy level. "
            "Keep maintaining your current progress."
        )

    elif average >= 60 or attendance >= 65:

        student_status = "Needs Attention"

        status_message = (
            "Your performance shows some areas that "
            "need attention. Focus on improving your "
            "weaker subject and maintaining better "
            "attendance."
        )

    else:

        student_status = "At Risk"

        status_message = (
            "Your academic performance and attendance "
            "both require immediate attention. "
            "A consistent study routine and regular "
            "class attendance are recommended."
        )


    # --------------------------------
    # Subject insight
    # --------------------------------

    if weakest_marks >= 80:

        subject_status = "Strong Performance"

        subject_status_message = (
            f"{weakest_subject} — {weakest_marks} marks. "
            f"You are performing strongly in this subject. "
            f"Focus on maintaining consistent performance."
        )

    elif weakest_marks >= 60:

        subject_status = "Moderate Performance"

        subject_status_message = (
            f"{weakest_subject} — {weakest_marks} marks. "
            f"This subject has room for improvement. "
            f"Regular revision and practice can help "
            f"you improve your score."
        )

    else:

        subject_status = "Needs Improvement"

        subject_status_message = (
            f"{weakest_subject} — {weakest_marks} marks. "
            f"This subject requires focused attention. "
            f"Try additional practice, revision, and "
            f"regular study sessions."
        )


    # --------------------------------
    # Study Recommendations
    # --------------------------------

    study_recommendations = []


    sorted_subjects = sorted(
        academic_data,
        key=lambda x: x[1]
    )


    for subject, marks, subject_attendance in sorted_subjects:

        if marks < 60:

            study_recommendations.append({
                "subject": subject,
                "marks": marks,
                "priority": "High Priority",
                "icon": "🔴",
                "message": (
                    f"Give {subject} extra study time. "
                    f"Focus on understanding basic concepts, "
                    f"practice questions regularly, and review "
                    f"mistakes from previous tests."
                )
            })

        elif marks < 80:

            study_recommendations.append({
                "subject": subject,
                "marks": marks,
                "priority": "Improvement Recommended",
                "icon": "🟡",
                "message": (
                    f"Spend some additional time on {subject}. "
                    f"Regular revision and practice can help "
                    f"you improve your current score."
                )
            })

        else:

            study_recommendations.append({
                "subject": subject,
                "marks": marks,
                "priority": "Maintain Performance",
                "icon": "🟢",
                "message": (
                    f"You are performing strongly in {subject}. "
                    f"Continue regular practice and maintain "
                    f"your current level of performance."
                )
            })


    # --------------------------------
    # Main recommendation
    # --------------------------------

    if average >= 80 and attendance >= 80:

        recommendation = (
            f"Excellent work! Your academic performance "
            f"and attendance are both strong. Your strongest "
            f"subject is {strongest_subject} with "
            f"{strongest_marks} marks. Continue maintaining "
            f"this level of performance."
        )

    elif average >= 70 and attendance >= 75:

        recommendation = (
            f"Your overall academic performance is good. "
            f"Your strongest subject is {strongest_subject} "
            f"with {strongest_marks} marks. Continue "
            f"maintaining your strong subjects and spend "
            f"some additional time reviewing {weakest_subject}."
        )

    elif average >= 70 and attendance < 75:

        recommendation = (
            f"Your academic performance is good, but your "
            f"attendance needs improvement. Your attendance "
            f"is {attendance}%. Try to attend classes more "
            f"regularly while continuing to work on "
            f"{weakest_subject}."
        )

    elif average < 70 and attendance >= 75:

        recommendation = (
            f"Your attendance is good, but your academic "
            f"performance needs improvement. Focus especially "
            f"on {weakest_subject}, where you scored "
            f"{weakest_marks} marks. Regular practice and "
            f"revision can help improve your marks."
        )

    else:

        recommendation = (
            f"Your academic performance and attendance need "
            f"attention. Your attendance is {attendance}%. "
            f"Focus especially on {weakest_subject}, where "
            f"you scored {weakest_marks} marks. Create a "
            f"regular study routine and attend classes more "
            f"consistently."
        )


    # --------------------------------
    # Improvement Goal
    # --------------------------------

    if weakest_marks >= 90:

        goal = (
            f"Maintain {weakest_subject} above "
            f"{weakest_marks - 5} marks and focus on "
            f"keeping your performance consistent."
        )

    elif weakest_marks >= 80:

        target_marks = min(
            weakest_marks + 5,
            100
        )

        goal = (
            f"Try to improve {weakest_subject} from "
            f"{weakest_marks} to around {target_marks} marks "
            f"while maintaining consistent performance."
        )

    elif weakest_marks >= 60:

        target_marks = min(
            weakest_marks + 10,
            100
        )

        goal = (
            f"Try to improve {weakest_subject} from "
            f"{weakest_marks} to at least {target_marks} marks "
            f"through regular revision and practice."
        )

    else:

        target_marks = min(
            weakest_marks + 15,
            100
        )

        goal = (
            f"Focus strongly on {weakest_subject} and try "
            f"to improve your score from {weakest_marks} "
            f"to at least {target_marks} marks."
        )


    if attendance < 75:

        goal += (
            f" Also aim to improve your attendance from "
            f"{attendance}% to at least 80%."
        )


    # ==================================================
    # STEP 30 — 7 DAY AI STUDY PLAN
    # ==================================================

    study_plan = []


    # --------------------------------
    # Choose important subjects
    # --------------------------------

    priority_subjects = sorted(
        academic_data,
        key=lambda x: x[1]
    )


    # Take up to 3 subjects

    priority_subjects = priority_subjects[:3]


    # --------------------------------
    # Day 1
    # --------------------------------

    first_subject = priority_subjects[0]

    if first_subject[1] < 60:

        day1_task = (
            f"Review the basic concepts of "
            f"{first_subject[0]} and identify the "
            f"topics you find difficult."
        )

        day1_time = "60 minutes"

    elif first_subject[1] < 80:

        day1_task = (
            f"Revise important topics from "
            f"{first_subject[0]} and make short notes."
        )

        day1_time = "45 minutes"

    else:

        day1_task = (
            f"Review important topics from "
            f"{first_subject[0]} and maintain your "
            f"current understanding."
        )

        day1_time = "30 minutes"


    study_plan.append({
        "day": "Day 1",
        "title": first_subject[0],
        "task": day1_task,
        "time": day1_time,
        "icon": "📖"
    })


    # --------------------------------
    # Day 2
    # --------------------------------

    if first_subject[1] < 60:

        day2_task = (
            f"Practice basic questions from "
            f"{first_subject[0]} and review your mistakes."
        )

        day2_time = "60 minutes"

    else:

        day2_task = (
            f"Practice questions from "
            f"{first_subject[0]} and review your mistakes."
        )

        day2_time = "45 minutes"


    study_plan.append({
        "day": "Day 2",
        "title": first_subject[0],
        "task": day2_task,
        "time": day2_time,
        "icon": "✏️"
    })


    # --------------------------------
    # Day 3
    # --------------------------------

    if len(priority_subjects) >= 2:

        second_subject = priority_subjects[1]

        if second_subject[1] < 60:

            day3_task = (
                f"Study the important concepts of "
                f"{second_subject[0]} and practice basic questions."
            )

            day3_time = "60 minutes"

        else:

            day3_task = (
                f"Revise important topics from "
                f"{second_subject[0]} and practice questions."
            )

            day3_time = "45 minutes"

        day3_title = second_subject[0]

    else:

        day3_task = (
            f"Continue practicing {first_subject[0]} "
            f"and review difficult topics."
        )

        day3_time = "45 minutes"

        day3_title = first_subject[0]


    study_plan.append({
        "day": "Day 3",
        "title": day3_title,
        "task": day3_task,
        "time": day3_time,
        "icon": "📚"
    })


    # --------------------------------
    # Day 4
    # --------------------------------

    if len(priority_subjects) >= 2:

        second_subject = priority_subjects[1]

        day4_task = (
            f"Practice questions in {second_subject[0]} "
            f"and revise the topics where you made mistakes."
        )

        day4_title = second_subject[0]

    else:

        day4_task = (
            f"Practice more questions in "
            f"{first_subject[0]} and check your progress."
        )

        day4_title = first_subject[0]


    study_plan.append({
        "day": "Day 4",
        "title": day4_title,
        "task": day4_task,
        "time": "45 minutes",
        "icon": "✏️"
    })


    # --------------------------------
    # Day 5
    # --------------------------------

    if len(priority_subjects) >= 3:

        third_subject = priority_subjects[2]

        day5_task = (
            f"Revise important topics from "
            f"{third_subject[0]} and practice a few questions."
        )

        day5_title = third_subject[0]

    else:

        day5_task = (
            f"Review your progress in {first_subject[0]} "
            f"and revise your weakest topics."
        )

        day5_title = first_subject[0]


    study_plan.append({
        "day": "Day 5",
        "title": day5_title,
        "task": day5_task,
        "time": "45 minutes",
        "icon": "📝"
    })


    # --------------------------------
    # Day 6
    # --------------------------------

    day6_task = (
        f"Mixed revision: review {first_subject[0]} "
        f"and your other weaker subjects. "
        f"Focus on mistakes and difficult topics."
    )


    study_plan.append({
        "day": "Day 6",
        "title": "Mixed Revision",
        "task": day6_task,
        "time": "60 minutes",
        "icon": "📚"
    })


    # --------------------------------
    # Day 7
    # --------------------------------

    day7_task = (
        "Take a small self-assessment or practice test. "
        "Review your mistakes and identify the topics "
        "that need more attention next week."
    )


    study_plan.append({
        "day": "Day 7",
        "title": "Self Assessment",
        "task": day7_task,
        "time": "45 minutes",
        "icon": "📝"
    })


    # --------------------------------
    # Return everything
    # --------------------------------

    return {

        "average": average,

        "strongest_subject":
            strongest_subject,

        "strongest_marks":
            strongest_marks,

        "weakest_subject":
            weakest_subject,

        "weakest_marks":
            weakest_marks,

        "attendance":
            attendance,

        "performance_level":
            performance_level,

        "attendance_status":
            attendance_status,

        "student_status":
            student_status,

        "status_message":
            status_message,

        "subject_status":
            subject_status,

        "subject_status_message":
            subject_status_message,

        "recommendation":
            recommendation,

        "goal":
            goal,

        "study_recommendations":
            study_recommendations,

        "study_plan":
            study_plan

    }