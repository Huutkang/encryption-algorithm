import ctypes
import os

def call_encode_subprocess(process_args):
    """
    Gọi chương trình encode với đối số đầu vào, không chờ chương trình con kết thúc.
    
    :param process_args: Danh sách chứa đường dẫn chương trình encode và các tham số [exe_path, arg1, arg2, arg3].
    """
    kernel32 = ctypes.windll.kernel32

    # Chuyển danh sách thành chuỗi command
    command_line = '"'+process_args[0]+'" '+process_args[1] + ' "'+process_args[2] + '" "'+process_args[3]+'"'
    # STARTUPINFO cấu hình khởi tạo chương trình
    startup_info = ctypes.create_string_buffer(68)
    process_info = ctypes.create_string_buffer(16)
    
    # Đánh dấu process sẽ chạy mà không chờ
    creation_flags = 0x00000008  # CREATE_NO_WINDOW

    # Gọi CreateProcess
    result = kernel32.CreateProcessA(
        None,  # Module (None -> chỉ định qua command line)
        ctypes.create_string_buffer(command_line.encode('utf-8')),
        None,  # Process security attributes
        None,  # Thread security attributes
        False,  # Inherit handles
        creation_flags,  # Creation flags
        None,  # Environment
        None,  # Current directory
        ctypes.byref(startup_info),  # Startup info
        ctypes.byref(process_info),  # Process info
    )

    if result == 0:
        raise OSError("Failed to start process. Error code: {}".format(kernel32.GetLastError()))

    print(f"Process started with PID: {ctypes.cast(process_info, ctypes.POINTER(ctypes.c_int))[0]}")


def call_decode_subprocess(exe_path, source_file, destination_file):
    """
    Gọi chương trình decode với đối số đầu vào, không chờ chương trình con kết thúc.
    
    :param source_file: Đường dẫn tới file nguồn.
    :param destination_file: Đường dẫn tới file đích.
    """
    kernel32 = ctypes.windll.kernel32

    # Xây dựng chuỗi lệnh
    command_line = f'"{exe_path}" "{source_file}" "{destination_file}"'
    # Cấu hình khởi tạo STARTUPINFO
    startup_info = ctypes.create_string_buffer(68)  # Kích thước cố định cho STARTUPINFO
    process_info = ctypes.create_string_buffer(16)  # Kích thước cố định cho PROCESS_INFORMATION

    # Cờ tạo tiến trình
    creation_flags = 0x00000008  # CREATE_NO_WINDOW

    # Gọi CreateProcess để tạo tiến trình con
    result = kernel32.CreateProcessA(
        None,  # Module (None -> sử dụng command line)
        ctypes.create_string_buffer(command_line.encode('utf-8')),
        None,  # Process security attributes
        None,  # Thread security attributes
        False,  # Inherit handles
        creation_flags,  # Creation flags
        None,  # Environment
        None,  # Current directory
        ctypes.byref(startup_info),  # Startup info
        ctypes.byref(process_info),  # Process info
    )

    if result == 0:
        error_code = kernel32.GetLastError()
        raise OSError(f"Failed to start process. Error code: {error_code}")

    print("Process started successfully.")

def list_files_in_directory(directory):
    """
    Quét tất cả các file trong thư mục và các thư mục con, trả về danh sách đường dẫn tuyệt đối của file.

    Args:
        directory (str): Đường dẫn tới thư mục cần quét.

    Returns:
        list: Danh sách chứa đường dẫn tuyệt đối của tất cả các file.
    """
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(os.path.abspath(file_path))
    return file_list


def encode ():
    files = list_files_in_directory("D:\\encryption test")
    for i in files:
        print(i)
        call_encode_subprocess(["./encode.exe", "985570", i, i+".lock"])
        

def decode ():
    files = list_files_in_directory("D:\\encryption test")
    for i in files:
        call_decode_subprocess("./decode.exe", i, i.rstrip(".lock"))

