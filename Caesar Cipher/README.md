
# Mô phỏng Mã hóa Caesar Cipher

Dự án này là một ứng dụng đồ họa sử dụng thư viện `pygame` để mô phỏng cách hoạt động của mã hóa Caesar Cipher. Người dùng có thể nhập văn bản, thay đổi giá trị dịch chuyển (shift) và xem trực quan quá trình mã hóa và giải mã.

## Cách cài đặt

### Yêu cầu hệ thống

- Python 3.8 trở lên
- Các thư viện Python cần thiết:
  - `pygame`

### Cài đặt các thư viện cần thiết

Sử dụng lệnh sau để cài đặt `pygame`:

```bash
pip install pygame
```

## Cách sử dụng

1. **Chạy chương trình:**
   - Mở terminal hoặc command prompt và chạy lệnh:

     ```bash
     python main.py
     ```

2. **Hướng dẫn sử dụng:**
   - **Nhập văn bản**: Nhập văn bản bạn muốn mã hóa hoặc giải mã (tối đa 30 ký tự). Chỉ nhận các ký tự chữ cái và khoảng trắng.
   - **Điều chỉnh shift**: Sử dụng phím mũi tên trái (`←`) và mũi tên phải (`→`) để giảm hoặc tăng giá trị dịch chuyển.
   - **Xác nhận**: Nhấn phím Enter (`Enter`) để bắt đầu mã hóa.
   - **Quy trình**:
     - Văn bản sẽ được mã hóa và hiển thị từng bước.
     - Sau khi mã hóa, nhấn Enter để chuyển sang giải mã.
     - Kết quả giải mã sẽ khớp với văn bản gốc.

3. **Thoát chương trình:**
   - Nhấn nút `X` trên cửa sổ hoặc phím `Esc` để thoát.

## Góp ý và báo lỗi

Nếu bạn gặp bất kỳ vấn đề nào hoặc có ý kiến cải thiện, vui lòng tạo một issue trên repository hoặc liên hệ với chúng tôi.

---

Chúc bạn có trải nghiệm thú vị với ứng dụng!
