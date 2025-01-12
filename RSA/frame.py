import pygame
import sys, time, random
from rsa import RSA
from draw.input import Input
from draw.output import Output
from draw.char import Char
from draw.ds import Ds
from draw.cme import Cme
from draw.mcd import Mcd
from draw.unicode import Unicode
from draw.button import Button
from draw.str import String


class SimulateRSA:

    running = True
    
    dis_width = 1200
    dis_height = 800
    
    # các biến cho gõ văn bản
    x = False 
    input_active = True
    input_text=''
    d=0
    t2=0
    ss=''
    
    pos=(0, 0)
    
    def __init__(self):
        # Khởi tạo Pygame
        pygame.init()
        self.rsa = RSA()

        self.screen = pygame.display.set_mode((self.dis_width, self.dis_height))
        pygame.display.set_caption("RSA")

        # Tạo đồng hồ để kiểm soát FPS
        self.clock = pygame.time.Clock()
        
        self.value = []
        
        self.ip = Input(512, 40)
        self.out = Output(512, 40)
        
        self.cme = Cme()
        self.mcd = Mcd()
        self.unicode = Unicode()
        
        self.bd = False
        
        self.button = Button()
        
        self.ds = Ds()
        
        self.index_prepare = 0
        self.t_go = 0
        
        
    def go(self):
        a = self.button.checkInObj(self.pos)
        if a:
            self.pos = [0, 0]
            if self.bd:
                self.bd = False
            else:
                self.bd = True
                self.initStr()
        if self.bd and time.time() > self.t_go+1:
            self.t_go = time.time()
            if len(self.input_text)>0:
                self.value[self.index_prepare][3].on = True
                self.value[self.index_prepare][3].setMove((355, 232), 3)
                self.value[self.index_prepare][4].on = False
                self.index_prepare += 1
                self.input_text = self.input_text[1:]
    
    def initStr(self):
        mh = self.rsa.encrypt(self.input_text)
        m=[]
        for i in range(len(self.input_text)):
            vb = self.input_text[i]
            m.append([vb, ord(vb), mh[i], Char(vb, type=1), String(str(mh[i]), type=2), String(str(ord(vb)), type=3)])
        self.value = m
        
        
    def draw(self, obj):
        self.screen.blit(obj[0], obj[1])
        
    def event(self):
        t1=0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # # Xử lý nhấp chuột
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.pos = (event.pos[0], event.pos[1])
                print(self.pos)
            
            # Xử lý nhập bàn phím
            if event.type == pygame.KEYDOWN and self.input_active:
                t1 = time.time()
            if event.type == pygame.KEYUP and self.input_active:
                t = time.time()-t1
                
                if event.key == pygame.K_BACKSPACE:
                    if (t<0.01):
                        if self.x==False:
                            self.x=True
                            self.ss=event.unicode
                            self.t2 = time.time()
                        self.d+=1
                        
                    else:
                        self.input_text = self.input_text[:-1]  # Xóa ký tự cuối
                else:
                    if len(self.input_text)<35:
                        self.input_text += event.unicode  # Thêm ký tự Unicode 
        if self.x:
            if (time.time()-self.t2>0.05):
                self.x=False
                self.input_text=SimulateRSA.replace_char_at_index(self.input_text,len(self.input_text)-self.d, self.ss)
                self.d=0
    
    def setStep(self, arr, step):
        for i in arr[3:]:
            i.step=step
    
    def move (self):
        for i in self.value:
            a=i[3].move()
            b=i[4].move()
            c=i[5].move()
            vt=self.ds.getCoordinates()
            if a:
                if (i[3].step==1):
                    self.setStep(i, 2)
                    i[3].setMove(vt, 3)
                    i[5].xy = [353, 241]
                    i[5].setMove((357, 374), 3)
                    i[5].on = True
                    self.setStep(i, 3)
            if c:
                if (i[5].step==3):
                    i[5].on = False
                    self.setStep(i, 4)
                    i[4].xy = [266, 398]
                    i[4].setMove((vt[0]+50, vt[1]+8), 3)
                    self.ds.append(i[0], str(i[2]))
                    i[4].on = True
            if b and c:
                if (i[5].step==4):
                    self.setStep(i, 5)
                    i[3].on = False
                    i[4].on = False
                    self.ds.unlock()
                    
                    
                
    def update (self):
        for i in self.value:
            if i[3].on:
                self.draw(i[3].update())
            if i[4].on:
                self.draw(i[4].update())
            if i[5].on:
                self.draw(i[5].update())
                
            
    def check (self):
        pass
    
    def checkInput(self):
        self.input_active = self.ip.checkInObj(self.pos)

    def run(self):
        while self.running:
            self.event()

            # Vẽ lên màn hình
            self.screen.fill("black")  # Xóa màn hình bằng màu đen
            self.checkInput()
            
            self.move()
            
            self.go()
                
            self.draw(self.ip.update([70, 90],input = self.input_text))
            self.draw(self.ds.update())
            self.draw(self.out.update([70, 720],input = 'meo meo'))
            
            self.draw(self.button.update())
            
            self.update()
            
            self.draw(self.cme.update())
            self.draw(self.mcd.update())
            self.draw(self.unicode.update())
                  
            # Cập nhật màn hình
            pygame.display.flip()
            
            # Giới hạn FPS (90 khung hình/giây)
            self.clock.tick(90)

        # Thoát Pygame
        pygame.quit()
        sys.exit()
    
    @staticmethod
    def replace_char_at_index(original_string, index, replacement_char):
        if not (0 <= index < len(original_string)):
            raise ValueError("Index nằm ngoài phạm vi của chuỗi.")

        if len(replacement_char) != 1:
            raise ValueError("Ký tự thay thế phải là một ký tự đơn lẻ.")

        # Tạo chuỗi mới với ký tự được thay thế
        new_string = original_string[:index] + replacement_char + original_string[index + 1:]
        return new_string


simulate = SimulateRSA()

simulate.run()

