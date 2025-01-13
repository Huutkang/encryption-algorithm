# SHA-256 Algorithm Simulation with Pygame

## Yêu cầu hệ thống
1. Python 3.6 trở lên.
2. Môi trường lập trình đã cài đặt `pip`.

## Hướng dẫn cài đặt

### Bước 1: Cài đặt Pygame
Pygame là thư viện Python được sử dụng để xây dựng các trò chơi và đồ họa. Để cài đặt, thực hiện các bước sau:

#### Trên Windows
1. Mở Command Prompt.
2. Nhập lệnh sau để cài đặt Pygame:
   ```bash
   pip install pygame
   ```
3. Đợi quá trình cài đặt hoàn tất.

#### Trên Linux/Mac
1. Mở Terminal.
2. Nhập lệnh sau để cài đặt Pygame:
   ```bash
   pip install pygame
   ```
3. Đợi quá trình cài đặt hoàn tất.

### Bước 2: Kiểm tra cài đặt Pygame
Để kiểm tra xem Pygame đã được cài đặt thành công hay chưa, bạn có thể chạy lệnh:
```bash
python -m pygame --version
```
Nếu lệnh này trả về phiên bản của Pygame (ví dụ: `2.1.3`), bạn đã cài đặt thành công.

### Bước 3: Chạy file `done.py`
1. Đảm bảo file `done.py` nằm trong thư mục hiện tại của bạn.
2. Mở Terminal (Linux/Mac) hoặc Command Prompt (Windows) và điều hướng tới thư mục chứa file `done.py`.
   ```bash
   cd /duong/dan/toi/thu/muc
   ```
3. Chạy file `done.py` bằng lệnh:
   ```bash
   python done.py
   ```

### Lưu ý
- Nếu gặp lỗi `ModuleNotFoundError: No module named 'pygame'`, hãy kiểm tra lại việc cài đặt Pygame hoặc môi trường Python.
- Đảm bảo bạn đang sử dụng đúng phiên bản Python hỗ trợ Pygame.

## Thông tin thêm
- Trang chủ Pygame: [https://www.pygame.org](https://www.pygame.org)
- Tài liệu chính thức: [https://www.pygame.org/docs/](https://www.pygame.org/docs/)

Chúc bạn thành công và tận hưởng chương trình với Pygame! 🚀

# Sau đây là cách sử dụng ứng dụng mô phỏng thuật toán SHA-256 với giao diện sử dụng Pygame:

- Khi bắt đầu ứng dụng hãy nhập văn bản bạn muốn mô phỏng (**Lưu ý**: Chỉ nhập ký tự chữ và số)
- Nhấn nút **Enter** hoặc nhấp chuột vào nút **Visualize** để bắt đầu
- Để xóa 1 ký tự khi nhập hãy nhấn nút **Backscape**

## Sau khi bắt đầu mô phỏng thì chuyển sang điều khiển bằng các nút dưới:
- **Return** để quay trở lại bắt đầu để nhập văn bản mới
- ➡ **Sang phải** để tiến tới bước tiếp theo và lưu ý chỉ dùng khi bước hiện tại đã mô phỏng xong
- ⬅ **Sang trái** để lùi lại bước trước

https://yesno.wtf/api
