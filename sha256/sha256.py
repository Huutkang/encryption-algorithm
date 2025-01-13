import pygame
import pygame.font
from hashlib import sha256
import time

pygame.init()
pygame.font.init()

WIDTH = 1200
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SHA-256 Algorithm Visualization")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (173, 216, 230)

FONT_SIZE = 20
font = pygame.font.SysFont('Segoe UI Symbol', FONT_SIZE)
title_font = pygame.font.SysFont('Arial', 30, bold=True)
small_font = pygame.font.SysFont('Segoe UI Symbol', 16)

class BinaryConverter:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.current_char = ""
        self.current_ascii = 0
        self.current_binary = ""
        self.show_conversion = False
        self.animation_step = 0
        self.last_update = 0
        
    def start_conversion(self, char):
        self.current_char = char
        self.current_ascii = ord(char)
        self.current_binary = format(self.current_ascii, '08b')
        self.show_conversion = True
        self.animation_step = 0
        self.last_update = time.time()
        
    def update(self):
        if not self.show_conversion:
            return
            
        current_time = time.time()
        if current_time - self.last_update > 0.2:  
            self.animation_step += 1
            self.last_update = current_time
            
        if self.animation_step > 10:
            self.show_conversion = False
            
    def draw(self, screen):
        if not self.show_conversion:
            return
        char_text = font.render(f"Character: '{self.current_char}'", True, BLACK)
        screen.blit(char_text, (self.x, self.y - 30))
        
        if self.animation_step >= 1:
            ascii_text = font.render(f"ASCII: {self.current_ascii}", True, BLUE)
            screen.blit(ascii_text, (self.x + 200, self.y - 30))
        
        if self.animation_step >= 2:
            binary_y = self.y + 10
            title = font.render("Binary conversion:", True, BLACK)
            screen.blit(title, (self.x, binary_y))

            step_y = binary_y + 30
            ascii_num = self.current_ascii
            for i in range(8):
                if self.animation_step >= i + 2:
                    bit = (ascii_num >> (7-i)) & 1
                    step_text = small_font.render(f"Step {i+1}: {ascii_num} ÷ 2 = {ascii_num//2} remainder {bit}", True, BLUE)
                    screen.blit(step_text, (self.x + 20, step_y + i*20))
                    ascii_num = ascii_num // 2
            
            if self.animation_step >= 10:
                result_text = font.render(f"Final binary: {self.current_binary}", True, GREEN)
                screen.blit(result_text, (self.x, step_y + 160))

