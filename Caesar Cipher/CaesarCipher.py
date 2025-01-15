

class CaesarCipher:
    def __init__(self, shift: int):
        """
        Khởi tạo lớp CaesarCipher với một giá trị dịch chuyển.
        :param shift: Số ký tự cần dịch chuyển (shift).
        """
        self.shift = shift % 26  # Đảm bảo shift nằm trong khoảng 0-25

    def set_shift(self, new_shift: int):
        """
        Thay đổi giá trị dịch chuyển.
        :param new_shift: Giá trị mới cho shift.
        """
        self.shift = new_shift % 26  # Cập nhật shift trong khoảng 0-25
        print(f"Shift đã được thay đổi thành: {self.shift}")

    def increase_shift(self):
        """
        Tăng giá trị dịch chuyển thêm 1.
        """
        self.shift = (self.shift + 1) % 26
        print(f"Shift đã được tăng thành: {self.shift}")

    def decrease_shift(self):
        """
        Giảm giá trị dịch chuyển đi 1.
        """
        self.shift = (self.shift - 1) % 26
        print(f"Shift đã được giảm thành: {self.shift}")

    @staticmethod
    def is_valid_character(char: str) -> bool:
        """
        Kiểm tra nếu ký tự là chữ hoặc số.
        :param char: Ký tự cần kiểm tra.
        :return: True nếu là chữ hoặc số, False nếu không.
        """
        return char.isalnum()

    def encrypt(self, plaintext: str) -> str:
        """
        Mã hóa một chuỗi văn bản bằng Caesar Cipher.
        :param plaintext: Chuỗi cần mã hóa.
        :return: Chuỗi đã được mã hóa.
        """
        encrypted_text = []
        for char in plaintext:
            if char.isalpha():  # Chỉ mã hóa các ký tự chữ cái
                shift_base = ord('A') if char.isupper() else ord('a')
                encrypted_char = chr((ord(char) - shift_base + self.shift) % 26 + shift_base)
                encrypted_text.append(encrypted_char)
            else:
                encrypted_text.append(char)  # Giữ nguyên ký tự không phải chữ cái
        return ''.join(encrypted_text)

    def decrypt(self, ciphertext: str) -> str:
        """
        Giải mã một chuỗi văn bản đã mã hóa bằng Caesar Cipher.
        :param ciphertext: Chuỗi cần giải mã.
        :return: Chuỗi đã được giải mã.
        """
        decrypted_text = []
        for char in ciphertext:
            if char.isalpha():  # Chỉ giải mã các ký tự chữ cái
                shift_base = ord('A') if char.isupper() else ord('a')
                decrypted_char = chr((ord(char) - shift_base - self.shift) % 26 + shift_base)
                decrypted_text.append(decrypted_char)
            else:
                decrypted_text.append(char)  # Giữ nguyên ký tự không phải chữ cái
        return ''.join(decrypted_text)


