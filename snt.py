def is_prime(num):
    """Kiểm tra số nguyên tố."""
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def find_primes(limit):
    """Tìm n số nguyên tố đầu tiên."""
    primes = []
    num = 2
    while len(primes) < limit:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def write_primes_to_file(primes, filename="primes.txt"):
    """Ghi danh sách số nguyên tố vào file."""
    with open(filename, "w") as file:
        for prime in primes:
            file.write(f"{prime}\n")

# Tìm 10,000 số nguyên tố đầu tiên
primes = find_primes(100000)

# Ghi vào file
write_primes_to_file(primes)

print("Đã ghi 10,000 số nguyên tố đầu tiên vào file primes.txt!")
