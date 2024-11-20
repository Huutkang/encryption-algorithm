
# Tìm hiểu và mô phỏng một số giải thuật mã hóa

Đây là dự án môn **Cấu trúc dữ liệu và giải thuật**, tập trung vào việc tìm hiểu và mô phỏng các giải thuật mã hóa phổ biến. Dự án nhằm cung cấp kiến thức cơ bản về mã hóa dữ liệu, áp dụng thực tế vào các bài toán bảo mật thông tin.

--- 

## Nội dung chính

1. **Giải thuật mã hóa**:
   - Mã hóa đối xứng (Symmetric Encryption): AES, DES, Triple DES.
   - Mã hóa bất đối xứng (Asymmetric Encryption): RSA, ECC.
   - Các giải thuật khác: MD5, SHA-256.

2. **Mô phỏng hoạt động**:
   - Cách mã hóa/giải mã dữ liệu.
   - So sánh hiệu suất và bảo mật giữa các giải thuật.

--- 

## Yêu cầu hệ thống

- **Ngôn ngữ**: Python (phiên bản `>=3.11`).
- **Thư viện bổ sung**:
  - `cryptography`
  - `pycryptodome`
  - `hashlib`

--- 

## Hướng dẫn cài đặt

1. **Clone dự án từ GitHub**:
   ```bash
   git clone https://github.com/Huutkang/encryption-algorithm.git
   cd encryption-algorithm
   ````

2. **Để sau viết tiếp**:

--- 

## Quy tắc làm việc nhóm

1. **Làm việc trên nhánh cá nhân**:
   - Mỗi thành viên làm việc trên nhánh riêng của mình (an, dai, phuc, phuoc, thang).
    ```bash
     git branch -M <tên_nhánh cá nhân>
     ```

2. **Luôn pull mã nguồn trước khi bắt đầu**:
   - Đảm bảo mã nguồn được cập nhật từ nhánh `main`:
     ```bash
     git pull origin main
     ```
    - Nếu bạn muốn pull nhánh từ thành viên khác:
     ```bash
     git pull origin <tên_nhánh>
     ```
    

3. **Commit rõ ràng**:
   - Commit cần có thông điệp mô tả chi tiết:
     ```bash
     git commit -m "Thêm mô phỏng AES (feature/aes)"
     ```

4. **Yêu cầu hợp nhất mã nguồn (Pull Request)**:
   - Sau khi hoàn thành công việc, gửi Pull Request từ nhánh cá nhân để được xem xét.

5. **Kiểm tra kỹ trước khi hợp nhất**:
   - Đảm bảo mã nguồn không có lỗi và đã được kiểm tra kỹ trước khi gửi yêu cầu hợp nhất.

--- 

## Một số lưu ý

1. **Không đẩy các file tạm thời hoặc môi trường ảo**:
   - Các file như `.pyc`, thư mục `venv` đã được liệt kê trong `.gitignore`.

2. **Cài đặt thư viện mới**:
   - Nếu thêm thư viện mới, chạy:
     ```bash
     pip install <tên_thư_viện>
     pip freeze > requirements.txt
     ```
   - Commit file `requirements.txt`.

3. **Liên hệ hỗ trợ**:
   - Nếu gặp vấn đề, vui lòng liên hệ **Hữu Thắng** hoặc các thành viên khác để được hỗ trợ.

---

## Tác giả

- Dự án được thực hiện bởi nhóm **Đặt tên đê**.
- Mọi đóng góp hoặc thắc mắc, vui lòng tạo **Issue** trong GitHub Repository.

---
