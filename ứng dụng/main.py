from FileChecksumVerifier import FileChecksumVerifier
from PasswordManager import PasswordManager
from RSASignature import RSASignature
import os


fileChecksumVerifier = FileChecksumVerifier()
passwordManager = PasswordManager()
rsaSignature = RSASignature(False)



# Checksum

# # tạo chuỗi hash cho file. đây là chuỗi tải xuống sẽ có thêm chuỗi này để so sánh file đã tải thành công hay chưa
# x = fileChecksumVerifier.calculate_checksum("ứng dụng/ảnh.jpg")
# print(x)



# chuỗi checksum trong file ở vị trí "./ứng dụng/checksum anh.jpg.txt" nó là đoạn mã đi kèm khi tải xuống
# a = fileChecksumVerifier.checksum("ứng dụng/ảnh.jpg", "86d03fe6483f500d94bbf5ecc3dd2f4df62a63a3db25da0b0f8aacde6ff97ec2")

# if a:
#     print("Checksum hợp lệ! File không bị thay đổi.")
# else:
#     print("Checksum không hợp lệ! File có thể đã bị thay đổi.")





# Password

# # Nơi ghi mật khẩu đã băm
# hashed_password_file = "ứng dụng/hashed_password.txt"

# # Nhập mật khẩu và băm
# original_password = "my_secure_password"
# hashed = passwordManager.hash_password(original_password)
# print("Mật khẩu đã băm (SHA-256):", hashed)
# passwordManager.save_hashed_password(hashed, hashed_password_file)
# print(f"Mật khẩu đã băm được lưu vào file {hashed_password_file}")


# # Đọc lại mật khẩu đã băm từ file
# saved_hashed = passwordManager.read_hashed_password(hashed_password_file)
# print("Mật khẩu đã băm được đọc từ file:", saved_hashed)
# # Kiểm tra mật khẩu khớp
# check_password = "my_secure_password"
# if passwordManager.verify_password(check_password, saved_hashed):
#     print("Mật khẩu khớp!")
# else:
#     print("Mật khẩu không khớp!")







# Signature

# input_file = "ứng dụng/sample RSASignature.txt"
# # Nơi lưu chữ ký
# signature_file = "ứng dụng/signature.sig"
# private_key_file = "ứng dụng/key/private_key.pem"
# public_key_file = "ứng dụng/key/public_key.pem"


# # # Tạo và lưu khóa nếu chưa có khóa
# if not os.path.exists(private_key_file) or not os.path.exists(public_key_file):
#     private_key, public_key = rsaSignature.generate_keys()
#     rsaSignature.set_keys(private_key, public_key)
#     rsaSignature.save_keys(private_key_file, public_key_file)
#     print(f"Khóa RSA đã được lưu vào {private_key_file} và {public_key_file}")


# rsaSignature.set_keys_from_files(private_key_file, public_key_file)
# # Đọc nội dung file
# with open(input_file, "rb") as file:
#     message = file.read()
# # Ký số
# signature = rsaSignature.sign_message(message)
# print("Chữ ký số đã được tạo.")
# # Lưu chữ ký vào file
# with open(signature_file, "wb") as sig_file:
#     sig_file.write(signature)
# print(f"Chữ ký số đã được lưu vào file {signature_file}")


# rsaSignature.set_keys_from_files(private_key_file, public_key_file)
# # Đọc nội dung file
# with open(input_file, "rb") as file:
#     message = file.read()
# # Đọc chữ ký từ file
# with open(signature_file, "rb") as sig_file:
#     signature = sig_file.read()
# print("Chữ ký số đã được đọc từ file.")
# # Xác minh chữ ký
# is_valid = rsaSignature.verify_signature(message, signature)
# if is_valid:
#     print("Chữ ký hợp lệ!")
# else:
#     print("Chữ ký không hợp lệ!")
