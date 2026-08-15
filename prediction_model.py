"""
AI Student Success Platform
STEP 35.1 - ML Prediction Foundation

This module provides the foundation for the machine-learning
student performance prediction system.

IMPORTANT:
The current academic database contains marks and attendance,
but does not yet contain a genuine future-performance target.
Therefore, this step focuses on:

1. Loading academic data
2. Preparing ML features
3. Creating student-level feature summaries
4. Validating the available data
5. Providing a clean foundation for the actual trained model

The actual ML model will be introduced in the following steps
after we prepare appropriate training targets.
"""

import sqlite3
from pathlib import Path

import pandas as pd


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATABASE_PATH = BASE_DIR / "students.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_database_connection():
    """
    Create and return a connection to the SQLite database.
    """

    return sqlite3.connect(DATABASE_PATH)


# ============================================================
# LOAD ACADEMIC DATA
# ============================================================

def load_academic_data():
    """
    Load academic records from the students database.

    Returns:
        pandas.DataFrame

    Expected columns include:
        student_id
        semester
        subject
        marks
        attendance
    """

    connection = get_database_connection()

    try:

        query = """
            SELECT
                student_id,
                semester,
                subject,
                marks,
                attendance
            FROM academic_data
        """

        dataframe = pd.read_sql_query(
            query,
            connection
        )

        return dataframe

    finally:

        connection.close()


# ============================================================
# VALIDATE ACADEMIC DATA
# ============================================================

