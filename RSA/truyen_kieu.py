import random

class TruyenKieu:
    def __init__(self, filename='RSA/truyện kiều.txt'):
        # Mở file và đọc nội dung
        with open(filename, 'r', encoding='utf-8') as file:
            self.content = file.read()

        # Tách các khổ thơ bằng dấu "---"
        self.verse_blocks = self.content.split('---')

        # Khởi tạo các thuộc tính để quản lý trạng thái
        self.current_verse = []  # Lưu khổ thơ hiện tại
        self.current_line_index = 0  # Chỉ số dòng hiện tại trong khổ thơ
        self.current_char_index = 0  # Chỉ số ký tự hiện tại trong dòng

        # Lấy khổ thơ đầu tiên
        self.get_random_verse()

    def get_random_verse(self):
        # Chọn ngẫu nhiên một khổ thơ
        random_verse = random.choice(self.verse_blocks).strip()

        # Tách khổ thơ thành từng dòng và lưu vào current_verse
        self.current_verse = random_verse.split('\n')
        self.current_line_index = 0  # Đặt lại chỉ số dòng
        self.current_char_index = 0  # Đặt lại chỉ số ký tự

        return self.current_verse

    def get_next_line(self):
        # Nếu đã duyệt hết các dòng trong khổ hiện tại, chọn khổ mới
        if self.current_line_index >= len(self.current_verse):
            self.get_random_verse()

        # Lấy dòng hiện tại
        next_line = self.current_verse[self.current_line_index].strip()
        
        # Tăng chỉ số dòng, đặt lại chỉ số ký tự
        self.current_line_index += 1
        self.current_char_index = 0

        return next_line

    def get_next_character(self):
        # Nếu đã duyệt hết các dòng trong khổ hiện tại, chọn khổ mới
        if self.current_line_index >= len(self.current_verse):
            self.get_random_verse()

        # Lấy dòng hiện tại
        current_line = self.current_verse[self.current_line_index]

        # Nếu đã duyệt hết ký tự trong dòng hiện tại
        if self.current_char_index >= len(current_line):
            self.current_char_index = 0  # Đặt lại chỉ số ký tự
            self.current_line_index += 1  # Chuyển sang dòng kế tiếp

            # Nếu dòng kế tiếp vượt quá giới hạn, chọn khổ mới
            if self.current_line_index >= len(self.current_verse):
                self.get_random_verse()

            return '\n'  # Trả về ký tự xuống dòng

        # Lấy ký tự hiện tại
        next_char = current_line[self.current_char_index]

        # Tăng chỉ số ký tự
        self.current_char_index += 1

        return next_char

# Ví dụ sử dụng
# filename = 'truyện kiều.txt'  # Đảm bảo file truyện kiều.txt nằm trong cùng thư mục với file Python
# truyen_kieu = TruyenKieu()

# for _ in range(10):
#     print(truyen_kieu.get_next_line())

# print('\n')


# import time
# while True:
#     time.sleep(0.08)
#     print(truyen_kieu.get_next_character(), end='')
