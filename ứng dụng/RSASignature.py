from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.padding import PSS, MGF1
from cryptography.hazmat.primitives.hashes import SHA256
import os

class RSASignature:
    def __init__(self, generate = True):
        if generate:
            self.private_key, self.public_key = self.generate_keys()
        else:
            self.private_key = None
            self.public_key = None

    def generate_keys(self):
        """
        Tạo cặp khóa RSA mới và lưu vào thuộc tính.
        """
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()
        return private_key, public_key
    
    def set_keys(self, private_key, public_key):
        self.private_key = private_key
        self.public_key = public_key

    def set_keys_from_files(self, private_key_file: str, public_key_file: str):
        """
        Đọc khóa RSA từ file và đặt vào thuộc tính.
        """
        # Đọc khóa riêng
        with open(private_key_file, "rb") as priv_file:
            self.private_key = serialization.load_pem_private_key(
                priv_file.read(),
                password=None
            )
        # Đọc khóa công khai
        with open(public_key_file, "rb") as pub_file:
            self.public_key = serialization.load_pem_public_key(
                pub_file.read()
            )

    def save_keys(self, private_key_file: str, public_key_file: str):
        """
        Lưu khóa RSA vào file.
        """
        if self.private_key is None or self.public_key is None:
            raise ValueError("Khóa chưa được tạo hoặc thiết lập.")

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

    def sign_message(self, message: bytes) -> bytes:
        """
        Ký số một thông điệp.
        """
        if self.private_key is None:
            raise ValueError("Khóa riêng chưa được thiết lập.")
        signature = self.private_key.sign(
            message,
            PSS(
                mgf=MGF1(SHA256()),
                salt_length=PSS.MAX_LENGTH
            ),
            SHA256()
        )
        return signature

    def verify_signature(self, message: bytes, signature: bytes) -> bool:
        """
        Xác minh chữ ký số.
        """
        if self.public_key is None:
            raise ValueError("Khóa công khai chưa được thiết lập.")
        try:
            self.public_key.verify(
                signature,
                message,
                PSS(
                    mgf=MGF1(SHA256()),
                    salt_length=PSS.MAX_LENGTH
                ),
                SHA256()
            )
            return True
        except Exception as e:
            print("Xác minh chữ ký thất bại:", e)
            return False
