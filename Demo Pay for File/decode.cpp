#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>
#include <openssl/aes.h>
#include <fstream>
#include <iostream>
#include <vector>
#include <cstring>
#include <cstdio>

#define AES_KEYLEN 32
#define AES_BLOCK_SIZE 16

void handleErrors() {
    ERR_print_errors_fp(stderr);
    abort();
}

std::vector<unsigned char> aes_decrypt(const std::vector<unsigned char>& ciphertext, unsigned char* key, unsigned char* iv) {
    EVP_CIPHER_CTX *ctx;
    std::vector<unsigned char> plaintext(ciphertext.size());
    int len;
    int plaintext_len;

    if(!(ctx = EVP_CIPHER_CTX_new())) handleErrors();
    if(1 != EVP_DecryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key, iv))
        handleErrors();
    if(1 != EVP_DecryptUpdate(ctx, plaintext.data(), &len, ciphertext.data(), ciphertext.size()))
        handleErrors();
    plaintext_len = len;
    if(1 != EVP_DecryptFinal_ex(ctx, plaintext.data() + len, &len)) handleErrors();
    plaintext_len += len;
    EVP_CIPHER_CTX_free(ctx);

    plaintext.resize(plaintext_len);
    return plaintext;
}

std::vector<unsigned char> readFile(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary);
    return std::vector<unsigned char>((std::istreambuf_iterator<char>(file)),
                                      std::istreambuf_iterator<char>());
}

void writeFile(const std::string& filename, const std::vector<unsigned char>& data) {
    std::ofstream file(filename, std::ios::binary);
    file.write(reinterpret_cast<const char*>(data.data()), data.size());
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Sử dụng: " << argv[0] << " <file mã hóa> <file giải mã>" << std::endl;
        return 1;
    }

    std::string input_filename = argv[1];
    std::string output_filename = argv[2];

    std::string key_str = "k8jD3m5hN2b7PqXwY6rV9tGfZ1c4S0ac";
    unsigned char key[AES_KEYLEN];
    unsigned char iv[AES_BLOCK_SIZE] = {0};
    std::memset(key, 0, AES_KEYLEN);
    std::strncpy(reinterpret_cast<char*>(key), key_str.c_str(), AES_KEYLEN);

    try {
        std::vector<unsigned char> encrypted_data = readFile(input_filename);
        std::vector<unsigned char> decrypted_text = aes_decrypt(encrypted_data, key, iv);

        writeFile(output_filename, decrypted_text);

        std::cout << "Giải mã thành công, file đã lưu tại: " << output_filename << std::endl;

        if (std::remove(input_filename.c_str()) == 0) {
            std::cout << "Đã xóa file mã hóa: " << input_filename << std::endl;
        } else {
            std::cerr << "Không thể xóa file mã hóa: " << input_filename << std::endl;
        }
    } catch (const std::exception& e) {
        std::cerr << "Lỗi: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
