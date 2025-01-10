import pygame
import sys
from aes import aes_encrypt_stepwise,aes_decrypt_stepwise

def main():
    pygame.init()
    # Constants for the GUI
    WIDTH, HEIGHT = 800, 700
    BG_COLOR = (255, 255, 255)
    TEXT_COLOR = (0, 0, 0)
    BUTTON_COLOR = (100, 150, 250)
    BUTTON_HOVER_COLOR = (70, 120, 220)
    FONT_SIZE = 20
    MATRIX_COLOR = (200, 200, 250)
    MATRIX_TEXT_COLOR = (50, 50, 150)

    # Initialize Pygame
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("AES Visualization Tool")
    font = pygame.font.Font(None, FONT_SIZE)

    # Input/output variables
    plaintext = ""
    key = ""
    ciphertext = ""
    plaintext_decrypt = ""
    visual_steps = []
    current_step = 0
    encryption_complete = False
    decryption_complete = False
    # Rects for input fields and buttons
    plaintext_rect = pygame.Rect(50, 50, 700, 40)
    key_rect = pygame.Rect(50, 120, 700, 40)
    ciphertext_rect = pygame.Rect(50, 190, 700, 40)
    decrypt_plaintext_rect = pygame.Rect(50, 260, 700, 40)
    encode_button_rect = pygame.Rect(200, 330, 120, 40)
    decode_button_rect = pygame.Rect(200,330,120,40)
    reset_button_rect = pygame.Rect(340, 330, 120, 40)
    exit_button_rect = pygame.Rect(480, 330, 120, 40)
    next_button_rect = pygame.Rect(660, 330, 120, 40)
    back_button_rect = pygame.Rect(50, 330, 100, 40)  # Back button
    encrypt_now_button_rect = pygame.Rect(620, 500, 150, 40)  # Encrypt Now button
    decrypt_now_button_rect = pygame.Rect(620, 500, 150, 40)  # Decrypt Now button

    # Focus control
    focused_input = None

    def draw_text(text, rect, focused):
        color = (230, 230, 230) if focused else BG_COLOR
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)
        rendered_text = font.render(text, True, TEXT_COLOR)
        screen.blit(rendered_text, (rect.x + 5, rect.y + 5))

    def draw_button(text, rect, hover):
        color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
        pygame.draw.rect(screen, color, rect)
        rendered_text = font.render(text, True, (255, 255, 255))
        text_rect = rendered_text.get_rect(center=rect.center)
        screen.blit(rendered_text, text_rect)

    def draw_matrix(matrix, x, y, highlight=False):
        for row in range(4):
            for col in range(4):
                pygame.draw.rect(screen, MATRIX_COLOR, (x + col * 50, y + row * 50, 50, 50))
                pygame.draw.rect(screen, (0, 0, 0), (x + col * 50, y + row * 50, 50, 50), 1)
                value = matrix[row][col]
                rendered_text = font.render(f"{value:02x}", True, MATRIX_TEXT_COLOR)
                text_rect = rendered_text.get_rect(
                    center=(x + col * 50 + 25, y + row * 50 + 25)
                )
                screen.blit(rendered_text, text_rect)
    def draw_arrow(x, y, length=100, height=20, color=(0, 0, 0)):
        # Tọa độ cho thân mũi tên (hình chữ nhật)
        body_rect = pygame.Rect(x, y - height // 4, length - height, height // 2)
        pygame.draw.rect(screen, color, body_rect)

        # Tọa độ cho đầu mũi tên (hình tam giác)
        tip_points = [
            (x + length - height, y - height // 2),  # Đỉnh trên của tam giác
            (x + length, y),  # Đỉnh nhọn
            (x + length - height, y + height // 2),  # Đỉnh dưới của tam giác
        ]
        pygame.draw.polygon(screen, color, tip_points)

    # Main loop
    running = True
    decryption_mode = False  # Thêm trạng thái để kiểm tra chế độ mã hóa hay giải mã

    while running:
        screen.fill(BG_COLOR)

        # Draw text fields and labels
        draw_text(plaintext, plaintext_rect, focused_input == "plaintext")
        draw_text(key, key_rect, focused_input == "key")

        # Hiển thị các nhãn và trường nhập liệu
        label_plaintext = font.render("Plaintext:", True, TEXT_COLOR)
        label_key = font.render("Key:", True, TEXT_COLOR)
        label_ciphertext = font.render("Ciphertext:", True, TEXT_COLOR)
        label_decrypted_plaintext = font.render("Decrypted Plaintext:", True, TEXT_COLOR)

        screen.blit(label_plaintext, (plaintext_rect.x, plaintext_rect.y - 25))
        screen.blit(label_key, (key_rect.x, key_rect.y - 25))
        screen.blit(label_ciphertext, (ciphertext_rect.x, ciphertext_rect.y - 25))
        screen.blit(
            label_decrypted_plaintext,
            (decrypt_plaintext_rect.x, decrypt_plaintext_rect.y - 25),
        )

        # Draw buttons
        if not decryption_mode:
            mouse_pos = pygame.mouse.get_pos()
            draw_button(
                "Encrypt",
                encode_button_rect,
                encode_button_rect.collidepoint(mouse_pos),
            )
        else:
            mouse_pos = pygame.mouse.get_pos()
            draw_button(
                "Decrypt",
                decode_button_rect,
                decode_button_rect.collidepoint(mouse_pos),
            )
        draw_button("Reset", reset_button_rect, reset_button_rect.collidepoint(mouse_pos))
        draw_button("Exit", exit_button_rect, exit_button_rect.collidepoint(mouse_pos))
        draw_button("Next", next_button_rect, next_button_rect.collidepoint(mouse_pos))
        draw_button("Back", back_button_rect, back_button_rect.collidepoint(mouse_pos))
        if not decryption_mode:
            draw_button(
                "Encrypt Now",
                encrypt_now_button_rect,
                encrypt_now_button_rect.collidepoint(mouse_pos),
            )
        else:
            draw_button(
                "Decrypt Now",
                decrypt_now_button_rect,
                decrypt_now_button_rect.collidepoint(mouse_pos),
            )

        # Draw matrices and arrow for visualization
        if current_step < len(visual_steps):
            label_step, matrix_before, matrix_after = visual_steps[current_step]

            # Draw labels for the current step
            step_text = font.render(label_step, True, TEXT_COLOR)
            screen.blit(step_text, (50, 300))

            # Draw before and after matrices
            if matrix_before:
                draw_matrix(matrix_before, 50, 450)
            if matrix_after:
                draw_matrix(matrix_after, 400, 450)
                draw_arrow(270, 550, length=120, height=40, color=(0, 0, 0))

        # Display final ciphertext or plaintext
        if encryption_complete:
            draw_text(ciphertext, ciphertext_rect, False)
        if decryption_complete:
            draw_text(plaintext_decrypt, decrypt_plaintext_rect, False)
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if plaintext_rect.collidepoint(event.pos):
                    focused_input = "plaintext"
                elif key_rect.collidepoint(event.pos):
                    focused_input = "key"
                elif encode_button_rect.collidepoint(
                    event.pos
                ) or decode_button_rect.collidepoint(event.pos):
                    if plaintext and key:
                        if not decryption_mode:
                            ciphertext, visual_steps = aes_encrypt_stepwise(plaintext, key)
                            encryption_complete = False
                        else:
                            plaintext_decrypt, visual_steps = aes_decrypt_stepwise(ciphertext, key)
                            decryption_complete = False
                        current_step = 0
                    else:
                        ciphertext = "Error: Provide valid input and key."
                elif reset_button_rect.collidepoint(event.pos):
                    plaintext = ""
                    key = ""
                    ciphertext = ""
                    plaintext_decrypt = ""
                    visual_steps = []
                    current_step = 0
                    encryption_complete = False
                    decryption_mode = False  # Reset chế độ về mã hóa
                    decryption_complete = False
                elif exit_button_rect.collidepoint(event.pos):
                    running = False  # Thoát vòng lặp chính
                    pygame.quit()     # Kết thúc pygame
                elif next_button_rect.collidepoint(event.pos) and current_step < len(
                    visual_steps
                ):
                    current_step += 1
                    if current_step == len(visual_steps):  # Khi hoàn thành tất cả các bước mã hóa
                        if not decryption_mode:
                            encryption_complete = True
                            decryption_mode = True
                        else:
                            decryption_complete = True
                        #   # Chuyển sang chế độ giải mã         
                elif back_button_rect.collidepoint(event.pos) and current_step > 0:
                    # Go back to the previous step
                    current_step -= 1
                    if current_step == len(visual_steps)-1:
                        if encryption_complete and not decryption_complete:
                            decryption_mode = False
                        elif decryption_complete:
                            decryption_complete = True
                elif encrypt_now_button_rect.collidepoint(event.pos) or decrypt_now_button_rect.collidepoint(event.pos):
                    if not decryption_mode:
                        ciphertext, visual_steps = aes_encrypt_stepwise(
                            plaintext, key
                        )  # Encrypt without steps
                        encryption_complete = True
                        decryption_mode = True
                    else:
                        plaintext_decrypt, visual_steps = aes_decrypt_stepwise(
                            ciphertext, key
                        )  # Decrypt without steps
                        decryption_complete = True

                    current_step = len(visual_steps)  # Skip all steps
                else:
                    focused_input = None

            elif event.type == pygame.KEYDOWN and focused_input:
                if event.key == pygame.K_BACKSPACE:
                    if focused_input == "plaintext":
                        plaintext = plaintext[:-1]
                    elif focused_input == "key":
                        key = key[:-1]
                else:
                    if focused_input == "plaintext":
                        plaintext += event.unicode
                    elif focused_input == "key" and len(key) < 16:
                        key += event.unicode

        pygame.display.flip()
    pygame.quit()
    sys.exit()
    pass

if __name__ == "__main__":
    main()
