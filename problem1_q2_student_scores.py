import sys
import json
import statistics
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

MOCK_STUDENTS = [
    {"student_id": 101, "name": "Aarav Sharma", "score": 88},
    {"student_id": 102, "name": "Bhavna Patel", "score": 94},
    {"student_id": 103, "name": "Chetan Verma", "score": 72},
    {"student_id": 104, "name": "Divya Nair", "score": 85},
    {"student_id": 105, "name": "Eshan Gupta", "score": 64},
    {"student_id": 106, "name": "Farhan Ali", "score": 91},
    {"student_id": 107, "name": "Geeta Rao", "score": 79},
    {"student_id": 108, "name": "Harsh Singh", "score": 83},
    {"student_id": 109, "name": "Ishita Roy", "score": 96},
    {"student_id": 110, "name": "Jayant Kulkarni", "score": 70}
]

PORT = 8765
LOCAL_API_URL = f"http://127.0.0.1:{PORT}/api/students/scores"
OUTPUT_CHART_FILE = "student_scores_bar_chart.png"

class MockStudentAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/students/scores":
            payload = json.dumps({"status": "success", "data": MOCK_STUDENTS}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return

def start_local_mock_server() -> HTTPServer:
    server = HTTPServer(("127.0.0.1", PORT), MockStudentAPIHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    return server

def fetch_student_scores(api_url: str = LOCAL_API_URL) -> list[dict]:
    print(f"[INFO] Fetching student test-score data from: {api_url}")
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if isinstance(result, dict) and "data" in result:
            students = result["data"]
        elif isinstance(result, list):
            students = result
        else:
            students = []

        print(f"[SUCCESS] Successfully fetched scores for {len(students)} students.")
        return students

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch data from API: {e}", file=sys.stderr)
        return []

def calculate_metrics(students: list[dict]) -> dict:
    if not students:
        raise ValueError("Cannot calculate metrics on an empty student list.")

    scores = [s["score"] for s in students]
    avg_score = statistics.mean(scores)
    med_score = statistics.median(scores)
    highest = max(scores)
    lowest = min(scores)

    return {
        "average": avg_score,
        "median": med_score,
        "highest": highest,
        "lowest": lowest,
        "total_students": len(scores)
    }

def create_and_save_bar_chart(students: list[dict], avg_score: float, output_path: str = OUTPUT_CHART_FILE) -> None:
    names = [s["name"] for s in students]
    scores = [s["score"] for s in students]

    plt.figure(figsize=(11, 6))

    bar_colors = ["#2b8a3e" if score >= avg_score else "#d97706" for score in scores]
    bars = plt.bar(names, scores, color=bar_colors, width=0.6, edgecolor="#333333", linewidth=0.8)

    plt.axhline(
        y=avg_score,
        color="#dc2626",
        linestyle="--",
        linewidth=2,
        label=f"Class Average ({avg_score:.2f})"
    )

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 1.2,
            f"{int(height)}",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold"
        )

    plt.title("Student Test-Score Performance Analysis", fontsize=15, fontweight="bold", pad=15)
    plt.xlabel("Student Name", fontsize=12, labelpad=10)
    plt.ylabel("Test Score (out of 100)", fontsize=12, labelpad=10)
    plt.ylim(0, 110)
    plt.xticks(rotation=30, ha="right", fontsize=10)
    plt.grid(axis="y", linestyle=":", alpha=0.6)
    plt.legend(loc="upper right", framealpha=0.9)
    plt.tight_layout()

    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[SUCCESS] Bar chart saved to '{output_path}'.")

def main():
    print("--- Problem 1, Question 2: Student Test Scores & Visualization ---")
    server = start_local_mock_server()
    print(f"[INFO] Mock REST API running at {LOCAL_API_URL}")

    try:
        students = fetch_student_scores(LOCAL_API_URL)
        if not students:
            print("[FAIL] No student data found.")
            return

        metrics = calculate_metrics(students)
        print("\n" + "=" * 45)
        print("          SCORE SUMMARY METRICS           ")
        print("=" * 45)
        print(f" Total Students Tested : {metrics['total_students']}")
        print(f" Average Score         : {metrics['average']:.2f}")
        print(f" Median Score          : {metrics['median']:.2f}")
        print(f" Highest Score         : {metrics['highest']}")
        print(f" Lowest Score          : {metrics['lowest']}")
        print("=" * 45 + "\n")

        create_and_save_bar_chart(students, metrics["average"], OUTPUT_CHART_FILE)

    finally:
        server.shutdown()
        server.server_close()

if __name__ == "__main__":
    main()
