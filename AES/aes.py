from AES.constant import S_BOX, RCON, INV_S_BOX

def to_matrix(data):
    return [[data[i * 4 + j] for j in range(4)] for i in range(4)]

def matrix_to_bytes(matrix):
    return bytes(sum(matrix, []))

def sub_bytes(matrix):
    # Thay thế từng byte trong trạng thái bằng giá trị tương ứng từ S_BOX
    return [[S_BOX[byte >> 4][byte & 0x0f] for byte in row] for row in matrix]

def shift_rows(matrix):
    return [row[i:] + row[:i] for i, row in enumerate(matrix)]

def galois_mult(a, b):
    """Phép nhân trong trường Galois GF(2^8)."""
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        high_bit_set = a & 0x80
        a <<= 1
        if high_bit_set:
            a ^= 0x1B  # Giảm mô-đun x^8 + x^4 + x^3 + x + 1
        b >>= 1
    return p & 0xFF

def mix_columns(matrix):
    """Thực hiện MixColumns trên ma trận trạng thái."""
    result = []
    for col in zip(*matrix):  # Xử lý theo từng cột
        result_col = [
            galois_mult(col[0], 2) ^ galois_mult(col[1], 3) ^ col[2] ^ col[3],
            col[0] ^ galois_mult(col[1], 2) ^ galois_mult(col[2], 3) ^ col[3],
            col[0] ^ col[1] ^ galois_mult(col[2], 2) ^ galois_mult(col[3], 3),
            galois_mult(col[0], 3) ^ col[1] ^ col[2] ^ galois_mult(col[3], 2),
        ]
        result.append(result_col)
    return [list(row) for row in zip(*result)]  # Chuyển cột về hàng

def key_expansion(key, rcon, s_box):
    num_rounds = 10  # Số vòng AES 128-bit
    round_keys = [key]  # Danh sách khóa vòng, bắt đầu từ khóa chính

    for round_num in range(1, num_rounds + 1):
        prev_key = round_keys[-1]

        # Lấy cột cuối của khóa trước đó
        last_column = [prev_key[i][3] for i in range(4)]

        # Thực hiện bước RotWord (dịch vòng lên trên 1 ô)
        rotated_column = last_column[1:] + last_column[:1]

        # Thực hiện SubBytes trên cột đã xoay
        sub_column = [s_box[byte >> 4][byte & 0x0F] for byte in rotated_column]

        # XOR với cột đầu của khóa trước đó và RCON
        first_column = [
            sub_column[i] ^ prev_key[i][0] ^ rcon[round_num - 1][i] for i in range(4)
        ]

        # Tạo khóa vòng mới từng cột
        new_key = [[0] * 4 for _ in range(4)]
        for i in range(4):
            if i == 0:
                new_key[i][0] = first_column[i]
            else:
                new_key[i][0] = prev_key[i][0] ^ new_key[i - 1][0]

        for j in range(1, 4):
            for i in range(4):
                new_key[i][j] = prev_key[i][j] ^ new_key[i][j - 1]

        round_keys.append(new_key)

    return round_keys

def add_round_key(state, key_matrix):
    return [[state[i][j] ^ key_matrix[i][j] for j in range(4)] for i in range(4)]

def inverse_shift_rows(matrix):
    # Đảo ngược ShiftRows: quay ngược các hàng
    return [row[-i:] + row[:-i] for i, row in enumerate(matrix)]

def inverse_sub_bytes(matrix):
    # Thay thế byte sử dụng bảng Inverse S-box
    return [[INV_S_BOX[byte >> 4][byte & 0x0F] for byte in row] for row in matrix]

def inverse_mix_columns(matrix):
    """Thực hiện Inverse MixColumns trên ma trận trạng thái."""
    result = []
    for col in zip(*matrix):  # Xử lý theo từng cột
        result_col = [
            galois_mult(col[0], 0x0E) ^ galois_mult(col[1], 0x0B) ^ galois_mult(col[2], 0x0D) ^ galois_mult(col[3], 0x09),
            galois_mult(col[0], 0x09) ^ galois_mult(col[1], 0x0E) ^ galois_mult(col[2], 0x0B) ^ galois_mult(col[3], 0x0D),
            galois_mult(col[0], 0x0D) ^ galois_mult(col[1], 0x09) ^ galois_mult(col[2], 0x0E) ^ galois_mult(col[3], 0x0B),
            galois_mult(col[0], 0x0B) ^ galois_mult(col[1], 0x0D) ^ galois_mult(col[2], 0x09) ^ galois_mult(col[3], 0x0E),
        ]
        result.append(result_col)
    return [list(row) for row in zip(*result)]  # Chuyển cột về hàng

