# AccuKnox AI/ML Trainee Technical Assignment

This workspace contains the complete implementation and interview preparation guide for the **AccuKnox AI/ML Trainee Technical Assignment**.

All scripts are written using clean Python 3, adhering strictly to production-level engineering practices: parameterized SQL queries, error handling, statistical metrics, and non-blocking backends.

---

## 📂 Project Structure

```text
assignment/
├── problem1_q1_books.py           # Problem 1.1: REST API -> SQLite -> Display Table
├── problem1_q2_student_scores.py  # Problem 1.2: API -> Score Averages -> Bar Chart
├── problem1_q3_csv_to_sqlite.py   # Problem 1.3: CSV -> SQLite with Upsert Idempotency
├── complex_python_sample.py       # Problem 1.4: Showcase Asynchronous Embedding Pipeline
├── complex_database_sample.sql    # Problem 1.5: Showcase Advanced SQL Schema & Analytics
├── users.csv                      # Dataset for Problem 1.3
├── books.db                       # Generated SQLite database for 1.1
├── users.db                       # Generated SQLite database for 1.3
├── student_scores_bar_chart.png   # Generated visualization for 1.2
├── assignment_submission_guide.md # Comprehensive solutions, architecture & interview guide
└── README.md                      # Quickstart and overview
```

---

## 🚀 Quick Execution Guide

### 1. Problem 1, Question 1: Books API & SQLite
Fetches book records from the Open Library REST API, saves them into SQLite with parameterized queries, and prints a formatted table.
```bash
python problem1_q1_books.py
```

### 2. Problem 1, Question 2: Student Scores & Bar Chart
Fetches student scores from a REST API endpoint, calculates the class average (82.20), median, and range, and creates a customized bar chart (`student_scores_bar_chart.png`).
```bash
python problem1_q2_student_scores.py
```

### 3. Problem 1, Question 3: CSV to SQLite
Reads and validates user records from `users.csv`, inserts/updates them into `users.db` using SQLite UPSERT logic, and confirms data integrity.
```bash
python problem1_q3_csv_to_sqlite.py
```

### 4. Problem 1, Question 4: Complex Python Showcase
Demonstrates asynchronous concurrency with `asyncio`, token chunking, and batch embedding vectorization.
```bash
python complex_python_sample.py
```

---

## 📖 Complete Written Responses & Interview Preparation

All theoretical answers, system architecture diagrams, vector database comparisons, self-ratings, and mock interview questions are organized in:
👉 **[`assignment_submission_guide.md`](assignment_submission_guide.md)**
