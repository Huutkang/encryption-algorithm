import hashlib
import os

class PasswordManager:
    def __init__(self):
        # self.salt = os.urandom(16)  # Tạo salt ngẫu nhiên để tăng độ bảo mật
        self.salt = b'\xd2\x9e\x88\xc5\x11\x1a\x07\xb6\xb3\xa5%\xd2}K\xc9I'

    def hash_password(self, password: str) -> str:
        """
        Hàm băm mật khẩu bằng SHA-256 với salt.
        """
        password_bytes = password.encode('utf-8')  # Chuyển mật khẩu sang dạng bytes
        salted_password = self.salt + password_bytes  # Ghép salt và mật khẩu
        hashed_password = hashlib.sha256(salted_password).hexdigest()  # Băm bằng SHA-256
        return hashed_password

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Kiểm tra mật khẩu đã nhập có khớp với mật khẩu đã băm không.
        """
        password_bytes = password.encode('utf-8')
        salted_password = self.salt + password_bytes
        return hashlib.sha256(salted_password).hexdigest() == hashed_password

    def save_hashed_password(self, hashed_password: str, filename: str = "ứng dụng/hashed_password.txt"):
        """
        Ghi mật khẩu đã băm vào file.
        """
        with open(filename, "w") as file:
            file.write(hashed_password)

    def read_hashed_password(self, filename: str = "ứng dụng/hashed_password.txt") -> str:
        """
        Đọc mật khẩu đã băm từ file.
        """
        with open(filename, "r") as file:
            return file.read()

