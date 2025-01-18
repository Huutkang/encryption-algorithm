from Crypto.Cipher import AES
import os

AES_KEYLEN = 32
AES_BLOCK_SIZE = 16

def handle_errors(e):
    print(f"An error occurred: {e}")
    raise Exception("Error occurred during decryption.")

def aes_decrypt(ciphertext, key, iv):
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext)
        # Remove padding if necessary
        plaintext = plaintext.rstrip(b"\x00")
        return plaintext
    except Exception as e:
        handle_errors(e)

def read_file(filename):
    with open(filename, 'rb') as f:
        return f.read()

def write_file(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)

def change_file_extension(filename, new_extension):
    base_name, _ = os.path.splitext(filename)
    return base_name + new_extension

def main():
    key_str = "k8jD3m5hN2b7PqXwY6rV9tGfZ1c4S0ac"
    key = key_str.encode('utf-8')
    iv = b'\x00' * AES_BLOCK_SIZE  # Initialization vector with zeros

    input_filename = "x"  # Change file as needed

    encrypted_data = read_file(input_filename)
    decrypted_text = aes_decrypt(encrypted_data, key, iv)

    print("Decrypted data:")
    print(decrypted_text.decode('utf-8', errors='ignore'))  # Decode the plaintext if it is a string

if __name__ == "__main__":
    main()
