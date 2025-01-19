import os
import uuid
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

class RandomFileGenerator:
    def __init__(self, filename="id.txt"):
        self.filename = filename
        self.key_length = 32  # Độ dài ID và chuỗi ngẫu nhiên
        self.private_key, self.public_key = self.generate_keys()

    def generate_keys(self):
        """
        Tạo cặp khóa RSA.
        """
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()
        return private_key, public_key

    def save_keys(self, private_key_file: str, public_key_file: str):
        """
        Lưu khóa RSA vào file.
        """
        # Lưu khóa riêng
        with open(private_key_file, "wb") as priv_file:
            priv_file.write(
                self.private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
            )
        # Lưu khóa công khai
        with open(public_key_file, "wb") as pub_file:
            pub_file.write(
                self.public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
            )

    def generate_random_string(self):
        """
        Tạo một chuỗi ngẫu nhiên 32 ký tự.
        """
        return str(uuid.uuid4()).replace("-", "")[:self.key_length]

    def encrypt_with_rsa(self, data: str) -> str:
        """
        Mã hóa dữ liệu bằng khóa công khai RSA.
        """
        encrypted_data = self.public_key.encrypt(
            data.encode("utf-8"),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_data.hex()

    def check_id(self) -> bool:
        """
        Kiểm tra xem file đã tồn tại và có ID hay chưa.
        """
        if not os.path.exists(self.filename):
            return False
        with open(self.filename, "r") as file:
            first_line = file.readline().strip()
            return first_line.startswith("id: ")

    def create_id(self):
        """
        Tạo file với định dạng yêu cầu.
        """
        if self.check_id():
            print(f"File '{self.filename}' đã tồn tại với ID.")
            return

        with open(self.filename, "w") as file:
            # Tạo ID và ghi vào dòng đầu
            file_id = self.generate_random_string()
            file.write(f"id: {file_id}\n")

            # Tạo chuỗi ngẫu nhiên và mã hóa RSA, ghi vào dòng thứ hai
            random_string = self.generate_random_string()
            encrypted_string = self.encrypt_with_rsa(random_string)
            file.write(f"{encrypted_string}\n")
            print(f"File '{self.filename}' được tạo thành công với ID {file_id}.")
            return file_id

    def get_id(self) -> str:
        """
        Lấy ID từ file.
        """
        if not self.check_id():
            raise FileNotFoundError(f"File '{self.filename}' không tồn tại hoặc không có ID.")
        
        with open(self.filename, "r") as file:
            first_line = file.readline().strip()
            return first_line.replace("id: ", "")

    def add_encrypted_line(self):
        """
        Thêm dòng mã hóa mới vào file hiện tại.
        """
        if not self.check_id():
            print(f"File '{self.filename}' không tồn tại. Hãy tạo nó trước.")
            return

        random_string = self.generate_random_string()
        encrypted_string = self.encrypt_with_rsa(random_string)

        with open(self.filename, "a") as file:
            file.write(f"{encrypted_string}\n")
        print("Dòng mã hóa mới đã được thêm vào file.")

