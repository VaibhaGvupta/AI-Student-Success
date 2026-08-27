from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3

from ai_analysis import analyze_student
from chatbot import chatbot_response


app = Flask(__name__)

# Secret key for session
app.secret_key = "ai_student_success_secret_key"


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template("index.html")


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    # -----------------------------------------------------
    # SHOW LOGIN PAGE
    # -----------------------------------------------------

    if request.method == "GET":

        return render_template("login.html")


    # -----------------------------------------------------
    # PROCESS LOGIN
    # -----------------------------------------------------

    email = request.form["email"].strip()
    password = request.form["password"]

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM students
        WHERE email = ?
        AND password = ?
        """,
        (email, password)
    )

    student = cursor.fetchone()

    conn.close()

    if student:

        session["student_id"] = student[0]
        session["student_name"] = student[1]

        # Normal login should not show account-created notification
        session.pop("account_created", None)

        return redirect(
            url_for("dashboard")
        )

    else:

        return "Invalid email or password"


# =========================================================
# FORGOT PASSWORD
# =========================================================

@app.route(
    "/forgot-password",
    methods=["GET", "POST"]
)
def forgot_password():

    # -----------------------------------------------------
    # SHOW FORGOT PASSWORD PAGE
    # -----------------------------------------------------

    if request.method == "GET":

        return render_template(
            "forgot_password.html"
        )


    # -----------------------------------------------------
    # GET FORM DATA
    # -----------------------------------------------------

    email = request.form.get("email", "").strip()

    if not email:

        return render_template(
            "forgot_password.html",
            error="Please enter your email address."
        )


    # -----------------------------------------------------
    # CONNECT DATABASE
    # -----------------------------------------------------

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()


    # -----------------------------------------------------
    # CHECK REGISTERED EMAIL
    # -----------------------------------------------------

    cursor.execute(
        """
        SELECT id
        FROM students
        WHERE email = ?
        """,
        (email,)
    )

    student = cursor.fetchone()

    conn.close()


    # -----------------------------------------------------
    # EMAIL NOT FOUND
    # -----------------------------------------------------

    if not student:

        return render_template(
            "forgot_password.html",
            error="No account found with that email address. Please check and try again."
        )


    # -----------------------------------------------------
    # STORE RESET EMAIL IN SESSION & REDIRECT
    # -----------------------------------------------------

    session["reset_email"] = email

    return redirect(
        url_for("reset_password")
    )


# =========================================================
# RESET PASSWORD
# =========================================================

@app.route(
    "/reset-password",
    methods=["GET", "POST"]
)
def reset_password():

    # -----------------------------------------------------
    # CHECK RESET SESSION
    # -----------------------------------------------------

    reset_email = session.get("reset_email")

    if not reset_email:

        return redirect(
            url_for("forgot_password")
        )


    # -----------------------------------------------------
    # SHOW RESET PASSWORD PAGE
    # -----------------------------------------------------

    if request.method == "GET":

        return render_template(
            "reset_password.html"
        )


    # -----------------------------------------------------
    # GET FORM DATA
    # -----------------------------------------------------

    new_password = request.form.get("new_password", "")

    confirm_password = request.form.get("confirm_password", "")


    # -----------------------------------------------------
    # CHECK PASSWORD LENGTH
    # -----------------------------------------------------

    if len(new_password) < 6:

        return render_template(
            "reset_password.html",
            error="Password must be at least 6 characters long."
        )


    # -----------------------------------------------------
    # CHECK PASSWORD MATCH
    # -----------------------------------------------------

    if new_password != confirm_password:

        return render_template(
            "reset_password.html",
            error="Passwords do not match. Please ensure both passwords match."
        )


    # -----------------------------------------------------
    # CONNECT DATABASE
    # -----------------------------------------------------

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()


    # -----------------------------------------------------
    # UPDATE PASSWORD
    # -----------------------------------------------------

    cursor.execute(
        """
        UPDATE students
        SET password = ?
        WHERE email = ?
        """,
        (
            new_password,
            reset_email
        )
    )

    conn.commit()

    conn.close()


    # -----------------------------------------------------
    # CLEAR RESET SESSION
    # -----------------------------------------------------

    session.pop("reset_email", None)


    # -----------------------------------------------------
    # PASSWORD RESET SUCCESS
    # -----------------------------------------------------

    return render_template(
        "reset_success.html"
    )



# =========================================================
# CHANGE PASSWORD
# =========================================================

@app.route(
    "/change-password",
    methods=["GET", "POST"]
)
def change_password():

    # -----------------------------------------------------
    # CHECK LOGIN
    # -----------------------------------------------------

    student_id = session.get("student_id")

    if not student_id:

        return redirect(
            url_for("login")
        )


    # -----------------------------------------------------
    # SHOW CHANGE PASSWORD PAGE
    # -----------------------------------------------------

    if request.method == "GET":

        return render_template(
            "change_password.html"
        )


    # -----------------------------------------------------
    # GET FORM DATA
    # -----------------------------------------------------

    current_password = request.form.get(
        "current_password",
        ""
    )

    new_password = request.form.get(
        "new_password",
        ""
    )

    confirm_password = request.form.get(
        "confirm_password",
        ""
    )


    # -----------------------------------------------------
    # CHECK CURRENT PASSWORD FIELD
    # -----------------------------------------------------

    if not current_password:

        return render_template(
            "change_password.html",
            error="Please enter your current password."
        )


    # -----------------------------------------------------
    # CHECK NEW PASSWORD LENGTH
    # -----------------------------------------------------

    if len(new_password) < 6:

        return render_template(
            "change_password.html",
            error="New password must be at least 6 characters long."
        )


    # -----------------------------------------------------
    # CHECK NEW PASSWORD MATCH
    # -----------------------------------------------------

    if new_password != confirm_password:

        return render_template(
            "change_password.html",
            error="New password and confirm password do not match."
        )


    # -----------------------------------------------------
    # CHECK NEW PASSWORD IS DIFFERENT
    # -----------------------------------------------------

    if current_password == new_password:

        return render_template(
            "change_password.html",
            error="New password must be different from your current password."
        )


    # -----------------------------------------------------
    # CONNECT DATABASE
    # -----------------------------------------------------

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()


    # -----------------------------------------------------
    # GET CURRENT PASSWORD
    # -----------------------------------------------------

    cursor.execute(
        """
        SELECT password
        FROM students
        WHERE id = ?
        """,
        (student_id,)
    )

    student = cursor.fetchone()


    # -----------------------------------------------------
    # STUDENT NOT FOUND
    # -----------------------------------------------------

    if not student:

        conn.close()

        session.clear()

        return redirect(
            url_for("login")
        )


    # -----------------------------------------------------
    # CHECK CURRENT PASSWORD
    # -----------------------------------------------------

    stored_password = student[0]


    if current_password != stored_password:

        conn.close()

        return render_template(
            "change_password.html",
            error="Current password is incorrect."
        )


    # -----------------------------------------------------
    # UPDATE PASSWORD
    # -----------------------------------------------------

    cursor.execute(
        """
        UPDATE students
        SET password = ?
        WHERE id = ?
        """,
        (
            new_password,
            student_id
        )
    )


    conn.commit()

    conn.close()


    # -----------------------------------------------------
    # STORE SUCCESS MESSAGE
    # -----------------------------------------------------

    session["password_changed"] = True


    # -----------------------------------------------------
    # RETURN TO DASHBOARD
    # -----------------------------------------------------

    return redirect(
        url_for("dashboard")
    )


# =========================================================
# CREATE ACCOUNT PAGE
# =========================================================

@app.route("/create-account")
def create_account():

    return render_template(
        "create_account.html"
    )


# =========================================================
# REGISTER / CREATE ACCOUNT
# =========================================================

@app.route("/register", methods=["POST"])
def register():

    name = request.form["name"].strip()

    email = request.form["email"].strip()

    password = request.form["password"]


    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()


    try:

        # Create new account
        cursor.execute(
            """
            INSERT INTO students
            (name, email, password)
            VALUES (?, ?, ?)
            """,
            (
                name,
                email,
                password
            )
        )


        conn.commit()


        # Get newly created student's ID
        student_id = cursor.lastrowid


        # Automatically log the new user in
        session["student_id"] = student_id

        session["student_name"] = name


        # Store success notification
        session["account_created"] = True


        # Go directly to dashboard
        return redirect(
            url_for("dashboard")
        )


    except sqlite3.IntegrityError:

        return "Email already registered!"


    finally:

        conn.close()


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    student_id = session.get("student_id")

    student_name = session.get("student_name")


    if not student_id:

        return redirect(
            url_for("home")
        )


    # =====================================================
    # CHECK NEW ACCOUNT NOTIFICATION
    # =====================================================

    account_created = session.pop(
        "account_created",
        False
    )


    # =====================================================
    # CHECK PASSWORD CHANGE NOTIFICATION
    # =====================================================

    password_changed = session.pop(
        "password_changed",
        False
    )


    # =====================================================
    # GET SELECTED SEMESTER
    # =====================================================

    semester = request.args.get(
        "semester",
        default=1,
        type=int
    )


    # =====================================================
    # PROTECT SEMESTER VALUE
    # =====================================================

    if semester < 1 or semester > 8:

        semester = 1


    # =====================================================
    # CONNECT DATABASE
    # =====================================================

    conn = sqlite3.connect("students.db")

    cursor = conn.cursor()


    # =====================================================
    # GET ACADEMIC DATA
    # =====================================================

    cursor.execute(
        """
        SELECT
            id,
            subject,
            marks,
            attendance
        FROM academic_data
        WHERE student_id = ?
        AND semester = ?
        ORDER BY id
        """,
        (
            student_id,
            semester
        )
    )


    academic_data = cursor.fetchall()

    conn.close()


    # =====================================================
    # AVERAGE MARKS
    # =====================================================

    if academic_data:

        total_marks = sum(
            row[2]
            for row in academic_data
        )

        average_marks = round(
            total_marks / len(academic_data)
        )

    else:

        average_marks = 0


    # =====================================================
    # ATTENDANCE
    # =====================================================

    if academic_data:

        total_attendance = sum(
            row[3]
            for row in academic_data
        )

        attendance = round(
            total_attendance / len(academic_data)
        )

    else:

        attendance = 0


    # =====================================================
    # OVERALL GRADE
    # =====================================================

    if average_marks >= 90:

        overall_grade = "A+"

    elif average_marks >= 80:

        overall_grade = "A"

    elif average_marks >= 70:

        overall_grade = "B+"

    elif average_marks >= 60:

        overall_grade = "B"

    elif average_marks >= 50:

        overall_grade = "C"

    else:

        overall_grade = "Needs Improvement"


    # =====================================================
    # AI ANALYSIS
    # =====================================================

    ai_result = analyze_student(
        student_id,
        semester
    )


    # =====================================================
    # SEND DATA TO DASHBOARD
    # =====================================================

    return render_template(
        "dashboard.html",

        name=student_name,

        academic_data=academic_data,

        average_marks=average_marks,

        attendance=attendance,

        overall_grade=overall_grade,

        ai_result=ai_result,

        semester=semester,

        account_created=account_created,

        password_changed=password_changed
    )


# =========================================================
# AI CHATBOT
# =========================================================

@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():

    student_id = session.get("student_id")

    student_name = session.get("student_name")


    if not student_id:

        return redirect(
            url_for("home")
        )


    # =====================================================
    # HANDLE CHAT MESSAGE
    # =====================================================

    if request.method == "POST":

        user_message = request.form.get(
            "message",
            ""
        ).strip()


        if not user_message:

            return jsonify({
                "response": "Please enter a question."
            })


        response = chatbot_response(
            student_id,
            user_message
        )


        return jsonify({
            "response": response
        })


    # =====================================================
    # OPEN CHATBOT PAGE
    # =====================================================

    return render_template(
        "chatbot.html",
        name=student_name
    )


# =========================================================
# ADD ACADEMIC DATA PAGE
# =========================================================

@app.route("/add-academic")
def add_academic():

    student_id = session.get("student_id")


    if not student_id:

        return redirect(
            url_for("home")
        )


    semester = request.args.get(
        "semester",
        default=1,
        type=int
    )


    return render_template(
        "add_academic.html",
        semester=semester
    )


# =========================================================
# ADD ACADEMIC DATA
# =========================================================

@app.route("/add-academic", methods=["POST"])
def add_academic_data():

    student_id = session.get("student_id")


    if not student_id:

        return redirect(
            url_for("home")
        )


    subject = request.form["subject"].strip()


    marks = int(
        request.form["marks"]
    )


    attendance = int(
        request.form["attendance"]
    )


    semester = int(
        request.form["semester"]
    )


    conn = sqlite3.connect("students.db")

    cursor = conn.cursor()


    # =====================================================
    # DUPLICATE SUBJECT PROTECTION
    # =====================================================

    cursor.execute(
        """
        SELECT id
        FROM academic_data
        WHERE student_id = ?
        AND semester = ?
        AND LOWER(TRIM(subject)) = LOWER(TRIM(?))
        """,
        (
            student_id,
            semester,
            subject
        )
    )


    existing_subject = cursor.fetchone()


    if existing_subject:

        conn.close()


        return render_template(
            "duplicate_subject.html",

            subject=subject,

            semester=semester
        )


    # =====================================================
    # INSERT DATA
    # =====================================================

    cursor.execute(
        """
        INSERT INTO academic_data
        (
            student_id,
            subject,
            marks,
            attendance,
            semester
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            student_id,
            subject,
            marks,
            attendance,
            semester
        )
    )


    conn.commit()

    conn.close()


    return redirect(
        url_for(
            "dashboard",
            semester=semester
        )
    )