class SHA256Visualizer:
    def __init__(self):
        self.message = ""
        self.current_step = 0
        self.total_steps = 6
        self.binary_message = ""
        self.padded_message = ""
        self.blocks = []
        self.final_hash = ""
        self.binary_converter = BinaryConverter(50, 150)
        self.current_char_index = 0
        self.conversion_complete = False
        self.binary_result = []
        self.w_values = [0] * 64
        self.current_w = 0
        self.calculation_h = 0
        self.scroll_offset = 0
        self.k_scroll_offset = 0
        self.last_w_update = 0
        self.w_update_delay = 0.2
        self.final_step5 = False
        self.input_box = pygame.Rect(100, 350, 600, 50)  # Input box lớn hơn
        self.button_box = pygame.Rect(750, 350, 150, 50)  # Nút "Visualize" lớn hơn
        self.color = pygame.Color('dodgerblue2')
        self.button_color = pygame.Color('lightgreen')
        self.text = self.message
        
    def update_message(self, msg):
        self.message = msg
        self.current_step = 0
        self.binary_message = ""
        self.current_char_index = 0
        self.conversion_complete = False
        self.binary_result = []
        if len(msg) > 0:
            self.binary_converter.start_conversion(msg[0])
        
        msg_len_bits = len(msg) * 8
        k = (448 - msg_len_bits - 1) % 512
        self.padded_message = ''.join(format(ord(c), '08b') for c in msg) + '1' + '0' * k + format(msg_len_bits, '064b')
        
        self.blocks = [self.padded_message[i:i+512] for i in range(0, len(self.padded_message), 512)]
        
        self.final_hash = sha256(msg.encode()).hexdigest()

    def next_step(self):
        if self.current_step < self.total_steps and (self.conversion_complete or self.current_step == 0):
            self.current_step += 1

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            if self.current_step == 0:
                self.current_char_index = 0
                self.conversion_complete = False
                if len(self.message) > 0:
                    self.binary_converter.start_conversion(self.message[0])

    def update(self):
        self.binary_converter.update()
        
        if self.current_step == 1 and not self.conversion_complete:
            if not self.binary_converter.show_conversion:
                if self.current_char_index < len(self.message) - 1:
                    self.current_char_index += 1
                    self.binary_converter.start_conversion(self.message[self.current_char_index])
                    self.binary_result.append(format(ord(self.message[self.current_char_index-1]), '08b'))
                else:
                    if len(self.message) > 0:
                        self.binary_result.append(format(ord(self.message[-1]), '08b'))
                    self.conversion_complete = True

    def draw(self, screen):
        screen.fill(WHITE)
        
        title = title_font.render("SHA-256 Algorithm Visualization", True, BLACK)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))

        if self.current_step == 0:
            self.text = self.message
            txt_surface = font.render(self.text, True, pygame.Color('black'))
            width = max(600, txt_surface.get_width() + 10)
            text = title_font.render("Enter a message to hash:", True, BLACK)
            screen.blit(text, (self.input_box.x , self.input_box.y - 40))
            self.input_box.w = width
            screen.blit(txt_surface, (self.input_box.x + 10, self.input_box.y + 10))
            pygame.draw.rect(screen, self.color, self.input_box, 3)

            pygame.draw.rect(screen, self.button_color, self.button_box)
            button_text = title_font.render("Visualize", True, pygame.Color('black'))
            screen.blit(button_text, (self.button_box.x + 15, self.button_box.y + 10))

        if self.current_step > 0:
            msg_text = font.render(f"Input Message: {self.message}", True, BLACK)
            screen.blit(msg_text, (50, 50))

        if self.current_step == 1 or self.current_step == 2 or self.current_step == 3:
            step_text = font.render("Step 1: Convert characters to binary", True, BLUE)
            screen.blit(step_text, (50, 90))
            
            if not self.conversion_complete:
                self.binary_converter.draw(screen)
            
            if len(self.binary_result) > 0:
                if self.conversion_complete:
                    result_y = 160
                    complete_binary = ''.join(self.binary_result)
                    # Giới hạn hiển thị chuỗi binary
                    max_display_length = 70
                    
                    if len(complete_binary) > max_display_length:
                        display_binary = complete_binary[:35] + "..." + complete_binary[-35:]
                    else:
                        display_binary = complete_binary
                    
                    # Render chuỗi
                    final_text = font.render("Final binary string:", True, BLACK)
                    screen.blit(final_text, (50, result_y - 40))
                    screen.blit(font.render(display_binary, True, GREEN), (70, result_y - 10))
                else:
                    result_y = 400
                    result_text = font.render("Converted results:", True, BLACK)
                    screen.blit(result_text, (50, result_y - 20 ))
                    
                    for i, binary in enumerate(self.binary_result):
                        char_text = font.render(f"'{self.message[i]}' = {binary}", True, GREEN)
                        if (i<15):
                            screen.blit(char_text, (70, result_y + i*25))
                        elif (i<30):
                            screen.blit(char_text, (250, result_y + (i-15)*25))
                        elif (i<45):
                            screen.blit(char_text, (430, result_y + (i-30)*25))
                        elif (i<60):
                            screen.blit(char_text, (610, result_y + (i-45)*25))
                        elif (i<75):
                            screen.blit(char_text, (790, result_y + (i-60)*25))
        
        if self.current_step == 2 or self.current_step == 3:
            self.draw_step2(screen)
        if self.current_step == 3:
            self.current_w = 0
            self.draw_step3(screen)
        if self.current_step == 4:
            self.draw_step3b(screen)
            self.draw_step4(screen)
            self.calculation_h = 0
            self.final_step5 = False
            if self.current_w < 63:
                current_time = time.time()
                if current_time - self.last_w_update > self.w_update_delay:  
                    self.last_w_update = current_time
                    self.current_w += 1
        if self.current_step >= 5:
            self.draw_step5(screen)
            if self.calculation_h < 63:
                current_time = time.time()
                if current_time - self.last_w_update > self.w_update_delay:  
                    self.last_w_update = current_time
                    self.calculation_h += 1
            else:
                self.final_step5 = True
            
    def draw_step2(self, screen):
        y = 180  
        text = font.render("Step 2: Padding", True, BLUE)
        screen.blit(text, (50, y))
        
        padding_y = y + 30
        msg_binary = ''.join(self.binary_result)
        max_display_length = 70
        
        if len(msg_binary) > max_display_length:
            display_binary = msg_binary[:35] + "..." + msg_binary[-35:]
        else:
            display_binary = msg_binary
        padding_one = font.render("Add '1' bit:", True, BLACK)
        screen.blit(padding_one, (50, padding_y))
        screen.blit(font.render(display_binary + "1", True, GREEN), (70, padding_y + 25))
        
        padding_zeros = font.render("Add '0' padding:", True, BLACK)
        screen.blit(padding_zeros, (50, padding_y + 50))
        padding_preview = self.padded_message[:-64]
        screen.blit(font.render(padding_preview[:35] + "..." + padding_preview[-35:], True, GREEN), 
                   (70, padding_y + 75))
        
        length_bits = font.render("Add message length (64 bits):", True, BLACK)
        screen.blit(length_bits, (50, padding_y + 100))
        screen.blit(font.render(self.padded_message[-64:], True, GREEN), 
                   (70, padding_y + 125))

    def draw_step3(self, screen):
        y = 355
        text = font.render("Step 3: Split into 512-bit blocks", True, BLUE)
        screen.blit(text, (50, y))

        block_y = y + 25
        for i, block in enumerate(self.blocks):
            if i >= 4:  
                overflow_text = font.render(f"... ({len(self.blocks) - 4} more blocks)", True, GRAY)
                screen.blit(overflow_text, (50, block_y + i * 25))
                break
            block_preview = block[:32] + "..." + block[-32:]  
            block_text = font.render(f"Block {i+1}: {block_preview} ({len(block)} bits)", True, BLACK)
            screen.blit(block_text, (50, block_y + i * 25))

    def draw_step3b(self, screen):
        y = 90
        text = font.render("Step 3: Split into 512-bit blocks", True, BLUE)
        screen.blit(text, (50, y))

        block_y = y + 25
        for i, block in enumerate(self.blocks):
            if i >= 4:  
                overflow_text = font.render(f"... ({len(self.blocks) - 4} more blocks)", True, GRAY)
                screen.blit(overflow_text, (50, block_y + i * 25))
                break
            block_preview = block[:32] + "..." + block[-32:]  
            block_text = font.render(f"Block {i+1}: {block_preview} ({len(block)} bits)", True, BLACK)
            screen.blit(block_text, (50, block_y + i * 25))
        
    def draw_step4(self, screen):
        y = 135
        text = font.render("Step 4: Message Schedule (W Array)", True, BLUE)
        screen.blit(text, (50, y))
        
        w_y = y + 30
        block = self.blocks[0]
        
        for i in range(16):
            self.w_values[i] = int(block[i*32:(i+1)*32], 2)
        
        def right_rotate(value, amount):
            return ((value >> amount) | (value << (32 - amount))) & 0xFFFFFFFF

        def sigma0(x):
            return right_rotate(x, 7) ^ right_rotate(x, 18) ^ (x >> 3)

        def sigma1(x):
            return right_rotate(x, 17) ^ right_rotate(x, 19) ^ (x >> 10)
        
        sigma0_text1 = font.render("σ₀(x) = (x >> 7) ⊕ (x ≫ 18) ⊕ (x ≫ 3)", True, BLACK)
        sigma1_text1 = font.render("σ₁(x) = (x ≫ 17) ⊕ (x ≫ 19) ⊕ (x ≫ 10)", True, BLACK)
        screen.blit(sigma0_text1, (400, 300))
        screen.blit(sigma1_text1, (400, 325))

        for i in range(16, 64):
            if i <= self.current_w:
                w_i_minus_2 = self.w_values[i - 2]
                w_i_minus_7 = self.w_values[i - 7]
                w_i_minus_15 = self.w_values[i - 15]
                w_i_minus_16 = self.w_values[i - 16]
                
                new_w = (sigma1(w_i_minus_2) + w_i_minus_7 + sigma0(w_i_minus_15) + w_i_minus_16) & 0xFFFFFFFF
                self.w_values[i] = new_w

        w_display_y = w_y
        for i in range(max(0, self.current_w - 15), self.current_w + 1):
            if 0 <= i < 64:
                text = font.render(f"W{i}: {self.w_values[i]:08x}", True, BLACK)
                screen.blit(text, (50, w_display_y - self.scroll_offset))
                w_display_y += 30

        # Display calculation for current W
        calc_y = w_y + 500
        if 16 <= self.current_w < 64:
            i = self.current_w
            w_i_minus_2 = self.w_values[i - 2]
            w_i_minus_7 = self.w_values[i - 7]
            w_i_minus_15 = self.w_values[i - 15]
            w_i_minus_16 = self.w_values[i - 16]
            
            text = font.render(f"Calculating W{i}:", True, BLUE)
            screen.blit(text, (50, calc_y))
            
            formula = f"W{i} = σ₁(W{i-2}) + W{i-7} + σ₀(W{i-15}) + W{i-16}"
            text = font.render(formula, True, BLACK)
            screen.blit(text, (50, calc_y + 30))
            
            values = f"    = σ₁({w_i_minus_2:08x}) + {w_i_minus_7:08x} + σ₀({w_i_minus_15:08x}) + {w_i_minus_16:08x}"
            text = font.render(values, True, BLACK)
            screen.blit(text, (50, calc_y + 60))
            
            result = f"    = {self.w_values[i]:08x}"
            text = font.render(result, True, BLACK)
            screen.blit(text, (50, calc_y + 90))

        # Display K constants on the right
        k_y = y
        text = font.render("K Constants:", True, BLUE)
        screen.blit(text, (950, y))
        
        k_values = [
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        ]
        
        k_display_y = k_y + 30
        for i in range(max(0, self.current_w - 15), self.current_w + 1):
            if 0 <= i < 64:
                text = font.render(f"K{i}: {k_values[i]:08x}", True, BLACK)
                screen.blit(text, (950, k_display_y - self.k_scroll_offset))
                k_display_y += 30

    def draw_step5(self, screen):
        k_values = [
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        ]
        y = 90
        text = font.render("Step 5: Final Hash Computation", True, BLUE)
        screen.blit(text, (50, y))
        
        # Initial hash values (first 32 bits of the fractional parts of the square roots of the first 8 primes)
        h_values = [
            0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
            0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
        ]
        labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        
        # Display initial hash values
        initial_text = font.render("Initial Hash Values (a b c d e f g h):", True, BLACK)
        screen.blit(initial_text, (50, y + 40))
        
        x_start = 50
        y_start = y + 70
        x = x_start
        y = y_start
        max_width = 1200
        spacing_x = 130
        spacing_y = 40
        
        # Display initial values
        for i, value in enumerate(h_values):
            if x + spacing_x > max_width:
                x = x_start
                y += spacing_y
            h_text = font.render(f"{labels[i]}: {value:08x}", True, BLACK)
            screen.blit(h_text, (x, y))
            x += spacing_x

        def right_rotate(value, amount):
            return ((value >> amount) | (value << (32 - amount))) & 0xFFFFFFFF

        def ch(x, y, z):
            return (x & y) ^ (~x & z)

        def maj(x, y, z):
            return (x & y) ^ (x & z) ^ (y & z)

        def sigma0(x):
            return right_rotate(x, 2) ^ right_rotate(x, 13) ^ right_rotate(x, 22)

        def sigma1(x):
            return right_rotate(x, 6) ^ right_rotate(x, 11) ^ right_rotate(x, 25)

        # Main compression function
        working_vars = list(h_values)  # Create a copy of initial hash values
        a, b, c, d, e, f, g, h = working_vars
        
        for i in range(64):
            w = self.w_values[i]
            k = k_values[i]
            
            T1 = (h + sigma1(e) + ch(e, f, g) + k + w) & 0xFFFFFFFF
            T2 = (sigma0(a) + maj(a, b, c)) & 0xFFFFFFFF
            
            h = g
            g = f
            f = e
            e = (d + T1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (T1 + T2) & 0xFFFFFFFF

            if i == self.calculation_h:
                step_text = font.render(f"Round {i + 1} Calculations", True, BLUE)
                screen.blit(step_text, (50, y + 40))

                ch_result = ch(e, f, g)
                maj_result = maj(a, b, c)
                sigma0_result = sigma0(a)
                sigma1_result = sigma1(e)
                ch_math = font.render(f"Ch(e, f, g) = (e ∧ f) ⊕ (¬e ∧ g)", True, BLUE)
                screen.blit(ch_math, (50, y + 70))
                
                maj_math = font.render(f"Maj(a, b, c) = (a ∧ b) ⊕ (a ∧ c) ⊕ (b ∧ c)", True, BLUE)
                screen.blit(maj_math, (50, y + 100))

                sigma0_math = font.render(f"Σ₀(a) = (a ≫ 2) ⊕ (a ≫ 13) ⊕ (a ≫ 22)", True, BLUE)
                screen.blit(sigma0_math, (50, y + 130))

                sigma1_math = font.render(f"Σ₁(e) = (e ≫ 6) ⊕ (e ≫ 11) ⊕ (e ≫ 25)", True, BLUE)
                screen.blit(sigma1_math, (50, y + 160))

                t1_math = font.render(f"T₁ = h + Σ₁(e) + Ch(e, f, g) + K{i} + W{i}", True, BLUE)
                screen.blit(t1_math, (50, y + 190))

                t2_math = font.render(f"T₂ = Σ₀(a) + Maj(a, b, c)", True, BLUE)
                screen.blit(t2_math, (50, y + 220))

                ch_text = font.render(f"Ch(e, f, g) = ({e:08x} ∧ {f:08x}) ⊕ (¬{e:08x} ∧ {g:08x}) = {ch_result:08x}", True, BLACK)
                screen.blit(ch_text, (50, y + 180 + 70))

                maj_text = font.render(f"Maj(a, b, c) = ({a:08x} ∧ {b:08x}) ⊕ ({a:08x} ∧ {c:08x}) ⊕ ({b:08x} ∧ {c:08x}) = {maj_result:08x}", True, BLACK)
                screen.blit(maj_text, (50, y + 180 + 100))

                sigma0_text = font.render(f"Σ₀(a) = ({a:08x} ≫ 2) ⊕ ({a:08x} ≫ 13) ⊕ ({a:08x} ≫ 22) = {sigma0_result:08x}", True, BLACK)
                screen.blit(sigma0_text, (50, y + 180 + 130))

                sigma1_text = font.render(f"Σ₁(e) = ({e:08x} ≫ 6) ⊕ ({e:08x} ≫ 11) ⊕ ({e:08x} ≫ 25) = {sigma1_result:08x}", True, BLACK)
                screen.blit(sigma1_text, (50, y + 180 + 160))

                t1_text = font.render(f"T₁ = {h:08x} + {sigma1_result:08x} + {ch_result:08x} + {k:08x} + {w:08x} = {T1:08x}", True, BLACK)
                screen.blit(t1_text, (50, y + 180 + 190))

                t2_text = font.render(f"T₂ = {sigma0_result:08x} + {maj_result:08x} = {T2:08x}", True, BLACK)
                screen.blit(t2_text, (50, y + 180 + 220))

                update_text = font.render(
                    f"Updates: h=g, g=f, f=e, e=d+T₁, d=c, c=b, b=a, a=T₁+T₂",
                    True, BLUE
                )
                screen.blit(update_text, (50, y + 180 + 250))
                
                updated_text = font.render("Updated Values:", True, BLACK)
                screen.blit(updated_text, (50, y + 180 + 280))
                
                updated_values = font.render(
                    f"a: {a:08x}, b: {b:08x}, c: {c:08x}, d: {d:08x}, e: {e:08x}, f: {f:08x}, g: {g:08x}, h: {h:08x}",
                    True, GREEN
                )
                screen.blit(updated_values, (50, y + 180 + 310))

        # After all rounds, add the compressed chunk to the current hash value
        final_hash_values = [
            (a + h_values[0]) & 0xFFFFFFFF,
            (b + h_values[1]) & 0xFFFFFFFF,
            (c + h_values[2]) & 0xFFFFFFFF,
            (d + h_values[3]) & 0xFFFFFFFF,
            (e + h_values[4]) & 0xFFFFFFFF,
            (f + h_values[5]) & 0xFFFFFFFF,
            (g + h_values[6]) & 0xFFFFFFFF,
            (h + h_values[7]) & 0xFFFFFFFF
        ]

        if self.final_step5:
            final_text = font.render("Final Hash Values:", True, BLUE)
            screen.blit(final_text, (50, y + 180 + 340))

            x = 50
            for i, value in enumerate(final_hash_values):
                final_value_text = font.render(f"{labels[i]}: {value:08x}", True, BLACK)
                screen.blit(final_value_text, (x, y + 180 + 370))
                x += 135

            final_hash = ''.join(f"{value:08x}" for value in final_hash_values)
            hash_text = font.render(f"Final Hash: {final_hash}", True, BLUE)
            screen.blit(hash_text, (50, y + 180 + 400))

            hash_result = sha256(self.message.encode()).hexdigest()
            hash_result_text = font.render(f"SHA-256 Result: {hash_result}", True, BLUE)
            screen.blit(hash_result_text, (50, y + 180 + 430))

def main():
    visualizer = SHA256Visualizer()
    # visualizer.update_message("hello")
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif visualizer.current_step == 0:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        visualizer.message = visualizer.text[:-1]
                    elif event.key == pygame.K_RETURN:
                        visualizer.update_message(visualizer.text)
                        visualizer.next_step()
                    else:
                        visualizer.message += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if visualizer.button_box.collidepoint(event.pos):
                        visualizer.update_message(visualizer.text)
                        visualizer.next_step()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    visualizer.prev_step()
                elif event.key == pygame.K_RIGHT:
                    visualizer.next_step()
                elif event.key == pygame.K_ESCAPE:
                    visualizer.update_message("")
                    visualizer.current_step = 0
            
        visualizer.update()
        visualizer.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
