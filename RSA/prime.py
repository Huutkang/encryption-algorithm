import random


class PrimeNumberUtils:
    '''class PrimeNumberUtils xử lí công việc liên quan đến số nguyên tố'''
    
    def __init__(self, path="RSA/primes.txt"):
        self.lowPrimes = self.readPrimesFromFile(path)
    
    @staticmethod
    def isPrimeSimple(num):
        """Kiểm tra số nguyên tố."""
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

    @staticmethod
    def findPrimes(limit):
        """Tìm n số nguyên tố đầu tiên."""
        primes = []
        num = 2
        while len(primes) < limit:
            if PrimeNumberUtils.isPrimeSimple(num):
                primes.append(num)
            num += 1
        return primes

    @staticmethod
    def writePrimesToFile(primes, path):
        """Ghi danh sách số nguyên tố vào file."""
        with open(path, "w") as file:
            for prime in primes:
                file.write(f"{prime}\n")

    def generatePrimeNumbers(self, n, path="primes.txt"):
        '''Tạo n số nguyên tố đầu tiên và ghi vào file'''
        # Tìm n số nguyên tố đầu tiên
        primes = PrimeNumberUtils.findPrimes(n)
        # Ghi vào file
        PrimeNumberUtils.writePrimesToFile(primes, path)
        print("Đã ghi n số nguyên tố đầu tiên vào file primes.txt!")

    def readPrimesFromFile(self, path="RSA/primes.txt"):
        """Đọc danh sách số nguyên tố từ file."""
        with open(path, "r") as file:
            primes = [int(line.strip()) for line in file]
        return primes

    # ----------------------------------------------------------------
    
    @staticmethod
    def rabinMiller(n, d):
        """
        Thuật toán Rabin-Miller kiểm tra tính nguyên tố
        """
        a = random.randint(2, (n - 2) - 2)
        x = pow(a, int(d), n)  # Tính a^d % n
        if x == 1 or x == n - 1:
            return True

        # Lặp lại để kiểm tra thêm
        while d != n - 1:
            x = pow(x, 2, n)
            d *= 2

            if x == 1:
                return False
            elif x == n - 1:
                return True

        return False  # Không phải số nguyên tố


    def isPrime(self, n):
        """
        Kiểm tra xem n có phải số nguyên tố không
        """
        if n < 2:  # Số nhỏ hơn 2 không phải là số nguyên tố
            return False

        if n in self.lowPrimes:  # Nếu n nằm trong danh sách số nguyên tố nhỏ
            return True

        # Kiểm tra n có chia hết cho các số nguyên tố nhỏ không
        for prime in self.lowPrimes:
            if n % prime == 0:
                return False

        # Tìm c sao cho c * 2^r = n - 1
        c = n - 1
        while c % 2 == 0:
            c //= 2

        # Kiểm tra bằng thuật toán Rabin-Miller
        for _ in range(128):
            if not PrimeNumberUtils.rabinMiller(n, c):
                return False

        return True

    def generateLargePrime(self, keysize):
        """
        Tạo và trả về một số nguyên tố lớn với độ dài keysize (số bit)
        """
        while True:
            num = random.randrange(2 ** (keysize - 1), 2 ** keysize - 1)
            if self.isPrime(num):
                return num