# =========================================================
# EDIT ACADEMIC DATA PAGE
# =========================================================

@app.route("/edit-academic/<int:academic_id>")
def edit_academic(academic_id):

    student_id = session.get("student_id")


    if not student_id:

        return redirect(
            url_for("home")
        )


    conn = sqlite3.connect("students.db")

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            id,
            subject,
            marks,
            attendance,
            semester
        FROM academic_data
        WHERE id = ?
        AND student_id = ?
        """,
        (
            academic_id,
            student_id
        )
    )


    academic = cursor.fetchone()

    conn.close()


    if not academic:

        return "Academic record not found."


    return render_template(
        "edit_academic.html",
        academic=academic
    )


# =========================================================
# UPDATE ACADEMIC DATA
# =========================================================

@app.route(
    "/edit-academic/<int:academic_id>",
    methods=["POST"]
)
def update_academic(academic_id):

    student_id = session.get("student_id")


    if not student_id:

        return redirect(
            url_for("home")
        )


    subject = request.form["subject"].strip()


    marks = int(
        request.form["marks"]
    )


    attendance = int(
        request.form["attendance"]
    )


    semester = int(
        request.form["semester"]
    )


    conn = sqlite3.connect("students.db")

    cursor = conn.cursor()


    # =====================================================
    # DUPLICATE CHECK DURING EDIT
    # =====================================================

    cursor.execute(
        """
        SELECT id
        FROM academic_data
        WHERE student_id = ?
        AND semester = ?
        AND LOWER(TRIM(subject)) = LOWER(TRIM(?))
        AND id != ?
        """,
        (
            student_id,
            semester,
            subject,
            academic_id
        )
    )


    existing_subject = cursor.fetchone()


    if existing_subject:

        conn.close()


        return render_template(
            "duplicate_subject.html",

            subject=subject,

            semester=semester
        )


    # =====================================================
    # UPDATE RECORD
    # =====================================================

    cursor.execute(
        """
        UPDATE academic_data
        SET
            subject = ?,
            marks = ?,
            attendance = ?,
            semester = ?
        WHERE id = ?
        AND student_id = ?
        """,
        (
            subject,
            marks,
            attendance,
            semester,
            academic_id,
            student_id
        )
    )


    conn.commit()

    conn.close()


    return redirect(
        url_for(
            "dashboard",
            semester=semester
        )
    )


# =========================================================
# DELETE ACADEMIC DATA
# =========================================================

@app.route(
    "/delete-academic/<int:academic_id>",
    methods=["POST"]
)
def delete_academic(academic_id):

    student_id = session.get("student_id")


    if not student_id:

        return redirect(
            url_for("home")
        )


    conn = sqlite3.connect("students.db")

    cursor = conn.cursor()


    # =====================================================
    # GET SEMESTER FIRST
    # =====================================================

    cursor.execute(
        """
        SELECT semester
        FROM academic_data
        WHERE id = ?
        AND student_id = ?
        """,
        (
            academic_id,
            student_id
        )
    )


    record = cursor.fetchone()


    if not record:

        conn.close()

        return "Academic record not found."


    semester = record[0]


    # =====================================================
    # DELETE RECORD
    # =====================================================

    cursor.execute(
        """
        DELETE FROM academic_data
        WHERE id = ?
        AND student_id = ?
        """,
        (
            academic_id,
            student_id
        )
    )


    conn.commit()

    conn.close()


    return redirect(
        url_for(
            "dashboard",
            semester=semester
        )
    )


# =========================================================
# ATTENDANCE ANALYSIS PAGE
# =========================================================

@app.route("/attendance")
def attendance_analysis():

    student_id = session.get("student_id")


    if not student_id:

        return redirect(
            url_for("home")
        )


    semester = request.args.get(
        "semester",
        default=1,
        type=int
    )


    conn = sqlite3.connect("students.db")

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            id,
            subject,
            marks,
            attendance
        FROM academic_data
        WHERE student_id = ?
        AND semester = ?
        ORDER BY id
        """,
        (
            student_id,
            semester
        )
    )


    academic_data = cursor.fetchall()

    conn.close()


    # =====================================================
    # CALCULATE ATTENDANCE
    # =====================================================

    if academic_data:

        total_attendance = sum(
            row[3]
            for row in academic_data
        )

        attendance = round(
            total_attendance / len(academic_data)
        )

    else:

        attendance = 0


    return render_template(
        "attendance.html",

        academic_data=academic_data,

        attendance=attendance,

        semester=semester
    )


