import random

def read_primes_from_file(filename="primes.txt"):
    """Đọc danh sách số nguyên tố từ file."""
    with open(filename, "r") as file:
        primes = [int(line.strip()) for line in file]
    return primes

def get_two_random_primes(primes):
    """Lấy hai số nguyên tố ngẫu nhiên từ danh sách."""
    return random.sample(primes, 2)

# Đọc danh sách số nguyên tố từ file
primes = read_primes_from_file()

# Lấy hai số nguyên tố ngẫu nhiên
prime1, prime2 = get_two_random_primes(primes)

print(f"Hai số nguyên tố ngẫu nhiên: {prime1}, {prime2}")
