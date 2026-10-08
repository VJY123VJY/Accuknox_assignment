import sqlite3
import requests
import sys

API_URL = "https://openlibrary.org/search.json"
DEFAULT_QUERY = "machine learning"
LIMIT = 10
DB_FILE = "books.db"

def fetch_books_from_api(query: str = DEFAULT_QUERY, limit: int = LIMIT) -> list[dict]:
    params = {
        "q": query,
        "limit": limit
    }
    
    print(f"[INFO] Fetching books matching '{query}' from Open Library API...")
    try:
        response = requests.get(API_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        books = []
        for doc in data.get("docs", []):
            title = doc.get("title", "Unknown Title")
            authors = doc.get("author_name", ["Unknown Author"])
            author_str = ", ".join(authors) if isinstance(authors, list) else str(authors)
            publish_year = doc.get("first_publish_year", None)
            isbn_list = doc.get("isbn", [])
            isbn = isbn_list[0] if isbn_list else "N/A"

            books.append({
                "title": title,
                "author": author_str,
                "publish_year": publish_year,
                "isbn": isbn
            })
            
        print(f"[SUCCESS] Successfully retrieved {len(books)} books from API.")
        return books

    except requests.exceptions.Timeout:
        print("[ERROR] The request to Open Library API timed out.", file=sys.stderr)
        return []
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch data from API: {e}", file=sys.stderr)
        return []

def store_books_in_sqlite(books: list[dict], db_path: str = DB_FILE) -> None:
    if not books:
        print("[WARNING] No books to insert into database.")
        return

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    publish_year INTEGER,
                    isbn TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            insert_query = """
                INSERT INTO books (title, author, publish_year, isbn)
                VALUES (?, ?, ?, ?);
            """
            
            records = [
                (b["title"], b["author"], b["publish_year"], b["isbn"])
                for b in books
            ]
            
            cursor.executemany(insert_query, records)
            conn.commit()
            print(f"[SUCCESS] Stored {len(records)} records in SQLite database '{db_path}'.")

    except sqlite3.Error as e:
        print(f"[ERROR] Database error occurred: {e}", file=sys.stderr)

def display_retrieved_books(db_path: str = DB_FILE) -> None:
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, author, publish_year, isbn FROM books ORDER BY id DESC LIMIT 10;")
            rows = cursor.fetchall()

            if not rows:
                print("[INFO] No books found in the database.")
                return

            print("\n" + "=" * 90)
            print(f"{'ID':<4} | {'TITLE':<38} | {'AUTHOR':<24} | {'YEAR':<6} | {'ISBN':<12}")
            print("-" * 90)
            
            for row in rows:
                book_id, title, author, year, isbn = row
                disp_title = (title[:35] + "..") if len(title) > 38 else title
                disp_author = (author[:21] + "..") if len(author) > 24 else author
                disp_year = str(year) if year is not None else "N/A"
                disp_isbn = str(isbn)[:12]
                
                print(f"{book_id:<4} | {disp_title:<38} | {disp_author:<24} | {disp_year:<6} | {disp_isbn:<12}")
            
            print("=" * 90 + "\n")

    except sqlite3.Error as e:
        print(f"[ERROR] Failed to read from database: {e}", file=sys.stderr)

def main():
    print("--- Problem 1: Book API Ingestion & SQLite Storage ---")
    books = fetch_books_from_api(query="artificial intelligence", limit=8)
    if books:
        store_books_in_sqlite(books)
        display_retrieved_books()
    else:
        print("[FAIL] Unable to proceed due to API fetch failure.")

if __name__ == "__main__":
    main()
