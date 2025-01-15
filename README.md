# Nghiên cứu các giải thuật mã hóa

Đây là dự án môn **Cấu trúc dữ liệu và giải thuật**, tập trung vào việc tìm hiểu và mô phỏng các giải thuật mã hóa phổ biến. Dự án nhằm cung cấp kiến thức cơ bản về mã hóa dữ liệu, áp dụng thực tế vào các bài toán bảo mật thông tin.

---

## Mục tiêu

- Hiểu rõ nguyên lý hoạt động của các giải thuật mã hóa cơ bản và nâng cao.

- Đánh giá hiệu quả và tính bảo mật của từng giải thuật trong các ứng dụng thực tế.

- Cung cấp tài liệu minh họa và mã nguồn để hỗ trợ học tập và nghiên cứu.

## Nội dung chính

### 1. Caesar Cipher

**Đặc điểm:**
- Là một trong những thuật toán mã hóa cổ điển, dễ hiểu và dễ triển khai.
- Dịch chuyển các ký tự trong bản rõ một số lượng bước cố định.

**Ứng dụng:**
- Tìm hiểu nguyên lý mã hóa cơ bản.
- Thích hợp để giảng dạy hoặc minh họa.

**Giao diện demo:**
![Caesar Cipher Demo]![ceaserCipher](https://github.com/user-attachments/assets/a4b12e25-8cb7-45de-b18f-fadc286d972b)

---

### 2. Advanced Encryption Standard (AES)

**Đặc điểm:**
- Mã hóa đối xứng hiện đại, được chuẩn hóa bởi NIST.
- Sử dụng các kích thước khóa: 128-bit, 192-bit, 256-bit.
- Bảo mật cao và tốc độ xử lý nhanh.

**Ứng dụng:**
- Bảo mật dữ liệu trong giao tiếp mạng.
- Lưu trữ dữ liệu an toàn.

**Giao diện demo:**
![AES Demo]![image](https://github.com/user-attachments/assets/0eb64cc8-d14f-4d7a-b3b7-6756e07d6169)

---

### 3. RSA (Rivest–Shamir–Adleman)

**Đặc điểm:**
- Mã hóa bất đối xứng sử dụng cặp khóa công khai và khóa riêng.
- Dựa trên bài toán phân tích số nguyên lớn, rất khó để phá vỡ.

**Ứng dụng:**
- Mã hóa email, chữ ký số.
- Bảo mật giao dịch trực tuyến.

**Giao diện demo:**
![RSA Demo]![image](https://github.com/user-attachments/assets/5c1d811e-b534-4fb0-998a-93ca2e30c1a1)

---

### 4. SHA-256 (Secure Hash Algorithm 256-bit)

**Đặc điểm:**
- Hàm băm được sử dụng rộng rãi trong blockchain và bảo mật dữ liệu.
- Biến đổi dữ liệu đầu vào thành chuỗi băm 256-bit cố định.
- Không thể đảo ngược về dữ liệu gốc.

**Ứng dụng:**
- Xác minh tính toàn vẹn của dữ liệu.
- Lưu trữ mật khẩu an toàn.

**Giao diện demo:**
![SHA-256 Demo]![image](https://github.com/user-attachments/assets/08560ba6-45af-4379-96e0-392620560b31)


## Yêu cầu hệ thống

- **Ngôn ngữ**: Python (phiên bản `>=3.11`).
- **Thư viện bổ sung**:
  - `cryptography`
  - `pycryptodome`
  - `hashlib`
  - `pygame`

---

## Quy tắc làm việc nhóm

1. **Quản lý nhánh làm việc**:
   - Mỗi thành viên nên làm việc trên nhánh riêng của mình:
     - An, Đại, Thắng, Phúc, Phước: `an`, `dai`, `phuc`, `phuoc`, `thang`.
   - Đối với file Word hoặc PowerPoint, sử dụng nhánh chung:
     - **Word**: `word`.
     - **PowerPoint**: `pp`.
   - Các thành viên có nhiều công việc (Phúc và Phước) sẽ làm mã nguồn trên nhánh cá nhân (`phuc`, `phuoc`) và các tài liệu trên nhánh chung (`word`, `pp`). hoặc thích thì tạo thêm nhánh `phuc_word`, `phuoc_pp` nếu thích.

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
   - Sau khi hoàn thành công việc, gửi Pull Request từ nhánh cá nhân hoặc nhánh chung để được xem xét.

5. **Kiểm tra kỹ trước khi hợp nhất**:
   - Đảm bảo mã nguồn không có lỗi và đã được kiểm tra kỹ trước khi gửi yêu cầu hợp nhất.

---



## Tác giả

- Dự án được thực hiện bởi nhóm **Nhóm 9**.
- Mọi đóng góp hoặc thắc mắc, vui lòng tạo **Issue** trong GitHub Repository.

---
