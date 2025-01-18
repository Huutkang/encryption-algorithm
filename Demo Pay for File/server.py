from flask import Flask
import webview
import threading
import os
import json
from datetime import datetime, timedelta

app = Flask(__name__)
TIME_FILE = "start_time.json"
HTML_FILE = "Demo Pay for File/index.html"
TOTAL_PAYMENT_DURATION = timedelta(days=1)  # Thời gian hết hạn thanh toán
TOTAL_FILE_DURATION = timedelta(days=3)  # Thời gian hết hạn file

# Lấy hoặc tạo thời gian bắt đầu
def get_or_create_start_time():
    if os.path.exists(TIME_FILE):
        with open(TIME_FILE, "r") as f:
            data = json.load(f)
            return datetime.fromisoformat(data["start_time"])
    else:
        start_time = datetime.now()
        with open(TIME_FILE, "w") as f:
            json.dump({"start_time": start_time.isoformat()}, f)
        return start_time

# Cập nhật thời gian trong file HTML
def update_html_with_time():
    start_time = get_or_create_start_time()
    payment_deadline = start_time + TOTAL_PAYMENT_DURATION
    file_deadline = start_time + TOTAL_FILE_DURATION
    payment_time_remaining = payment_deadline - datetime.now()
    file_time_remaining = file_deadline - datetime.now()
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Thay thế thời gian trong HTML
    html_content = html_content.replace(
        "5/16/2017 00:47:55", payment_deadline.strftime("%m/%d/%Y %H:%M:%S")
    )
    html_content = html_content.replace(
        "5/20/2017 00:47:55", file_deadline.strftime("%m/%d/%Y %H:%M:%S")
    )
    html_content = html_content.replace(
        "'time-left-payment', 24 * 60 * 60", f"'time-left-payment', {str(int(payment_time_remaining.total_seconds()))}")
    html_content = html_content.replace(
        "'time-left-files', 3 * 24 * 60 * 60", f"'time-left-files', {str(int(file_time_remaining.total_seconds()))}")

    return html_content

# Route chính hiển thị HTML
@app.route("/")
def index():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        return f.read()

# Chạy server Flask trong một luồng riêng
def run_flask():
    app.run(debug=False, port=5000)

if __name__ == "__main__":
    html_content = update_html_with_time()
    # Chạy Flask trong một luồng riêng
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Chạy pywebview
    webview.create_window("Payment Reminder", "http://127.0.0.1:5000", html_content, fullscreen=True)
    webview.start()
