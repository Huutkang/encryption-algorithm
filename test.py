from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# Chuỗi đầu vào và khóa (sử dụng UTF-8)
plaintext = "Hello, world!123".encode("utf-8")  # Mã hóa chuỗi sang bytes bằng UTF-8
key = "mysecretkey12345".encode("utf-8")       # Mã hóa chuỗi sang bytes bằng UTF-8

# Tạo đối tượng AES (chế độ ECB)
cipher = AES.new(key, AES.MODE_ECB)

# Mã hóa chuỗi
ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))  # Pad chuỗi để đạt độ dài bội của 16 bytes

# In kết quả
print("Ciphertext (hex):", ciphertext.hex())
