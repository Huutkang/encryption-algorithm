import random
# import time

class TruyenKieu:
    def __init__(self, filename):
        # Mở file và đọc nội dung
        with open(filename, 'r', encoding='utf-8') as file:
            self.content = file.read()

        # Tách các khổ thơ bằng dấu "---"
        self.verse_blocks = self.content.split('---')

    def get_random_verse(self):
        # Chọn ngẫu nhiên một khổ thơ
        random_verse = random.choice(self.verse_blocks).strip()

        # Tách khổ thơ thành từng dòng và trả về dưới dạng mảng
        return random_verse.split('\n')



# # Ví dụ sử dụng
# import time
# filename = 'truyện kiều.txt'  # Đảm bảo file truyện kiều.txt nằm trong cùng thư mục với file Python
# truyen_kieu = TruyenKieu(filename)

# for i in range(1000):
#     # Lấy một khổ thơ ngẫu nhiên
#     verse = truyen_kieu.get_random_verse()

#     # In kết quả
#     for line in verse:
#         print(line)
#     time.sleep(0.1)
#     print('\n')  # Xuống dòng

