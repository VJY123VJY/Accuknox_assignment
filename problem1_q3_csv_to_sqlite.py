import csv
import sqlite3
import os
import sys

CSV_FILE_PATH = "users.csv"
DB_FILE_PATH = "users.db"

def read_users_from_csv(csv_path: str = CSV_FILE_PATH) -> list[dict]:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found at: {csv_path}")

    users = []
    required_fields = {"user_id", "full_name", "email", "role", "department", "joined_date"}

    print(f"[INFO] Reading user records from CSV: {csv_path}")
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        
        if not required_fields.issubset(set(reader.fieldnames or [])):
            missing = required_fields - set(reader.fieldnames or [])
            raise ValueError(f"Missing required CSV columns: {missing}")

        for row_num, row in enumerate(reader, start=2):
            if not row["user_id"] or not row["email"] or not row["full_name"]:
                print(f"[WARNING] Skipping row {row_num}: Missing primary identification data.")
                continue

            users.append({
                "user_id": int(row["user_id"].strip()),
                "full_name": row["full_name"].strip(),
                "email": row["email"].strip().lower(),
                "role": row["role"].strip(),
                "department": row["department"].strip(),
                "joined_date": row["joined_date"].strip()
            })

    print(f"[SUCCESS] Parsed and validated {len(users)} user records from CSV.")
    return users

def store_users_in_sqlite(users: list[dict], db_path: str = DB_FILE_PATH) -> int:
    if not users:
        print("[WARNING] No user data provided for insertion.")
        return 0

    inserted_count = 0
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    full_name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    role TEXT NOT NULL,
                    department TEXT NOT NULL,
                    joined_date TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            upsert_query = """
                INSERT INTO users (user_id, full_name, email, role, department, joined_date)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    full_name = excluded.full_name,
                    email = excluded.email,
                    role = excluded.role,
                    department = excluded.department,
                    joined_date = excluded.joined_date;
            """

            records = [
                (
                    u["user_id"],
                    u["full_name"],
                    u["email"],
                    u["role"],
                    u["department"],
                    u["joined_date"]
                )
                for u in users
            ]

            cursor.executemany(upsert_query, records)
            conn.commit()
            inserted_count = len(records)
            print(f"[SUCCESS] Successfully inserted/updated {inserted_count} records into '{db_path}'.")

    except sqlite3.Error as e:
        print(f"[ERROR] Database error during insertion: {e}", file=sys.stderr)

    return inserted_count

def verify_and_display_users(db_path: str = DB_FILE_PATH) -> None:
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, full_name, email, role, department, joined_date FROM users ORDER BY user_id ASC;")
            rows = cursor.fetchall()

            if not rows:
                print("[INFO] No records found in the database.")
                return

            print("\n" + "=" * 95)
            print(f"{'USER ID':<8} | {'FULL NAME':<18} | {'EMAIL':<28} | {'ROLE':<18} | {'DEPT':<14}")
            print("-" * 95)
            
            for row in rows:
                uid, name, email, role, dept, _ = row
                print(f"{uid:<8} | {name:<18} | {email:<28} | {role:<18} | {dept:<14}")

            print("=" * 95 + "\n")

    except sqlite3.Error as e:
        print(f"[ERROR] Failed to query database: {e}", file=sys.stderr)

def main():
    print("--- Problem 1, Question 3: CSV to SQLite ETL Pipeline ---")
    users = read_users_from_csv(CSV_FILE_PATH)
    if users:
        store_users_in_sqlite(users, DB_FILE_PATH)
        verify_and_display_users(DB_FILE_PATH)

if __name__ == "__main__":
    main()
