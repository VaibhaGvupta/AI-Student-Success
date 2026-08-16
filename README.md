# 🎓 AI Student Success Platform

An AI-assisted student performance tracking platform built with **Flask**. Students can log in, record their academic marks and attendance, view AI-generated performance analysis, chat with a rule-based academic assistant, and get **machine-learning predictions** of future performance using a trained Random Forest model.

---

## 🌐 Live Demo

👉 **[https://ai-student-success.onrender.com/](https://ai-student-success.onrender.com/)**

> ⏳ Hosted on Render's free tier — the app may take 30–60 seconds to wake up on the first request if it has been idle.

---

## ✨ Features

- 🔐 **Student authentication** — account creation, login, forgot/change password
- 📊 **Dashboard** — semester-wise overview of marks, attendance, and grades
- 🧠 **AI Analysis** — automatic detection of strongest/weakest subjects, performance level, and personalized study recommendations
- 💬 **Chatbot assistant** — answers questions about a student's marks, attendance, grades, and study advice
- 📈 **ML Performance Prediction** — a trained `RandomForestRegressor` model predicts future academic performance and risk level from semester-level features
- 📝 **Academic record management** — add/edit subject marks and attendance per semester
- 🏫 **Grade & attendance reports** — dedicated views for grades, attendance, and subject-wise performance

---

## 🛠️ Tech Stack

| Layer          | Technology                          |
|----------------|--------------------------------------|
| Backend        | Python, Flask                        |
| Database       | SQLite                               |
| Machine Learning | scikit-learn (Random Forest), pandas, numpy |
| Frontend       | HTML, Jinja2 templates               |
| Server (prod)  | Gunicorn                             |

---

## 📁 Project Structure

```
AI_Student_Success/
├── app.py                      # Main Flask application & routes
├── ai_analysis.py              # Rule-based AI academic analysis engine
├── chatbot.py                  # Rule-based chatbot logic
├── prediction_model.py         # ML data loading & feature preparation
├── prediction_service.py       # Loads trained model & serves predictions
├── train_prediction_model.py   # Trains the Random Forest prediction model
├── init_db.py                  # Initializes the SQLite database schema
├── add_data.py                 # Utility script to seed sample data
├── update_db.py                # Database migration/update helper
├── models/
│   ├── student_performance_model.pkl  # Trained ML model
│   └── model_features.pkl             # Feature names used by the model
├── templates/                  # Jinja2 HTML templates
│   ├── index.html
│   ├── login.html
│   ├── create_account.html
│   ├── dashboard.html
│   ├── chatbot.html
│   ├── add_academic.html
│   ├── edit_academic.html
│   ├── attendance.html
│   ├── grade.html
│   ├── subject_performance.html
│   └── ...
├── students.db                 # SQLite database
└── requirements.txt             # Python dependencies
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/VaibhaGvupta/AI-Student-Success.git
   cd AI-Student-Success
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python init_db.py
   ```

5. **(Optional) Train the prediction model**
   ```bash
   python train_prediction_model.py
   ```
   > A pre-trained model is already included under `models/`, so this step is only needed if you want to retrain it on new data.

6. **Run the application**
   ```bash
   python app.py
   ```

7. Open your browser and go to:
   ```
   http://127.0.0.1:5000
   ```

---

## 🗄️ Database Schema

**`students`**
| Column   | Type    | Notes                |
|----------|---------|-----------------------|
| id       | INTEGER | Primary key            |
| name     | TEXT    | Student's name         |
| email    | TEXT    | Unique login identifier|
| password | TEXT    | Login password          |

**`academic_data`**
| Column     | Type    | Notes                          |
|------------|---------|----------------------------------|
| id         | INTEGER | Primary key                     |
| student_id | INTEGER | Foreign key → `students.id`     |
| semester   | INTEGER | Semester number                 |
| subject    | TEXT    | Subject name                    |
| marks      | INTEGER | Marks obtained                  |
| attendance | INTEGER | Attendance percentage           |

---

## 🤖 How the AI Features Work

- **AI Analysis (`ai_analysis.py`)** — computes a student's average marks, strongest/weakest subject, attendance status, and generates a study recommendation and goal message per semester.
- **Chatbot (`chatbot.py`)** — a keyword-driven assistant that recognizes intents such as *performance*, *marks*, *attendance*, *strongest/weakest subject*, *grades*, and *study advice*, then responds using the student's real academic data pulled from the database.
- **Prediction Model (`prediction_model.py` → `train_prediction_model.py` → `prediction_service.py`)** — aggregates semester-level marks/attendance into ML features, trains a `RandomForestRegressor` to predict future performance, and serves predictions with an associated risk level at runtime.

---

## 📦 Deployment

The project includes `gunicorn` in `requirements.txt`, making it ready for deployment on platforms like **Render**, **Railway**, or **Heroku**:

```bash
gunicorn app:app
```

---

## 📌 Notes

- `students.db` is included for convenience/demo purposes. For a fresh setup, delete it and re-run `init_db.py`.
- Passwords are currently stored in plain text in the database — **not suitable for production** without adding hashing (e.g. `werkzeug.security.generate_password_hash`).
- `app.secret_key` should be moved to an environment variable before deploying publicly.

---

## 📄 License

This project currently has no license specified. Add a `LICENSE` file (e.g. MIT) if you intend to make usage terms explicit.

---

## 🙋 Author

Built by [VaibhaGvupta](https://github.com/VaibhaGvupta)
