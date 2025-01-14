# Hướng Dẫn Sử Dụng Dự Án Mô Phỏng RSA

## Giới Thiệu

Dự án này là một mô phỏng thuật toán mã hóa RSA, được triển khai bằng Python kèm giao diện đồ họa sử dụng thư viện Pygame. Dự án bao gồm các tính năng:

- Sinh các cặp khóa RSA.
- Mã hóa và giải mã thông điệp.
- Hiển thị trực quan quy trình hoạt động của thuật toán.

## Thiết Lập Môi Trường

1. Cài đặt Python 3.7 hoặc cao hơn.
2. Cài đặt thư viện Pygame:

   ```bash
   pip install pygame
   ```

3. Đảm bảo mở trong thư mục mẹ của thư mục RSA.

## Hướng Dẫn Sử Dụng

### 1. Chạy Chương Trình

- Mở terminal, di chuyển đến thư mục dự án:

- Chạy tệp `main.py`:

  ```bash
  python main.py
  ```

### 2. Tính Năng Giao Diện

#### Sinh Khóa RSA

- Nhập độ dài khóa mong muốn (vd: 64, 128, 256 bit).
- Khóa công khai (e, N) và khóa bí mật (d) sẽ được hiển thị.

#### Mã Hóa và Giải Mã

- Sử dụng các phím mũi tên để chuyển đổi chế độ:
  - **Mũi tên lên**: Bắt đầu chế độ tự động.
  - **Mũi tên xuống**: Chọn chế độ thủ công (và vào chế độ mã hóa).
  - **Mũi tên phải**: Chọn chế độ giải mã (sau khi ở chế độ thủ công)
  - **Y/N**: Phản hồi các nhắc nhở trong quá trình sinh khóa..
- Nhập thông điệp qua bàn phím, nhấn **Enter** để thực hiện một số quá trình.
- Quan sát quá trình mã hóa và giải mã được hiển thị trực quan.

#### Tương Tác Bằng Chuột

- Nhấn chuột vào nút go trên giao diện để bắt đầu mã hóa.

#### Tương Tác Bằng Bàn Phím

- có thể nhập thông tin vào ô input, và nhập được cả tiếng Việt.

### 3. Công Cụ Hỗ Trợ

#### Xử Lý Số Nguyên Tố

- Sử dụng tệp `prime.py` để sinh số nguyên tố lớn hoặc kiểm tra tính nguyên tố của một số:

  ```python
  from prime import PrimeNumberUtils
  utils = PrimeNumberUtils()
  utils.generatePrimeNumbers(100)
  print(utils.isPrime(37))  # True
  ```

#### Trích Xuất "Truyện Kiều"

- Sử dụng tệp `truyen_kieu.py` để lấy ngẫu nhiên các đoạn thơ:

  ```python
  from truyen_kieu import TruyenKieu
  truyen = TruyenKieu()
  print(truyen.get_random_verse())
  print(truyen.get_next_line())
  ```

## Lưu Ý

- Dự án đã được tối ưu hóa cho độ phân giải 1200x800. Nếu sử dụng độ phân giải khác, giao diện có thể hiển thị không đúng như mong muốn.
- File `primes.txt` chứa danh sách các số nguyên tố nhỏ để tối ưu hóa quá trình sinh và kiểm tra số nguyên tố.

## Liên Hệ

Mọi đóng góp hoặc phản hồi về dự án, vui lòng liên hệ qua email của nhóm phát triển.
