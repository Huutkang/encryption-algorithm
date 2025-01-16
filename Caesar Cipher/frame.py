import pygame
import sys, time
from CaesarCipher import CaesarCipher
from draw.input import Input
from draw.output import Output
from draw.char import Char
from draw.RotatingAlphabet import RotatingAlphabet

class SimulateCaesarCipher:

    running = True
    
    dis_width = 1200
    dis_height = 800
    
    # các biến cho gõ văn bản
    input_active = True
    input_text=''
    
    def __init__(self):
        # Khởi tạo Pygame
        pygame.init()
        self.caesarCipher = CaesarCipher(0)
        self.font = pygame.font.SysFont("Calibri", 20)
        self.screen = pygame.display.set_mode((self.dis_width, self.dis_height))
        pygame.display.set_caption("Caesar Cipher")
        self.clock = pygame.time.Clock()
        self.rotatingAlphabet = RotatingAlphabet([170, 500], color = "red")
        self.alphabet = RotatingAlphabet([170, 300], color="DeepSkyBlue1")
        self.ip = Input(512, 40, [200, 70], True)
        self.output1 = Output(512, 40, [300, 700], True)
        self.output2 = Output(512, 40, [300, 1100], True)
        self.pos = [0, 0]
        self.step = 0
        self.op1=''
        self.op2=''
        self.chars = []
        self.autoIp = False
        self.encodeOn = False
        self.deCodeOn = False
        self.t=0
        self.lockEnter = False

    def draw(self, obj):
        self.screen.blit(obj[0], obj[1])
    
    
    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # # Xử lý nhấp chuột
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.pos = (event.pos[0], event.pos[1])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if self.step==0:
                        self.rotatingAlphabet.rotate_right()
                        self.caesarCipher.decrease_shift()
                elif event.key == pygame.K_LEFT:
                    if self.step ==0:
                        self.rotatingAlphabet.rotate_left()
                        self.caesarCipher.increase_shift()
                elif event.key == pygame.K_RETURN:
                    self.eventEnter()
            
            # Xử lý nhập bàn phím
            if event.type == pygame.KEYDOWN and self.input_active:
                if event.key == pygame.K_BACKSPACE:
                    if len(self.input_text)>0:
                        self.input_text = self.input_text[:-1]
                else:
                    if len(self.input_text)<30:
                        if event.unicode.isalpha() or event.unicode.isspace():
                            self.input_text += event.unicode.upper()
                            self.input_text=self.input_text.replace('\r', '')

    def eventEnter(self):
        if self.lockEnter:
            return
        match self.step:
            case 0:
                if len(self.input_text)>0:
                    self.ip.setMove([-700, 0], 10)
                    self.chars = [Char(i, [400, -200]) for i in self.input_text]
                    for i in range(len(self.input_text)):
                        self.chars[i].setMove([200+32*i, 70], 4)
                    self.step += 1
                    self.op1=self.caesarCipher.encrypt(self.input_text)
                else:
                    self.indexAutoInput = 0
                    self.text_atip = 'CAESAR CIPHER'
                    self.t = time.time()
                    self.autoIp=True
                    self.lockEnter = True
            case 1:
                self.encodeOn=True
                self.indexEndcode=0
                self.step += 1
                self.lockEnter = True
            case 2:
                for i in self.chars:
                    i.xy = [400, -200]
                self.step += 1
            case 3:
                self.rotatingAlphabet.setMove([170, 300], 6)
                self.alphabet.setMove([170, 500], 6)
                self.output1.setMove([200, 70], 6)
                self.output2.setMove([300, 700], 6)
                self.step += 1
            case 4:
                for i in range(len(self.chars)):
                    self.chars[i].setMove([200+32*i, 70], 4)
                self.output2.setMove([300, 900], 3)
                self.step += 1
            case 5:
                self.deCodeOn=True
                self.indexDecode=0
                self.step += 1
                self.lockEnter = True
            case 6:
                self.output2.xy = [300, 700]
                self.chars.clear()
                self.step += 1
                self.op2=self.input_text
            case 7:
                self.output1.setMove([300, 700], 6)
                self.output2.setMove([300, 1100], 6)
                self.rotatingAlphabet.setMove([170, 500], 6)
                self.alphabet.setMove([170, 300], 6)
                self.input_text =''
                self.step = 0
                self.ip.setMove([200, 70], 10)
                self.indexEndcode=0
                self.indexDecode=0
                

    def checkDoneStep(self, step):
        for i in self.chars:
            if i.step<step:
                return False
        return True

    def encode(self):
        if self.encodeOn:
            if time.time() > self.t+2:
                if self.indexEndcode < len (self.chars):
                    self.t = time.time()
                    i=self.chars[self.indexEndcode]
                    if i.char ==" ":
                        i.step+=1
                        i.setMove([302+32*self.indexEndcode, 700], 2)
                    else:
                        i.setMove([170+32*(ord(i.char)-65), 300], 4)
                    i.step+=1
                    self.indexEndcode+=1
    
    def decode(self):
        if self.deCodeOn:
            if time.time() > self.t+2:
                if self.indexDecode < len (self.chars):
                    self.t = time.time()
                    i=self.chars[self.indexDecode]
                    if i.char ==" ":
                        i.step+=1
                        i.setMove([302+32*self.indexDecode, 700], 2)
                    else:
                        i.setMove([170+32*((ord(i.char)-65 - self.caesarCipher.shift)% 26), 300], 4)
                    i.step+=1
                    self.indexDecode+=1
    
    def move (self):
        self.rotatingAlphabet.move()
        self.alphabet.move()
        self.ip.move()
        self.output1.move()
        self.output2.move()
        self.encode()
        self.decode()
        for i in range(len(self.chars)):
            char = self.chars[i]
            kq=char.move()
            if kq and self.step==2:
                match char.step:
                    case 1:
                        char.step+=1
                        self.step_endcode = 0
                        char.setMove([170+32*(ord(char.char)-65), 500], 1)
                    case 2:
                        char.char = self.op1[i]
                        char.step+=1
                        char.setMove([302+32*i, 700], 4)
            if kq and self.step==6:
                match char.step:
                    case 4:
                        char.step+=1
                        char.setMove([170+32*((ord(char.char)-65 - self.caesarCipher.shift)% 26), 500], 1)
                    case 5:
                        char.char = self.input_text[i]
                        char.step+=1
                        char.setMove([302+32*i, 700], 4)

    def autoInput (self):
        if self.autoIp:
            if time.time() > self.t+0.1:
                self.t = time.time()
                self.input_text += self.text_atip[self.indexAutoInput]
                self.indexAutoInput += 1
                if self.indexAutoInput >= len(self.text_atip):
                    self.autoIp = False
                    self.lockEnter = False
    
    def update (self):
        self.draw(self.output2.update(input=self.op2))
        self.draw(self.ip.update(input = self.input_text))
        if self.step>3:
            self.draw(self.rotatingAlphabet.update())
        else:
            self.draw(self.alphabet.update())
        for i in self.chars:
            self.draw(i.update())
        match self.step:
            case 0:
                self.autoInput()
            case 3:
                self.draw(self.output1.update(input=self.op1))
            case 4:
                self.draw(self.output1.update(input=self.op1))
        if self.step<4:
            self.draw(self.rotatingAlphabet.update())
        else:
            self.draw(self.alphabet.update())
        if self.step == 2 and self.checkDoneStep(3):
            self.lockEnter = False
        if self.step == 6 and self.checkDoneStep(6):
            self.lockEnter = False
        
        text = self.font.render("Shift: "+str(self.caesarCipher.shift), True, "orange")
        self.screen.blit(text, (1100, 27))


    def checkInput(self):
        self.input_active = self.ip.checkInObj(self.pos)


    def run(self):
        while self.running:
            # Vẽ lên màn hình
            self.screen.fill("black")  # Xóa màn hình bằng màu đen
            self.checkInput()
            
            self.move()
            
            self.update()
            
            self.event()
            
            # Cập nhật màn hình
            pygame.display.flip()
            
            # Giới hạn FPS (90 khung hình/giây)
            self.clock.tick(90)

        # Thoát Pygame
        pygame.quit()
        sys.exit()


