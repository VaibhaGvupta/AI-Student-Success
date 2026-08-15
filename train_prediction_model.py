"""
AI Student Success Platform
STEP 35.2
Student Performance Prediction Model Training

This script:

1. Loads the ML dataset from prediction_model.py
2. Uses semester-level academic data
3. Prepares ML training features
4. Trains a Random Forest regression model
5. Saves the trained model
6. Saves the feature names
"""

import os
import pickle

from sklearn.ensemble import RandomForestRegressor

from prediction_model import prepare_ml_dataset


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_DIR = "models"

MODEL_FILE = os.path.join(
    MODEL_DIR,
    "student_performance_model.pkl"
)

FEATURE_FILE = os.path.join(
    MODEL_DIR,
    "model_features.pkl"
)


# ============================================================
# TRAINING FUNCTION
# ============================================================

def train_prediction_model():

    print()
    print("=" * 60)
    print("AI STUDENT SUCCESS PLATFORM")
    print("STEP 35.2 - MODEL TRAINING")
    print("=" * 60)
    print()

    # --------------------------------------------------------
    # Generate ML dataset
    # --------------------------------------------------------

    print("Generating ML dataset...")

    dataset = prepare_ml_dataset()

    if not isinstance(dataset, dict):

        print("❌ Unexpected ML dataset format.")

        return False

    # --------------------------------------------------------
    # Check validation
    # --------------------------------------------------------

    validation = dataset.get(
        "validation",
        {}
    )

    if not validation.get(
        "valid",
        False
    ):

        print("❌ Academic data validation failed.")

        print(
            validation.get(
                "message",
                "Unknown validation error."
            )
        )

        return False

    print(
        "✓ Academic data validation passed."
    )

    print()

    # --------------------------------------------------------
    # Get semester features
    # --------------------------------------------------------

    semester_features = dataset.get(
        "semester_features"
    )

    if semester_features is None:

        print(
            "❌ Semester features were not generated."
        )

        return False

    if semester_features.empty:

        print(
            "❌ No semester training data available."
        )

        return False

    print(
        f"✓ Training records available: "
        f"{len(semester_features)}"
    )

    print()

    # --------------------------------------------------------
    # Display available columns
    # --------------------------------------------------------

    print("Available semester ML columns:")

    for column in semester_features.columns:

        print(f"✓ {column}")

    print()

    # --------------------------------------------------------
    # Target column
    # --------------------------------------------------------
    #
    # The model predicts semester average marks.
    # --------------------------------------------------------

    target_column = "semester_average_marks"

    if target_column not in semester_features.columns:

        print(
            f"❌ Target column "
            f"'{target_column}' was not found."
        )

        return False

    # --------------------------------------------------------
    # Select model features
    # --------------------------------------------------------
    #
    # We intentionally exclude:
    #
    # student_id
    # semester
    # semester_average_marks
    #
    # student_id and semester are identifiers rather
    # than meaningful performance measurements.
    # --------------------------------------------------------

    feature_columns = [
        "semester_average_attendance",
        "semester_highest_marks",
        "semester_lowest_marks",
        "semester_subject_count"
    ]

    # --------------------------------------------------------
    # Check feature availability
    # --------------------------------------------------------

    missing_features = [
        column
        for column in feature_columns
        if column not in semester_features.columns
    ]

    if missing_features:

        print(
            "❌ Missing required model features:"
        )

        for column in missing_features:

            print(f"❌ {column}")

        return False

    # --------------------------------------------------------
    # Prepare X and y
    # --------------------------------------------------------

    X = semester_features[
        feature_columns
    ].copy()

    y = semester_features[
        target_column
    ].copy()

    print(
        "Preparing training data..."
    )

    print(
        f"✓ Training samples: {len(X)}"
    )

    print(
        f"✓ Input features: {len(feature_columns)}"
    )

    print()

    print("Final model features:")

    for column in feature_columns:

        print(f"✓ {column}")

    print()

    # --------------------------------------------------------
    # Check for missing values
    # --------------------------------------------------------

    if X.isnull().any().any():

        print(
            "⚠ Missing values detected."
        )

        X = X.fillna(
            X.mean(numeric_only=True)
        )

    if y.isnull().any():

        print(
            "❌ Target contains missing values."
        )

        return False

    # --------------------------------------------------------
    # Train Random Forest
    # --------------------------------------------------------

    print(
        "Training Random Forest model..."
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        max_depth=10
    )

    model.fit(
        X,
        y
    )

    print(
        "✓ Model training completed."
    )

    print()

    # --------------------------------------------------------
    # Create model directory
    # --------------------------------------------------------

    os.makedirs(
        MODEL_DIR,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Save model
    # --------------------------------------------------------

    with open(
        MODEL_FILE,
        "wb"
    ) as file:

        pickle.dump(
            model,
            file
        )

    print(
        f"✓ Model saved to: {MODEL_FILE}"
    )

    # --------------------------------------------------------
    # Save feature names
    # --------------------------------------------------------

    with open(
        FEATURE_FILE,
        "wb"
    ) as file:

        pickle.dump(
            feature_columns,
            file
        )

    print(
        f"✓ Feature list saved to: {FEATURE_FILE}"
    )

    # --------------------------------------------------------
    # Model information
    # --------------------------------------------------------

    print()

    print("Model information:")

    print(
        "✓ Algorithm: Random Forest Regressor"
    )

    print(
        f"✓ Number of trees: "
        f"{len(model.estimators_)}"
    )

    print(
        f"✓ Number of features: "
        f"{len(feature_columns)}"
    )

    print(
        f"✓ Training samples: "
        f"{len(X)}"
    )

    print()

    # --------------------------------------------------------
    # Feature importance
    # --------------------------------------------------------

    print(
        "Feature importance:"
    )

    importance_data = sorted(
        zip(
            feature_columns,
            model.feature_importances_
        ),
        key=lambda item: item[1],
        reverse=True
    )

    for feature, importance in importance_data:

        print(
            f"✓ {feature}: "
            f"{importance:.4f}"
        )

    print()

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    print("=" * 60)
    print(
        "✅ STEP 35.2 MODEL TRAINING COMPLETED"
    )
    print("=" * 60)
    print()

    return True


# ============================================================
# RUN SCRIPT
# ============================================================

if __name__ == "__main__":

    train_prediction_model()