def aes_encrypt_stepwise(plaintext, key):
    global visual_steps
    try:
        # Kiểm tra và xử lý key
        key = key.encode("utf-8")
        if len(key) != 16:
            return "Key must be 16 characters long (128-bit key required)"
        key_matrix = to_matrix(list(key))

        # Sinh các round keys
        round_keys = key_expansion(key_matrix, RCON, S_BOX)

        # Xử lý plaintext: chia thành các khối 16 byte
        blocks = [plaintext[i : i + 16] for i in range(0, len(plaintext), 16)]
        if len(blocks[-1]) < 16:
            # Padding khối cuối cùng nếu cần (PKCS7 Padding)
            padding_length = 16 - len(blocks[-1])
            blocks[-1] += chr(padding_length) * padding_length

        ciphertext_blocks = []  # Lưu kết quả ciphertext cho từng khối
        visual_steps = []  # Lưu các bước trực quan hóa cho tất cả khối

        # Thực hiện mã hóa cho từng khối
        for block_index, block in enumerate(blocks):
            # Chuyển block thành ma trận 4x4
            plaintext_matrix = to_matrix(list(block.encode("utf-8")))

            # Lưu trạng thái ban đầu
            visual_steps.append(
                (
                    f"Block {block_index + 1}: Initial State",
                    plaintext_matrix,
                    None,
                )
            )

            # Bắt đầu vòng lặp mã hóa
            state = plaintext_matrix

            # AddRoundKey đầu tiên
            previous_state = state
            state = add_round_key(state, round_keys[0])
            visual_steps.append(
                (
                    f"Block {block_index + 1}: AddRoundKey (Initial)",
                    previous_state,
                    state,
                )
            )

            # 9 vòng lặp trung gian
            for round_num in range(1, 10):
                # SubBytes
                previous_state = state
                state = sub_bytes(state)
                visual_steps.append(
                    (
                        f"Block {block_index + 1}: Round {round_num} SubBytes",
                        previous_state,
                        state,
                    )
                )

                # ShiftRows
                previous_state = state
                state = shift_rows(state)
                visual_steps.append(
                    (
                        f"Block {block_index + 1}: Round {round_num} ShiftRows",
                        previous_state,
                        state,
                    )
                )

                # MixColumns
                previous_state = state
                state = mix_columns(state)
                visual_steps.append(
                    (
                        f"Block {block_index + 1}: Round {round_num} MixColumns",
                        previous_state,
                        state,
                    )
                )

                # AddRoundKey
                previous_state = state
                state = add_round_key(state, round_keys[round_num])
                visual_steps.append(
                    (
                        f"Block {block_index + 1}: Round {round_num} AddRoundKey",
                        previous_state,
                        state,
                    )
                )

            # Vòng cuối cùng (không MixColumns)
            # SubBytes
            previous_state = state
            state = sub_bytes(state)
            visual_steps.append(
                (
                    f"Block {block_index + 1}: Final Round SubBytes",
                    previous_state,
                    state,
                )
            )

            # ShiftRows
            previous_state = state
            state = shift_rows(state)
            visual_steps.append(
                (
                    f"Block {block_index + 1}: Final Round ShiftRows",
                    previous_state,
                    state,
                )
            )

            # AddRoundKey
            previous_state = state
            state = add_round_key(state, round_keys[10])
            visual_steps.append(
                (
                    f"Block {block_index + 1}: Final Round AddRoundKey",
                    previous_state,
                    state,
                )
            )

            # Chuyển trạng thái cuối cùng thành ciphertext
            ciphertext_block = matrix_to_bytes(state)
            ciphertext_blocks.append(ciphertext_block)

        # Ghép tất cả các khối ciphertext lại thành chuỗi
        ciphertext = b"".join(ciphertext_blocks)

        # Trả về ciphertext cuối cùng dưới dạng hex
        return ciphertext.hex(), visual_steps
    except Exception as e:
        return f"Error: {e}"

