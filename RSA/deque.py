from collections import deque

# Tạo deque với dữ liệu
dq = deque([10, 20, 30, 40])

# Xem tất cả các phần tử
print(dq)  # Output: deque([10, 20, 30, 40])

item = dq.popleft()

# Truy cập phần tử bằng chỉ số
print(dq[0])  # Output: 10 (phần tử đầu)
print(dq[-1])  # Output: 40 (phần tử cuối)

# Duyệt qua từng phần tử
for item in dq:
    print(item, end=" ")  # Output: 10 20 30 40
