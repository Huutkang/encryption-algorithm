import pygame, time


def replace_char_at_index(original_string, index, replacement_char):
    """
    Thay thế ký tự tại vị trí index trong chuỗi ban đầu bằng ký tự mới.

    Args:
        original_string (str): Chuỗi ban đầu.
        index (int): Vị trí của ký tự cần thay thế (bắt đầu từ 0).
        replacement_char (str): Ký tự thay thế.

    Returns:
        str: Chuỗi mới sau khi thay thế ký tự.

    Raises:
        ValueError: Nếu index nằm ngoài phạm vi của chuỗi.
    """
    if not (0 <= index < len(original_string)):
        raise ValueError("Index nằm ngoài phạm vi của chuỗi.")

    if len(replacement_char) != 1:
        raise ValueError("Ký tự thay thế phải là một ký tự đơn lẻ.")

    # Tạo chuỗi mới với ký tự được thay thế
    new_string = original_string[:index] + replacement_char + original_string[index + 1:]
    return new_string


# Khởi tạo Pygame
pygame.init()

# Cấu hình màn hình và màu sắc
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Input Văn Bản Có Dấu")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Font chữ hỗ trợ Unicode
font = pygame.font.Font(pygame.font.match_font('Calibri'), 32)

# Nội dung ô nhập
input_text = ""
input_active = False  # Trạng thái ô nhập

t_old = time.time()
index=0
d=0
ss='xxxxxxxxxxxxxxx'
t2=234
x=False
# Vòng lặp chính
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Xử lý nhấp chuột
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 100 <= event.pos[0] <= 500 and 150 <= event.pos[1] <= 200:
                input_active = True  # Kích hoạt ô nhập
            else:
                input_active = False  # Vô hiệu hóa ô nhập

        
        # Xử lý nhập bàn phím
        if event.type == pygame.KEYDOWN and input_active:
            t_old = time.time()
        if event.type == pygame.KEYUP and input_active:
            t = time.time()-t_old
            
            if event.key == pygame.K_BACKSPACE:
                if (t<0.01):
                    if x==False:
                        x=True
                        ss=event.unicode
                        t2 = time.time()
                    d+=1
                    
                else:
                    input_text = input_text[:-1]  # Xóa ký tự cuối
            else:
                input_text += event.unicode  # Thêm ký tự Unicode
    if x:
        if (time.time()-t2>0.1):
            x=False
            input_text=replace_char_at_index(input_text,len(input_text)-d, ss)
            d=0
            print(input_text)
                
        # print(d)

        
    # Vẽ giao diện
    screen.fill(WHITE)

    # Vẽ ô nhập
    if input_active:
        pygame.draw.rect(screen, GRAY, (100, 150, 400, 50))
    else:
        pygame.draw.rect(screen, BLACK, (100, 150, 400, 50), 2)

    # Hiển thị văn bản trong ô nhập
    text_surface = font.render(input_text, True, BLACK)
    screen.blit(text_surface, (110, 160))

    # Cập nhật màn hình
    pygame.display.flip()

pygame.quit()
a=''
a.split()