def aes_decrypt_stepwise(ciphertext, key):
    global visual_steps
    try:
        # Kiểm tra và xử lý key
        key = key.encode("utf-8")
        if len(key) != 16:
            return "Key must be 16 characters long (128-bit key required)"
        key_matrix = to_matrix(list(key))

        # Sinh các round keys
        round_keys = key_expansion(key_matrix, RCON, S_BOX)

        # Chuyển ciphertext từ hex sang bytes và chia thành các khối 16 byte
        ciphertext_bytes = bytes.fromhex(ciphertext)
        blocks = [
            ciphertext_bytes[i : i + 16] for i in range(0, len(ciphertext_bytes), 16)
        ]

        plaintext_blocks = []  # Lưu kết quả plaintext cho từng khối
        visual_steps = []  # Lưu các bước trực quan hóa cho tất cả khối

        # Thực hiện giải mã cho từng khối
        for block_index, block in enumerate(blocks):
            # Chuyển block thành ma trận 4x4
            ciphertext_matrix = to_matrix(list(block))

            # Lưu trạng thái ban đầu
            visual_steps.append(
                (
                    f"Block {block_index + 1}: Initial State",
                    ciphertext_matrix,
                    None,
                )
            )

            # Bắt đầu vòng lặp giải mã
            state = ciphertext_matrix

            # AddRoundKey với khóa của vòng cuối
            previous_state = state
            state = add_round_key(state, round_keys[10])
            visual_steps.append(
                (
                    f"Block {block_index + 1}: AddRoundKey (Final Round)",
                    previous_state,
                    state,
                )
            )

            # Inverse ShiftRows
            previous_state = state
            state = inverse_shift_rows(state)
            visual_steps.append(
                (
                    f"Block {block_index + 1}: Final Round Inverse ShiftRows",
                    previous_state,
                    state,
                )
            )

            # Inverse SubBytes
            previous_state = state
            state = inverse_sub_bytes(state)
            visual_steps.append(
                (
                    f"Block {block_index + 1}: Final Round Inverse SubBytes",
                    previous_state,
                    state,
                )
            )

            # 9 vòng lặp trung gian
            for round_num in range(9, 0, -1):
                # AddRoundKey
                previous_state = state
                state = add_round_key(state, round_keys[round_num])
                visual_steps.append(
                    (
                        f"Block {block_index + 1}: Round {round_num} AddRoundKey",
                        previous_state,
                        state,
                    )
                )

                # Inverse MixColumns
                previous_state = state
                state = inverse_mix_columns(state)
                visual_steps.append(
                    (
                        f"Block {block_index + 1}: Round {round_num} Inverse MixColumns",
                        previous_state,
                        state,
                    )
                )

                # Inverse ShiftRows
                previous_state = state
                state = inverse_shift_rows(state)
                visual_steps.append(
                    (
                        f"Block {block_index + 1}: Round {round_num} Inverse ShiftRows",
                        previous_state,
                        state,
                    )
                )

                # Inverse SubBytes
                previous_state = state
                state = inverse_sub_bytes(state)
                visual_steps.append(
                    (
                        f"Block {block_index + 1}: Round {round_num} Inverse SubBytes",
                        previous_state,
                        state,
                    )
                )

            # AddRoundKey với khóa của vòng đầu
            previous_state = state
            state = add_round_key(state, round_keys[0])
            visual_steps.append(
                (
                    f"Block {block_index + 1}: AddRoundKey (Initial)",
                    previous_state,
                    state,
                )
            )

            # Chuyển trạng thái cuối cùng thành plaintext
            plaintext_block = matrix_to_bytes(state)
            plaintext_blocks.append(plaintext_block)

        # Ghép tất cả các khối plaintext lại thành chuỗi
        plaintext_bytes = b"".join(plaintext_blocks)

        # Loại bỏ padding (PKCS7)
        padding_length = plaintext_bytes[-1]
        plaintext_bytes = plaintext_bytes[:-padding_length]

        # Trả về plaintext đã giải mã (dạng UTF-8)
        return plaintext_bytes.decode("utf-8"), visual_steps
    except Exception as e:
        return f"Error: {e}"
