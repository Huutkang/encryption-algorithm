import random
from prime import PrimeNumberUtils

class RSA(object):
    """
    Lớp đại diện cho thuật toán RSA
    """

    def __init__(self, keysize=64, test=False):
        self.snt = PrimeNumberUtils()
        self.e, self.d, self.N = 0, 0, 0
        if not test:
            self.keysize = keysize
            self.generateKeys(self.keysize)

    def generateKeys(self, keysize=128):
        """
        Sinh cặp khóa RSA (e, d, N) với keysize bit
        """
        p = self.snt.generateLargePrime(keysize)
        q = self.snt.generateLargePrime(keysize)

        self.N = self.calculateN(p, q)
        phiN = self.calculatePhiN(p, q)

        self.e = self.selectE(phiN, keysize)
        self.d = self.calculateD(self.e, phiN)

        self.p, self.q = p, q
    
    @staticmethod
    def calculateN(p, q):
        """
        Tính N = p * q
        """
        return p * q

    @staticmethod
    def calculatePhiN(p, q):
        """
        Tính hàm Euler phi(N) = (p-1) * (q-1)
        """
        return (p - 1) * (q - 1)

    def selectE(self, phiN, keysize):
        """
        Chọn số e thỏa mãn gcd(e, phiN) = 1
        """
        while True:
            e = random.randrange(2 ** (keysize - 1), 2 ** keysize - 1)
            if self.isCoPrime(e, phiN):
                return e

    def calculateD(self, e, phiN):
        """
        Tính d là nghịch đảo modular của e mod phiN
        """
        return RSA.modularInv(e, phiN)

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
