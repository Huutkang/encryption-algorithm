import os

def compile_cpp(file_path):
    # Loại bỏ đuôi ".cpp" để đặt tên tệp thực thi
    file_path_no_ext = file_path[:-4]
    
    # Lệnh biên dịch, bao gồm các đường dẫn OpenSSL
    command = (
        'g++ "' + file_path + '" -o "' + file_path_no_ext + '.exe" '
        '-I"C:\\Program Files\\OpenSSL-Win64\\include" '
        '"C:\\Program Files\\OpenSSL-Win64\\lib\\VC\\x64\\MD\\libssl.lib" '
        '"C:\\Program Files\\OpenSSL-Win64\\lib\\VC\\x64\\MD\\libcrypto.lib"'
    )
    
    # Thực thi lệnh biên dịch
    os.system(command)
    print(f"Đã biên dịch {file_path} thành {file_path_no_ext}.exe!")

# Danh sách các tệp C++ cần biên dịch
file_paths = [ "Demo Pay for File/encode.cpp", "Demo Pay for File/decode.cpp"]

# Biên dịch từng tệp
for file_path in file_paths:
    compile_cpp(file_path)

