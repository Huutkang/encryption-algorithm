import random
from prime import PrimeNumberUtils



class RSA(object):
    """
    Lớp đại diện cho thuật toán RSA
    """

    def __init__(self, keysize=128):
        self.keysize = keysize
        self.snt = PrimeNumberUtils()
        self.generateKeys(self.keysize)

    def generateKeys(self, keysize=128):
        """
        Sinh cặp khóa RSA (e, d, N) với keysize bit
        """
        e = d = N = 0

        # Tạo hai số nguyên tố lớn p và q
        p = self.snt.generateLargePrime(keysize)
        q = self.snt.generateLargePrime(keysize)

        N = p * q  # Tích N = p * q
        phiN = (p - 1) * (q - 1)  # Tính hàm Euler phi(N)

        # Chọn số e thỏa mãn gcd(e, phiN) = 1
        while True:
            e = random.randrange(2 ** (keysize - 1), 2 ** keysize - 1)
            if RSA.isCoPrime(e, phiN):
                break

        # Tính d là nghịch đảo modular của e mod phiN
        d = RSA.modularInv(e, phiN)

        self.p, self.q, self.e, self.d, self.N = p, q, e, d, N

    @staticmethod
    def isCoPrime(p, q):
        """
        Kiểm tra xem p và q có nguyên tố cùng nhau không (gcd = 1)
        """
        return RSA.gcd(p, q) == 1

    @staticmethod
    def gcd(p, q):
        """
        Thuật toán Euclid để tìm ước chung lớn nhất (GCD)
        """
        while q:
            p, q = q, p % q
        return p

    @staticmethod
    def egcd(a, b):
        """
        Tìm GCD và các hệ số x, y sao cho ax + by = gcd(a, b)
        """
        s, old_s = 0, 1
        t, old_t = 1, 0
        r, old_r = b, a

        while r != 0:
            quotient = old_r // r
            old_r, r = r, old_r - quotient * r
            old_s, s = s, old_s - quotient * s
            old_t, t = t, old_t - quotient * t

        return old_r, old_s, old_t

    @staticmethod
    def modularInv(a, b):
        """
        Tính nghịch đảo modular của a mod b
        """
        gcd, x, _ = RSA.egcd(a, b)
        if x < 0:
            x += b
        return x

    def encrypt(self, msg):
        """
        Mã hóa một thông điệp
        Trả về mảng chứa danh sách các phần tử đã mã hóa
        """
        cipher = []
        for c in msg:
            m = ord(c)  # Lấy mã Unicode của ký tự đơn
            cipher.append(pow(m, self.e, self.N))  # Mã hóa từng ký tự
        return cipher

    def decrypt(self, cipher):
        """
        Giải mã một danh sách các phần tử đã mã hóa
        Trả về chuỗi thông điệp
        """
        msg = ""
        for c in cipher:
            msg += chr(pow(c, self.d, self.N))  # Giải mã từng ký tự
        return msg
