import hashlib, os

class FileChecksumVerifier:
    
    def calculate_checksum(self, file_path) -> str:
        """
        Tính toán checksum SHA-256 của file.
        """
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                # Đọc file theo từng khối để tránh tốn nhiều bộ nhớ
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except FileNotFoundError:
            print(f"File {self.file_path} không tồn tại.")
            return ""

    def checksum(self, file_path, expected_checksum) -> bool:
        """
        Kiểm tra checksum của file với checksum mong đợi.
        """
        calculated_checksum = self.calculate_checksum(file_path)
        if not calculated_checksum:
            return False

        if calculated_checksum == expected_checksum:
            return True
        else:
            return False