# =========================================================
# SUBJECT PERFORMANCE PAGE
# =========================================================

@app.route("/subject-performance")
def subject_performance():

    student_id = session.get("student_id")


    if not student_id:

        return redirect(
            url_for("home")
        )


    semester = request.args.get(
        "semester",
        default=1,
        type=int
    )


    conn = sqlite3.connect("students.db")

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            id,
            subject,
            marks,
            attendance
        FROM academic_data
        WHERE student_id = ?
        AND semester = ?
        ORDER BY id
        """,
        (
            student_id,
            semester
        )
    )


    academic_data = cursor.fetchall()

    conn.close()


    return render_template(
        "subject_performance.html",

        academic_data=academic_data,

        semester=semester
    )


# =========================================================
# GRADE OVERVIEW PAGE
# =========================================================

@app.route("/grade")
def grade_overview():

    student_id = session.get("student_id")


    if not student_id:

        return redirect(
            url_for("home")
        )


    semester = request.args.get(
        "semester",
        default=1,
        type=int
    )


    conn = sqlite3.connect("students.db")

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            id,
            subject,
            marks,
            attendance
        FROM academic_data
        WHERE student_id = ?
        AND semester = ?
        ORDER BY id
        """,
        (
            student_id,
            semester
        )
    )


    academic_data = cursor.fetchall()

    conn.close()


    # =====================================================
    # CALCULATE AVERAGE MARKS
    # =====================================================

    if academic_data:

        total_marks = sum(
            row[2]
            for row in academic_data
        )

        average_marks = round(
            total_marks / len(academic_data)
        )

    else:

        average_marks = 0


    # =====================================================
    # CALCULATE OVERALL GRADE
    # =====================================================

    if average_marks >= 90:

        overall_grade = "A+"

    elif average_marks >= 80:

        overall_grade = "A"

    elif average_marks >= 70:

        overall_grade = "B+"

    elif average_marks >= 60:

        overall_grade = "B"

    elif average_marks >= 50:

        overall_grade = "C"

    else:

        overall_grade = "Needs Improvement"


    return render_template(
        "grade.html",

        academic_data=academic_data,

        overall_grade=overall_grade,

        semester=semester
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()


    return redirect(
        url_for("home")
    )


# =========================================================
# RUN FLASK
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )