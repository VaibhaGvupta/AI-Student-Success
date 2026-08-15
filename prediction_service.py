"""
AI Student Success Platform
STEP 35.3
Student Performance Prediction Service

This module:

1. Loads the trained ML model
2. Loads the model feature configuration
3. Gets a student's semester-level academic features
4. Generates a predicted performance score
5. Calculates an understandable risk level
"""

import os
import pickle

from prediction_model import prepare_ml_dataset


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_FILE = os.path.join(
    "models",
    "student_performance_model.pkl"
)

FEATURE_FILE = os.path.join(
    "models",
    "model_features.pkl"
)


# ============================================================
# LOAD MODEL
# ============================================================

def load_prediction_model():

    if not os.path.exists(MODEL_FILE):

        raise FileNotFoundError(
            f"Prediction model not found: {MODEL_FILE}"
        )

    with open(
        MODEL_FILE,
        "rb"
    ) as file:

        model = pickle.load(file)

    return model


# ============================================================
# LOAD FEATURE NAMES
# ============================================================

def load_model_features():

    if not os.path.exists(FEATURE_FILE):

        raise FileNotFoundError(
            f"Model feature file not found: {FEATURE_FILE}"
        )

    with open(
        FEATURE_FILE,
        "rb"
    ) as file:

        features = pickle.load(file)

    return features


# ============================================================
# GET STUDENT SEMESTER DATA
# ============================================================

def get_student_semester_data(student_id):

    dataset = prepare_ml_dataset()

    if not isinstance(dataset, dict):

        raise ValueError(
            "Unexpected ML dataset format."
        )

    semester_features = dataset.get(
        "semester_features"
    )

    if semester_features is None:

        raise ValueError(
            "Semester features are not available."
        )

    student_data = semester_features[
        semester_features["student_id"] == student_id
    ]

    if student_data.empty:

        raise ValueError(
            f"No academic semester data found "
            f"for student {student_id}."
        )

    return student_data


# ============================================================
# CALCULATE RISK LEVEL
# ============================================================

def calculate_risk_level(predicted_marks):

    if predicted_marks >= 75:

        return "LOW"

    if predicted_marks >= 50:

        return "MEDIUM"

    return "HIGH"


# ============================================================
# GENERATE PREDICTION
# ============================================================

def predict_student_performance(student_id):

    # --------------------------------------------------------
    # Load model
    # --------------------------------------------------------

    model = load_prediction_model()

    # --------------------------------------------------------
    # Load feature configuration
    # --------------------------------------------------------

    feature_columns = load_model_features()

    # --------------------------------------------------------
    # Get student's semester data
    # --------------------------------------------------------

    student_data = get_student_semester_data(
        student_id
    )

    # --------------------------------------------------------
    # Select the latest semester
    # --------------------------------------------------------

    latest_semester = student_data.sort_values(
        "semester"
    ).iloc[-1]

    # --------------------------------------------------------
    # Build model input
    # --------------------------------------------------------

    input_data = {}

    for feature in feature_columns:

        if feature not in latest_semester:

            raise ValueError(
                f"Required feature '{feature}' "
                f"not found in semester data."
            )

        input_data[feature] = float(
            latest_semester[feature]
        )

    # --------------------------------------------------------
    # Generate prediction
    # --------------------------------------------------------
    #
    # Use a pandas DataFrame so the feature names match
    # the names used when the Random Forest was trained.
    # --------------------------------------------------------

    import pandas as pd

    prediction_input = pd.DataFrame(
        [input_data],
        columns=feature_columns
    )

    predicted_marks = model.predict(
        prediction_input
    )[0]

    # --------------------------------------------------------
    # Keep prediction within valid marks range
    # --------------------------------------------------------

    predicted_marks = max(
        0,
        min(
            100,
            predicted_marks
        )
    )

    predicted_marks = round(
        float(predicted_marks),
        2
    )

    # --------------------------------------------------------
    # Calculate risk
    # --------------------------------------------------------

    risk_level = calculate_risk_level(
        predicted_marks
    )

    # --------------------------------------------------------
    # Return prediction result
    # --------------------------------------------------------

    result = {

        "student_id": int(student_id),

        "semester": int(
            latest_semester["semester"]
        ),

        "predicted_performance": predicted_marks,

        "risk_level": risk_level,

        "average_attendance": round(
            float(
                latest_semester[
                    "semester_average_attendance"
                ]
            ),
            2
        ),

        "highest_marks": round(
            float(
                latest_semester[
                    "semester_highest_marks"
                ]
            ),
            2
        ),

        "lowest_marks": round(
            float(
                latest_semester[
                    "semester_lowest_marks"
                ]
            ),
            2
        ),

        "subject_count": int(
            latest_semester[
                "semester_subject_count"
            ]
        )
    }

    return result


# ============================================================
# FOUNDATION TEST
# ============================================================

def run_prediction_test():

    print()
    print("=" * 60)
    print("AI STUDENT SUCCESS PLATFORM")
    print("STEP 35.3 - PREDICTION SERVICE TEST")
    print("=" * 60)
    print()

    student_id = 1

    print(
        f"Generating prediction for student {student_id}..."
    )

    result = predict_student_performance(
        student_id
    )

    print()

    print("Prediction result:")

    print(
        f"✓ Student ID: "
        f"{result['student_id']}"
    )

    print(
        f"✓ Latest semester: "
        f"{result['semester']}"
    )

    print(
        f"✓ Predicted performance: "
        f"{result['predicted_performance']}%"
    )

    print(
        f"✓ Risk level: "
        f"{result['risk_level']}"
    )

    print(
        f"✓ Average attendance: "
        f"{result['average_attendance']}%"
    )

    print(
        f"✓ Highest marks: "
        f"{result['highest_marks']}"
    )

    print(
        f"✓ Lowest marks: "
        f"{result['lowest_marks']}"
    )

    print(
        f"✓ Subject count: "
        f"{result['subject_count']}"
    )

    print()

    print("=" * 60)
    print(
        "✅ STEP 35.3 PREDICTION TEST COMPLETED"
    )
    print("=" * 60)
    print()


# ============================================================
# RUN TEST
# ============================================================

if __name__ == "__main__":

    run_prediction_test()