#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>
#include <openssl/aes.h>
#include <fstream>
#include <vector>
#include <cstring>
#include <cstdio>
#include <cmath>

#define AES_KEYLEN 32
#define AES_BLOCK_SIZE 16

void handleErrors() {
    ERR_print_errors_fp(stderr);
    abort();
}

// Hàm kiểm tra số nguyên tố
bool is_prime(int n) {
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    for (int i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0) return false;
    }
    return true;
}

// Hàm giải mã chuỗi với làm tròn kết quả sqrt
void decode_string(char *key, const int encoded_key[], int key_length, int secret_key) {
    for (int i = 0; i < key_length; i++) {
        int position = i + 1;
        int modifier = secret_key % (i + 5); // Yếu tố biến đổi dựa trên key bí mật
        int decoded_value = encoded_key[i] ^ modifier; // XOR ngược lại với giá trị biến đổi

        if (is_prime(position)) {
            key[i] = (int)round(sqrt(decoded_value - 2)); // Làm tròn trước khi ép kiểu
        } else if (position >= 1 && position <= 10 && !is_prime(position)) {
            key[i] = decoded_value - 9;
        } else {
            key[i] = decoded_value + 3;
        }
    }
    key[key_length] = '\0'; // Đảm bảo chuỗi kết thúc bằng ký tự null
}

std::vector<unsigned char> aes_encrypt(const std::vector<unsigned char>& plaintext, unsigned char* key, unsigned char* iv) {
    EVP_CIPHER_CTX *ctx;
    std::vector<unsigned char> ciphertext(plaintext.size() + AES_BLOCK_SIZE);
    int len;
    int ciphertext_len;

    if (!(ctx = EVP_CIPHER_CTX_new())) handleErrors();
    if (1 != EVP_EncryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key, iv))
        handleErrors();
    if (1 != EVP_EncryptUpdate(ctx, ciphertext.data(), &len, plaintext.data(), plaintext.size()))
        handleErrors();
    ciphertext_len = len;
    if (1 != EVP_EncryptFinal_ex(ctx, ciphertext.data() + len, &len)) handleErrors();
    ciphertext_len += len;
    EVP_CIPHER_CTX_free(ctx);

    ciphertext.resize(ciphertext_len);
    return ciphertext;
}

std::vector<unsigned char> aes_decrypt(const std::vector<unsigned char>& ciphertext, unsigned char* key, unsigned char* iv) {
    EVP_CIPHER_CTX *ctx;
    std::vector<unsigned char> plaintext(ciphertext.size());
    int len;
    int plaintext_len;

    if (!(ctx = EVP_CIPHER_CTX_new())) handleErrors();
    if (1 != EVP_DecryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key, iv))
        handleErrors();
    if (1 != EVP_DecryptUpdate(ctx, plaintext.data(), &len, ciphertext.data(), ciphertext.size()))
        handleErrors();
    plaintext_len = len;
    if (1 != EVP_DecryptFinal_ex(ctx, plaintext.data() + len, &len)) handleErrors();
    plaintext_len += len;
    EVP_CIPHER_CTX_free(ctx);

    plaintext.resize(plaintext_len);
    return plaintext;
}

std::vector<unsigned char> readFile(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary);
    if (!file) {
        handleErrors();
    }
    return std::vector<unsigned char>((std::istreambuf_iterator<char>(file)),
                                      std::istreambuf_iterator<char>());
}

void writeFile(const std::string& filename, const std::vector<unsigned char>& data) {
    std::ofstream file(filename, std::ios::binary);
    if (!file) {
        handleErrors();
    }
    file.write(reinterpret_cast<const char*>(data.data()), data.size());
}

void encryptFile(const std::string& input_filename, const std::string& output_filename, unsigned char* key, unsigned char* iv) {
    std::vector<unsigned char> plaintext = readFile(input_filename);
    std::vector<unsigned char> ciphertext = aes_encrypt(plaintext, key, iv);
    writeFile(output_filename, ciphertext);
    // Xóa file gốc sau khi mã hóa
    std::remove(input_filename.c_str());
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        return 1;
    }
    
    if (std::strcmp(argv[1], "985570") != 0) {
        return 1;
    }

    // Mảng khóa được mã hóa
    int encoded_key[256] = {
        119, 3137, 11235, 74, 2600, 117, 2809, 114, 94, 62, 9605, 59, 6413, 109, 91, 119,
        7935, 62, 13000, 92, 62, 120, 5030, 112, 65, 45, 125, 62, 6899, 34, 9442, 99,
        -5, -36, -12, -22, 22, -36, -24, -34, 1, -40, 28, -14, -36, -36, 13, -34,
        -50, -24, -16, -46, 35, -50, -15, -2, -57, -32, 14, -46, 50, -60, -56, -14,
        -63, -36, 53, -38, -43, -42, 35, -70, 70, -12, -40, -62, -74, -64, 11, -74,
        -82, -24, 49, -78, -6, -2, -64, -82, 62, -80, -36, -14, -20, -36, -60, -82,
        6, -14, -9, -86, 35, -50, 29, -74, -70, -16, 4, -46, 22, -36, -82, -50,
        50, -70, -120, -62, -27, -118, -101, -90, -82, -74, -67, -46, -24, -116, 63, -122,
        -36, -56, 50, -14, -91, -132, -134, -102, 28, -54, 33, -110, -137, -116, -36, -42,
        -142, -36, -12, -70, 64, -148, 155, -86, -104, -40, -50, -142, 154, -74, -75, -142,
        -122, -12, 134, -158, -86, -82, 145, -106, -136, -50, -36, -78, 14, -6, -67, -2,
        -1, -64, 182, -174, 41, -156, -133, -170, -74, -36, -48, -110, -37, -20, 50, -130,
        71, -60, -94, -182, 122, -108, 136, -14, -142, -116, -132, -190, -89, -36, -23, -50,
        -125, -30, 195, -182, -214, -70, -185, -122, -103, -120, -173, -46, -182, -136, 123, -146,
        -210, -82, 220, -166, 150, -168, -217, -70, 193, -120, -76, -62, -86, -148, 239, -118,
        35, -228, -207, -214, -12, -82, -192, -74, -247, -190, 170, -174, -215, -24, -120, -242
    };

    char key[257]; // Chuỗi khôi phục có kích thước động
    int key_length = 256; // Độ dài key linh hoạt
    int secret_key = 977583; // Key bí mật

    // Giải mã key
    decode_string(key, encoded_key, key_length, secret_key);
    
    unsigned char aes_key[AES_KEYLEN];
    std::memcpy(aes_key, key, AES_KEYLEN); // Chuyển key sang unsigned char
    
    unsigned char iv[AES_BLOCK_SIZE] = {0};  // Khởi tạo IV tĩnh

    std::string input_filename = argv[2];
    std::string output_filename = argv[3];

    encryptFile(input_filename, output_filename, aes_key, iv);

    return 0;
}
