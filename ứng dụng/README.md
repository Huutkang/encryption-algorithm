
# Hướng dẫn sử dụng các tính năng mã hóa trong ứng dụng

Ứng dụng này là một bộ công cụ demo các thuật toán mã hóa bao gồm: kiểm tra checksum, quản lý mật khẩu và ký số RSA. Bạn có thể chạy từng tính năng bằng cách mở phần comment tương ứng trong file `main.py`.

## Cài đặt môi trường

1. **Python**: Yêu cầu Python 3.6 trở lên.
2. **Cài đặt thư viện cần thiết**:

   ```bash
   pip install cryptography
   ```

## Các tệp chính

- `FileChecksumVerifier.py`: Tính toán và kiểm tra checksum SHA-256 cho file.
- `PasswordManager.py`: Băm mật khẩu bằng SHA-256 và kiểm tra mật khẩu.
- `RSASignature.py`: Tạo khóa RSA, ký số, và xác minh chữ ký số.
- `main.py`: File chính để demo các tính năng trên.

---

## Hướng dẫn sử dụng

### 1. **Kiểm tra Checksum**

- **Mục đích**: Kiểm tra file tải xuống có bị thay đổi hay không bằng cách so sánh checksum.
- **Cách sử dụng**:

  1. Tính toán checksum cho một file:

    ```python
    x = fileChecksumVerifier.calculate_checksum("ứng dụng/ảnh.jpg")
    print(x)
    ```

  2. Kiểm tra checksum có khớp với giá trị mong đợi không:

    ```python
    a = fileChecksumVerifier.checksum("ứng dụng/ảnh.jpg", "checksum_mong_đợi")
    if a:
        print("Checksum hợp lệ! File không bị thay đổi.")
    else:
        print("Checksum không hợp lệ! File có thể đã bị thay đổi.")
    ```

### 2. **Quản lý Mật khẩu**

- **Mục đích**: Lưu mật khẩu an toàn và kiểm tra tính hợp lệ của mật khẩu.
- **Cách sử dụng**:
     1. Băm mật khẩu và lưu vào file:

        ```python
        original_password = "my_secure_password"
        hashed = passwordManager.hash_password(original_password)
        print("Mật khẩu đã băm (SHA-256):", hashed)
        passwordManager.save_hashed_password(hashed, "ứng dụng/hashed_password.txt")
        ```

     2. Kiểm tra mật khẩu khớp:

        ```python
        saved_hashed = passwordManager.read_hashed_password("ứng dụng/hashed_password.txt")
        check_password = "my_secure_password"
        if passwordManager.verify_password(check_password, saved_hashed):
            print("Mật khẩu khớp!")
        else:
            print("Mật khẩu không khớp!")
        ```

### 3. **Ký số RSA**

- **Mục đích**: Tạo chữ ký số cho file và xác minh chữ ký.
- **Cách sử dụng**:
     1. Tạo cặp khóa RSA:

        ```python
        private_key, public_key = rsaSignature.generate_keys()
        rsaSignature.save_keys("ứng dụng/key/private_key.pem", "ứng dụng/key/public_key.pem")
        ```

     2. Ký số cho một file:

        ```python
        with open("ứng dụng/sample RSASignature.txt", "rb") as file:
            message = file.read()
        signature = rsaSignature.sign_message(message)
        with open("ứng dụng/signature.sig", "wb") as sig_file:
            sig_file.write(signature)
        ```

     3. Xác minh chữ ký số:

        ```python
        rsaSignature.set_keys_from_files("ứng dụng/key/private_key.pem", "ứng dụng/key/public_key.pem")
        with open("ứng dụng/sample RSASignature.txt", "rb") as file:
            message = file.read()
        with open("ứng dụng/signature.sig", "rb") as sig_file:
            signature = sig_file.read()
        is_valid = rsaSignature.verify_signature(message, signature)
        if is_valid:
            print("Chữ ký hợp lệ!")
        else:
            print("Chữ ký không hợp lệ!")
        ```

---

## Lưu ý

- Để chạy từng tính năng, mở comment của từng phần trong file `main.py`.
- Các file liên quan như `ảnh.jpg`, `hashed_password.txt`, `sample RSASignature.txt`, và các file khóa nên được đặt trong thư mục `ứng dụng`.

Chúc bạn thành công!
