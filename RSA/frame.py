import pygame, re
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
from truyen_kieu import TruyenKieu

class SimulateRSA:

    running = True
    
    dis_width = 1200
    dis_height = 800
    
    # các biến cho gõ văn bản
    x = False 
    input_active = True
    input_text='64'
    d=0
    t2=0
    ss=''
    
    pos=(0, 0)
    
    def __init__(self):
        # Khởi tạo Pygame
        pygame.init()
        self.rsa = RSA(test=True)
        self.truyen_kieu = TruyenKieu()
        self.font = pygame.font.SysFont("Calibri", 20)
        self.screen = pygame.display.set_mode((self.dis_width, self.dis_height))
        pygame.display.set_caption("RSA")

        # Tạo đồng hồ để kiểm soát FPS
        self.clock = pygame.time.Clock()
        self.value = []
        self.ip = Input(512, 40)
        self.keysize = Input(80, 35)
        self.out = Output(512, 40)
        self.cme = Cme()
        self.mcd = Mcd()
        self.unicode = Unicode()
        self.tex_out = ""
        self.bd = False
        self.button = Button()
        self.ds = Ds()
        self.index_prepare = 0
        self.t_go = 0
        self.type = "key" # encode, decode, key, auto
        self.auto = "input"
        self.stepkey = 0
        
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
                self.value[self.index_prepare][3].setMove((320, 300), 3)
                self.value[self.index_prepare][4].on = False
                self.index_prepare += 1
                self.input_text = self.input_text[1:]
            else:
                self.bd=False
    
    def dcd(self):
        if self.ds.checkgoto0() == False:
            return
        if time.time() > self.t_go+1:
            if len(self.ds.dq)>0:
                self.t_go = time.time()
                i=self.value[self.index_prepare]
                i[4].on = True
                i[4].setCoordinates(800, 70)
                i[4].setMove((250, 300), 3)
                self.setStep(i, 6)
                self.index_prepare += 1
                self.ds.pop()
        
    def initStr(self):
        mh = self.rsa.encrypt(self.input_text)
        m=[]
        for i in range(len(self.input_text)):
            vb = self.input_text[i]
            m.append([vb, ord(vb), mh[i], Char(vb, type=1), String(str(mh[i]), type=2), String(str(ord(vb)), type=3)])
        self.value = m
        
    def drawString(self):
        text = self.font.render("d: "+str(self.rsa.d), True, "orange")
        self.screen.blit(text, (10, 27))
        text = self.font.render("n: "+str(self.rsa.N), True, "orange")
        self.screen.blit(text, (10, 4))
        text = self.font.render("e: "+str(self.rsa.e), True, "orange")
        self.screen.blit(text, (10, 50))
    
    def draw(self, obj):
        self.screen.blit(obj[0], obj[1])
    
    
    def isNumber(self, char):
        if len(char) == 1 and char.isdigit():
            return True
        return False

    def is_valid_character(self, char):
        special_characters = r"""`~!@#$%^&*()-_=+[{]}\\|;:'",<.>/? """
        pattern = (
            rf"^[{re.escape(special_characters)}"
            r"a-zA-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂÂÊÔơưăâêô0-9]$"
        )
        return bool(re.match(pattern, char))
    
    def event(self):
        t1=0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # # Xử lý nhấp chuột
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.pos = (event.pos[0], event.pos[1])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.type = "auto"
                    self.initEncode()
                    self.auto = "input"
                elif event.key == pygame.K_DOWN:
                    self.type = "encode"
                    self.initEncode()
                elif event.key == pygame.K_RIGHT:
                    if self.type == "encode":
                        self.type = "decode"
                        self.initDecode()
                elif event.key == pygame.K_LEFT:
                    if self.type == "decode":
                        self.type = "encode"
                        self.initEncode()
                elif event.key == pygame.K_RETURN:
                    if self.type == "key":
                        self.eventCreateKey()
                    else:
                        self.bd = True
                        self.initStr()
                elif event.key == pygame.K_y:
                    self.yesNo(True)
                elif event.key == pygame.K_n:
                    self.yesNo(False)
                
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
                        if self.is_valid_character(event.unicode):
                            if self.type == "encode":
                                self.input_text += event.unicode  # Thêm ký tự Unicode
                            elif self.isNumber(event.unicode)  and self.type == "key" and len(self.input_text)<4:
                                self.input_text += event.unicode
        if self.x:
            if (time.time()-self.t2>0.02):
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
            if self.type == "encode" or (self.type == "auto" and self.auto == "encode"):
                vt=self.ds.getCoordinates()
                if a:
                    if (i[3].step==1):
                        self.setStep(i, 2)
                        i[3].setMove(vt, 3)
                        i[5].xy = [320, 300]
                        i[5].setMove((320, 547), 3)
                        i[5].on = True
                        self.setStep(i, 3)
                if c:
                    if (i[5].step==3):
                        i[5].on = False
                        self.setStep(i, 4)
                        i[4].xy = [116, 547]
                        i[4].setMove((vt[0]+50, vt[1]+8), 4)
                        self.ds.append(i[0], str(i[2]))
                        i[4].on = True
                if b:
                    if (i[5].step==4):
                        if len(self.ds.dq)>20:
                            self.ds.forward()
                        self.setStep(i, 5)
                        i[3].on = False
                        i[4].on = False
                        self.ds.unlock()
            elif self.type == "decode" or (self.type == "auto" and self.auto == "decode"):
                if b:
                    if (i[4].step==6):
                        self.setStep(i, 7)
                        i[5].xy = [400, 300]
                        i[5].setMove((370, 530), 3)
                        i[5].on = True
                        i[3].on = False
                if c:
                    if (i[3].step==7):
                        i[4].on = False
                        i[3].xy = [370, 530]
                        i[3].setMove((370, 720), 3)
                        i[3].on = True
                        self.setStep(i, 8)
                if a:
                    if (i[3].step==8):
                        self.tex_out+=i[0]
                        self.setStep(i, 9)

    def update (self):
        for i in self.value:
            if i[3].on:
                self.draw(i[3].update())
            if i[4].on:
                self.draw(i[4].update())
            if i[5].on:
                self.draw(i[5].update())

    def checkInput(self):
        self.input_active = self.ip.checkInObj(self.pos) or self.keysize.checkInObj((self.pos))

    def initEncode(self):
        self.index_prepare = 0
        self.input_text = ""
        self.value = []
        self.unicode.xy = [266, 270]
        self.ds.reset()
    
    def initDecode(self):
        self.unicode.xy=[300, 500]
        self.index_prepare = 0
        self.ds.goto0()
        self.tex_out = ""
    
    def encode(self):
        self.go() 
        self.draw(self.ip.update([70, 120],input = self.input_text))
        self.draw(self.button.update())
        self.update()
        self.draw(self.cme.update())
        self.draw(self.unicode.update())
    
    def decode(self):
        self.dcd()
        self.update()
        self.draw(self.out.update([70, 720],input = self.tex_out))
        self.draw(self.mcd.update())
        self.draw(self.unicode.update())
    
    def yesNo(self, yn):
        if self.type != "key":
            return
        match self.stepkey:
            case 3:
                if yn:
                    self.rsa.p = self.p
                    self.rsa.q = self.q
                    self.stepkey += 1
                else:
                    self.stepkey = 1
            case 7:
                if yn:
                    self.rsa.e = self.e
                    self.stepkey += 1
                else:
                    self.stepkey = 6

    def eventCreateKey(self):
        match self.stepkey:
            case 0:
                self.rsa.keysize = int(self.input_text)
                self.input_text = ''
                self.stepkey += 1
                print(self.rsa.keysize)
            case 1:
                self.stepkey += 1
                pygame.draw.rect(self.screen, "black", [10, 150, 300, 30])
                text = self.font.render("Đang tính toán ...", True, "orange")
                self.screen.blit(text, (10, 150))
                self.p=0
                self.q=0
            case 4:
                self.rsa.N = self.rsa.calculateN(self.p, self.q)
                self.phiN = self.rsa.calculatePhiN(self.p, self.q)
                self.stepkey += 1
            case 5:
                self.stepkey += 1
            case 6:
                self.e = self.rsa.selectE(self.phiN, self.rsa.keysize)
                self.stepkey += 1
            case 8:
                self.rsa.d = self.rsa.calculateD(self.e, self.phiN)
                self.stepkey += 1
            case 9:
                self.stepkey += 1
            case 10:
                self.type = "auto"
                self.initEncode()
                self.auto = "input"
                
    def createKey(self):
        match self.stepkey:
            case 0:
                text = self.font.render("Nhập keysize:", True, "orange")
                self.screen.blit(text, (10, 125))
                self.draw(self.keysize.update([130, 120],input = self.input_text))
            case 1:
                text = self.font.render("Tạo hai số nguyên tố lớn p và q?", True, "orange")
                self.screen.blit(text, (10, 125))
                text = self.font.render("Nhấn enter để tiếp tục ...", True, "orange")
                self.screen.blit(text, (10, 150))
            case 2:
                self.p = self.rsa.snt.generateLargePrime(self.rsa.keysize)
                self.q = self.rsa.snt.generateLargePrime(self.rsa.keysize)
                self.stepkey += 1
                pass
            case 3:
                text = self.font.render("Tạo hai số nguyên tố lớn p và q?", True, "orange")
                self.screen.blit(text, (10, 125))
                text = self.font.render("p="+str(self.p), True, "orange")
                self.screen.blit(text, (10, 160))
                text = self.font.render("q="+str(self.q), True, "orange")
                self.screen.blit(text, (10, 190))
                text = self.font.render("Nhấn y để đồng ý, nhấn n để tạo lại", True, "orange")
                self.screen.blit(text, (10, 220))
            case 4:
                text = self.font.render("p="+str(self.p), True, "orange")
                self.screen.blit(text, (10, 125))
                text = self.font.render("q="+str(self.q), True, "orange")
                self.screen.blit(text, (10, 150))
                text = self.font.render("Tính n=p.q và hàm Euler phi(n)=(p-1)(q-1)", True, "orange")
                self.screen.blit(text, (10, 200))
                text = self.font.render("Enter", True, "orange")
                self.screen.blit(text, (10, 225))
            case 5:
                text = self.font.render("p="+str(self.p), True, "orange")
                self.screen.blit(text, (10, 125))
                text = self.font.render("q="+str(self.q), True, "orange")
                self.screen.blit(text, (10, 150))
                text = self.font.render("Tính n=p.q và hàm Euler phi(n)=(p-1)(q-1)", True, "orange")
                self.screen.blit(text, (10, 200))
                text = self.font.render("n="+str(self.rsa.N), True, "orange")
                self.screen.blit(text, (10, 225))
                text = self.font.render("Phi(n)="+str( self.phiN), True, "orange")
                self.screen.blit(text, (10, 250))
            case 6:
                text = self.font.render("p="+str(self.p), True, "orange")
                self.screen.blit(text, (10, 125))
                text = self.font.render("q="+str(self.q), True, "orange")
                self.screen.blit(text, (10, 150))
                text = self.font.render("Tính n=p.q và hàm Euler phi(n)=(p-1)(q-1)", True, "orange")
                self.screen.blit(text, (10, 200))
                text = self.font.render("n="+str(self.rsa.N), True, "orange")
                self.screen.blit(text, (10, 225))
                text = self.font.render("Phi(n)="+str( self.phiN), True, "orange")
                self.screen.blit(text, (10, 250))
                text = self.font.render("Chọn một số tự nhiên e sao cho 1<e<Phi(n) và nguyên tố cùng nhau với Phi(n)", True, "orange")
                self.screen.blit(text, (10, 290))
            case 7:
                text = self.font.render("p="+str(self.p), True, "orange")
                self.screen.blit(text, (10, 125))
                text = self.font.render("q="+str(self.q), True, "orange")
                self.screen.blit(text, (10, 150))
                text = self.font.render("Tính n=p.q và hàm Euler phi(n)=(p-1)(q-1)", True, "orange")
                self.screen.blit(text, (10, 200))
                text = self.font.render("n="+str(self.rsa.N), True, "orange")
                self.screen.blit(text, (10, 225))
                text = self.font.render("Phi(n)="+str( self.phiN), True, "orange")
                self.screen.blit(text, (10, 250))
                text = self.font.render("Chọn một số tự nhiên e sao cho 1<e<Phi(n) và nguyên tố cùng nhau với Phi(n)", True, "orange")
                self.screen.blit(text, (10, 290))
                text = self.font.render("Đã tìm được: e="+str(self.e), True, "orange")
                self.screen.blit(text, (10, 320))
                text = self.font.render("Nhấn y để đồng ý, nhấn n để tạo lại", True, "orange")
                self.screen.blit(text, (10, 345))
            case 8:
                text = self.font.render("p="+str(self.p), True, "orange")
                self.screen.blit(text, (10, 125))
                text = self.font.render("q="+str(self.q), True, "orange")
                self.screen.blit(text, (10, 150))
                text = self.font.render("Tính n=p.q và hàm Euler phi(n)=(p-1)(q-1)", True, "orange")
                self.screen.blit(text, (10, 200))
                text = self.font.render("n="+str(self.rsa.N), True, "orange")
                self.screen.blit(text, (10, 225))
                text = self.font.render("Phi(n)="+str( self.phiN), True, "orange")
                self.screen.blit(text, (10, 250))
                text = self.font.render("Chọn một số tự nhiên e sao cho 1<e<Phi(n) và nguyên tố cùng nhau với Phi(n)", True, "orange")
                self.screen.blit(text, (10, 290))
                text = self.font.render("Đã tìm được: e="+str(self.e), True, "orange")
                self.screen.blit(text, (10, 320))
                text = self.font.render("Tính d sao cho d.e đồng dư với 1 (mod Phi(n))", True, "orange")
                self.screen.blit(text, (10, 345))
            case 9:
                text = self.font.render("p="+str(self.p), True, "orange")
                self.screen.blit(text, (10, 125))
                text = self.font.render("q="+str(self.q), True, "orange")
                self.screen.blit(text, (10, 150))
                text = self.font.render("Tính n=p.q và hàm Euler phi(n)=(p-1)(q-1)", True, "orange")
                self.screen.blit(text, (10, 200))
                text = self.font.render("n="+str(self.rsa.N), True, "orange")
                self.screen.blit(text, (10, 225))
                text = self.font.render("Phi(n)="+str( self.phiN), True, "orange")
                self.screen.blit(text, (10, 250))
                text = self.font.render("Chọn một số tự nhiên e sao cho 1<e<Phi(n) và nguyên tố cùng nhau với Phi(n)", True, "orange")
                self.screen.blit(text, (10, 290))
                text = self.font.render("e="+str(self.e), True, "orange")
                self.screen.blit(text, (10, 320))
                text = self.font.render("Tính d sao cho d.e đồng dư với 1 (mod Phi(n))", True, "orange")
                self.screen.blit(text, (10, 345))
                text = self.font.render("d="+str(self.rsa.d), True, "orange")
                self.screen.blit(text, (10, 370))
            case 10:
                text = self.font.render("Đã hoàn tất việc tạo khóa:", True, "orange")
                self.screen.blit(text, (10, 125))
                text = self.font.render("Khóa công khai n, e", True, "orange")
                self.screen.blit(text, (10, 150))
                text = self.font.render("khóa bí mật n, d", True, "orange")
                self.screen.blit(text, (10, 175))
                text = self.font.render("n="+str(self.rsa.N), True, "orange")
                self.screen.blit(text, (10, 200))
                text = self.font.render("e="+str(self.e), True, "orange")
                self.screen.blit(text, (10, 225))
                text = self.font.render("d="+str(self.rsa.d), True, "orange")
                self.screen.blit(text, (10, 250))
    
    def autoInput(self):
        if time.time() > self.t_go+0.08:
            self.t_go = time.time()
            vb = self.truyen_kieu.get_next_character()
            if vb =="\n":
                self.auto = "encode"
                self.bd = True
                self.initStr()
            else:
                self.input_text += vb

    def checkStatusEncode(self):
        for i in self.value:
            if i[3].step < 5:
                return False
        return True
    
    def checkStatusDecode(self):
        for i in self.value:
            if i[3].step < 9:
                return False
        return True
    
    def run(self):
        while self.running:
            # Vẽ lên màn hình
            self.screen.fill("black")  # Xóa màn hình bằng màu đen
            self.checkInput()
            
            if self.type=="key":
                self.createKey()
            else:
                self.move()
                self.draw(self.ds.update())
            
            if self.type=="encode":
                self.encode()
            
            if self.type=="decode":
                self.decode()
                
            if self.type=="auto":
                if self.auto == "encode":
                    if self.checkStatusEncode():
                        self.auto = "decode"
                        self.initDecode()
                    self.encode()
                elif self.auto == "decode":
                    self.decode()
                    if self.checkStatusDecode():
                        self.initEncode()
                        self.auto = "input"
                elif self.auto == "input":
                    self.encode()
                    self.autoInput()
                    
                    
            self.drawString()
            
            self.event()
            
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