def validate_academic_data(dataframe):
    """
    Validate the academic dataset before using it for ML.

    Returns:
        dictionary containing validation information.
    """

    required_columns = [
        "student_id",
        "semester",
        "subject",
        "marks",
        "attendance"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:

        return {
            "valid": False,
            "message": "Required columns are missing.",
            "missing_columns": missing_columns
        }

    if dataframe.empty:

        return {
            "valid": False,
            "message": "No academic records are available.",
            "missing_columns": []
        }

    numeric_columns = [
        "marks",
        "attendance"
    ]

    for column in numeric_columns:

        dataframe[column] = pd.to_numeric(
            dataframe[column],
            errors="coerce"
        )

    invalid_marks = dataframe[
        dataframe["marks"].isna()
        | (dataframe["marks"] < 0)
        | (dataframe["marks"] > 100)
    ]

    invalid_attendance = dataframe[
        dataframe["attendance"].isna()
        | (dataframe["attendance"] < 0)
        | (dataframe["attendance"] > 100)
    ]

    return {
        "valid": (
            len(invalid_marks) == 0
            and len(invalid_attendance) == 0
        ),

        "message": "Academic data validation completed.",

        "missing_columns": [],

        "total_records": len(dataframe),

        "invalid_marks": len(invalid_marks),

        "invalid_attendance": len(invalid_attendance)
    }


# ============================================================
# CREATE STUDENT-LEVEL FEATURES
# ============================================================

def create_student_features(dataframe):
    """
    Convert subject-level academic records into
    student-level ML features.

    These features will eventually be used by the
    performance prediction model.

    Features currently generated:

        average_marks
        average_attendance
        highest_marks
        lowest_marks
        marks_std
        subject_count
        semester_count
    """

    if dataframe.empty:

        return pd.DataFrame()

    dataframe = dataframe.copy()

    dataframe["marks"] = pd.to_numeric(
        dataframe["marks"],
        errors="coerce"
    )

    dataframe["attendance"] = pd.to_numeric(
        dataframe["attendance"],
        errors="coerce"
    )

    dataframe = dataframe.dropna(
        subset=[
            "student_id",
            "marks",
            "attendance"
        ]
    )

    if dataframe.empty:

        return pd.DataFrame()

    student_features = (
        dataframe
        .groupby("student_id")
        .agg(
            average_marks=("marks", "mean"),

            average_attendance=(
                "attendance",
                "mean"
            ),

            highest_marks=(
                "marks",
                "max"
            ),

            lowest_marks=(
                "marks",
                "min"
            ),

            marks_std=(
                "marks",
                "std"
            ),

            subject_count=(
                "subject",
                "nunique"
            ),

            semester_count=(
                "semester",
                "nunique"
            )
        )
        .reset_index()
    )

    # If a student has only one academic record,
    # standard deviation is NaN. Replace it with 0.
    student_features["marks_std"] = (
        student_features["marks_std"]
        .fillna(0)
    )

    return student_features


# ============================================================
# CREATE SEMESTER-LEVEL FEATURES
# ============================================================

def create_semester_features(dataframe):
    """
    Create semester-level performance features.

    These features will become particularly important
    when we introduce historical performance trends.
    """

    if dataframe.empty:

        return pd.DataFrame()

    dataframe = dataframe.copy()

    dataframe["marks"] = pd.to_numeric(
        dataframe["marks"],
        errors="coerce"
    )

    dataframe["attendance"] = pd.to_numeric(
        dataframe["attendance"],
        errors="coerce"
    )

    dataframe = dataframe.dropna(
        subset=[
            "student_id",
            "semester",
            "marks",
            "attendance"
        ]
    )

    if dataframe.empty:

        return pd.DataFrame()

    semester_features = (
        dataframe
        .groupby(
            [
                "student_id",
                "semester"
            ]
        )
        .agg(
            semester_average_marks=(
                "marks",
                "mean"
            ),

            semester_average_attendance=(
                "attendance",
                "mean"
            ),

            semester_highest_marks=(
                "marks",
                "max"
            ),

            semester_lowest_marks=(
                "marks",
                "min"
            ),

            semester_subject_count=(
                "subject",
                "nunique"
            )
        )
        .reset_index()
    )

    return semester_features


# ============================================================
# CREATE PERFORMANCE TREND
# ============================================================

def create_performance_trend(dataframe):
    """
    Calculate semester-to-semester performance trends.

    This becomes important for future prediction because
    a student's improvement or decline is more informative
    than a single marks value.
    """

    semester_features = create_semester_features(
        dataframe
    )

    if semester_features.empty:

        return pd.DataFrame()

    semester_features = semester_features.sort_values(
        [
            "student_id",
            "semester"
        ]
    )

    semester_features["previous_semester_marks"] = (
        semester_features
        .groupby("student_id")[
            "semester_average_marks"
        ]
        .shift(1)
    )

    semester_features["marks_change"] = (
        semester_features[
            "semester_average_marks"
        ]
        -
        semester_features[
            "previous_semester_marks"
        ]
    )

    semester_features["marks_change"] = (
        semester_features["marks_change"]
        .fillna(0)
    )

    return semester_features


# ============================================================
# GET COMPLETE ML DATASET
# ============================================================

def prepare_ml_dataset():
    """
    Load and prepare the complete dataset that will
    eventually be supplied to the ML training pipeline.

    Returns:
        dictionary containing:

        raw_data
        student_features
        semester_features
        performance_trend
        validation
    """

    raw_data = load_academic_data()

    validation = validate_academic_data(
        raw_data
    )

    if not validation["valid"]:

        return {
            "raw_data": raw_data,
            "student_features": pd.DataFrame(),
            "semester_features": pd.DataFrame(),
            "performance_trend": pd.DataFrame(),
            "validation": validation
        }

    student_features = create_student_features(
        raw_data
    )

    semester_features = create_semester_features(
        raw_data
    )

    performance_trend = create_performance_trend(
        raw_data
    )

    return {
        "raw_data": raw_data,
        "student_features": student_features,
        "semester_features": semester_features,
        "performance_trend": performance_trend,
        "validation": validation
    }


# ============================================================
# STUDENT PREDICTION FEATURES
# ============================================================

def get_student_features(student_id):
    """
    Return ML features for a specific student.

    This function will later be used by Flask
    when the prediction model is integrated.
    """

    dataset = prepare_ml_dataset()

    student_features = dataset[
        "student_features"
    ]

    if student_features.empty:

        return None

    matching_student = student_features[
        student_features["student_id"].astype(str)
        == str(student_id)
    ]

    if matching_student.empty:

        return None

    return matching_student.iloc[0].to_dict()


# ============================================================
# FOUNDATION TEST
# ============================================================

def run_prediction_foundation_test():
    """
    Run a basic test of the ML foundation.

    This does NOT train a prediction model yet.
    """

    print("=" * 60)

    print(
        "AI STUDENT SUCCESS PLATFORM"
    )

    print(
        "STEP 35.1 - ML PREDICTION FOUNDATION"
    )

    print("=" * 60)

    print()

    print(
        "Database:",
        DATABASE_PATH
    )

    print()

    try:

        dataset = prepare_ml_dataset()

        validation = dataset["validation"]

        print(
            "Data validation:",
            validation["message"]
        )

        print(
            "Total academic records:",
            validation.get(
                "total_records",
                0
            )
        )

        print()

        if not validation["valid"]:

            print(
                "❌ Dataset validation failed."
            )

            print(
                validation
            )

            return

        student_features = (
            dataset["student_features"]
        )

        semester_features = (
            dataset["semester_features"]
        )

        performance_trend = (
            dataset["performance_trend"]
        )

        print(
            "Students available:",
            len(student_features)
        )

        print(
            "Semester records:",
            len(semester_features)
        )

        print(
            "Performance trend records:",
            len(performance_trend)
        )

        print()

        print(
            "Generated ML features:"
        )

        if not student_features.empty:

            feature_columns = [
                column
                for column in student_features.columns
                if column != "student_id"
            ]

            for feature in feature_columns:

                print(
                    "  ✓",
                    feature
                )

        print()

        print(
            "✅ STEP 35.1 foundation test completed."
        )

        print()

        print(
            "The actual trained ML prediction model"
        )

        print(
            "will be added in the next step after"
        )

        print(
            "we establish the correct prediction target."
        )

    except Exception as error:

        print()

        print(
            "❌ Prediction foundation test failed."
        )

        print(
            "Error:",
            error
        )


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":

    run_prediction_foundation_test()