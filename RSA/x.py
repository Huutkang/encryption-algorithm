'''
nhập c để bắt đầu cắt
k để kết thúc cắt. trước khi nhấn k cần ghi tên file bằng 1 số. vd: '1' -> 'map0'+'1'
chạy bằng run python file
nhập số tương ứng với bản đồ rồi nhấn j để thay đổi
trong khi nhập nhấn i để xóa str vừa nhập
dùng w,a,s,d để di chuyển con trỏ. lên, xuống, trái, phải để di chuyển bản đồ
0 là cỏ
1 là tường
2 là nước
3 là gạch
4 là cây
5 là đất
7 water_edge
8 water_edge_down
9 water_edge_left
10 water_edge_right
11 water_edge_bot_right
12 water_edge_bot_left
13 water_edge_left_up
14 water_edge_right_up
15 water_corner_top_right
16 water_corner_upper_left
17 water_corner_bot_left
18 water_corner_bot_right
'''

import pygame, sys
from pygame.locals import *

# đọc file txt
MANG=[]
HANG=0
COT=0
a = open ('map.txt','r',encoding='utf8')
dl=a.readlines()
a.close()
for i in dl:
    x=i.strip()
    xx=x.split()
    MANG.append(xx)
# sao lưu lại dữ liệu tránh trường hợp lỗi gây mất file
b=open('saoluu2.txt','w',encoding='utf8')
for i in MANG:
    HANG=HANG+1
    for j in i:
        b.write(j+' ')
    b.write('\n')   
b.close()

for i in MANG[0]:
    COT=COT+1
print(HANG)
print(COT)

if HANG<=37:
    hang=HANG
else:
    hang=37
if COT<=60:
    cot=COT
else:
    cot=60


WHITE = (255, 255, 255)
RED   = (255,   0,   0)
BLACK = (0, 0, 0)
# bắt đầu gọi hàm khởi tạo init
pygame.init()

### Xác định FPS ###
FPS = 60
fpsClock = pygame.time.Clock()
# cài đặt màn hình
DISPLAYSURF = pygame.display.set_mode((24*cot, 24*hang))
# đặt tên chương trình
pygame.display.set_caption('Event')
# chọn font chữ
score_font = pygame.font.SysFont("comicsansms", 12)
# hàm in chữ ra màn hình
def Inchu(H,C,h,c):
    COT = score_font.render(str(C), True, BLACK)
    DISPLAYSURF.blit(COT, [24*c+4, 24*h+10])
    HANG = score_font.render(str(H), True, RED)
    DISPLAYSURF.blit(HANG, [24*c+4, 24*h-4])

# lớp chính. mình lên mạng copy nên ngại sửa tên
class Car():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.X=0
        self.Y=0
        # khai báo string để nhập vào khi chỉnh sửa
        self.vb=''
        ## tải ảnh
        self.grass = pygame.image.load('grass.png')
        self.wall = pygame.image.load('wall.png')
        self.water = pygame.image.load('water.png')
        self.ground = pygame.image.load('ground.png')
        self.tree1 = pygame.image.load('tree1.png')
        self.sand = pygame.image.load('sand.png')
        self.water_edge = pygame.image.load('water_edge.png')
        self.cay_sa_mac = pygame.image.load('cay_sa_mac.png')
        self.water_edge_down = pygame.image.load('water_edge_down.png')
        self.water_edge_left = pygame.image.load('water_edge_left.png')
        self.water_edge_right = pygame.image.load('water_edge_right.png')
        self.water_edge_bot_right = pygame.image.load('water_edge_bot_right.png')
        self.water_edge_bot_left = pygame.image.load('water_edge_bot_left.png')
        self.water_edge_left_up = pygame.image.load('water_edge_left_up.png')
        self.water_edge_right_up = pygame.image.load('water_edge_right_up.png')
        self.water_corner_top_right = pygame.image.load('water_corner_top _right.png')
        self.water_corner_upper_left = pygame.image.load('water_corner_upper_left.png')
        self.water_corner_bot_left = pygame.image.load('water_corner_bot_left.png')
        self.water_corner_bot_right = pygame.image.load('water_corner_bot_right.png')

    # đk
        self.dk=False
        self.h0=0
        self.c0=0
    def draw(self): # Hàm dùng để vẽ 
        for c in range(cot):
            for h in range(hang):
                if MANG[h+self.y][c+self.x]=='0':
                    DISPLAYSURF.blit(self.grass, (24*c, 24*h))
                    if self.dk==True and ( h+self.y==self.h0 or c+self.x==self.c0 or h==int(self.Y) or c==int(self.X)):
                        Inchu(h+self.y-self.h0,c+self.x-self.c0,h,c)
                if MANG[h+self.y][c+self.x]=='1':
                    DISPLAYSURF.blit(self.wall, (24*c, 24*h))
                    if self.dk==True and ( h+self.y==self.h0 or c+self.x==self.c0 or h==int(self.Y) or c==int(self.X)):
                        Inchu(h+self.y-self.h0,c+self.x-self.c0,h,c)
                if MANG[h+self.y][c+self.x]=='2':
                    DISPLAYSURF.blit(self.water, (24*c, 24*h))
                    if self.dk==True and ( h+self.y==self.h0 or c+self.x==self.c0 or h==int(self.Y) or c==int(self.X)):
                        Inchu(h+self.y-self.h0,c+self.x-self.c0,h,c)
                if MANG[h+self.y][c+self.x]=='3':
                    DISPLAYSURF.blit(self.ground, (24*c, 24*h))
                    if self.dk==True and ( h+self.y==self.h0 or c+self.x==self.c0 or h==int(self.Y) or c==int(self.X)):
                        Inchu(h+self.y-self.h0,c+self.x-self.c0,h,c)
                if MANG[h+self.y][c+self.x]=='4':
                    DISPLAYSURF.blit(self.tree1, (24*c, 24*h))
                    if self.dk==True and ( h+self.y==self.h0 or c+self.x==self.c0 or h==int(self.Y) or c==int(self.X)):
                        Inchu(h+self.y-self.h0,c+self.x-self.c0,h,c)
                if MANG[h+self.y][c+self.x]=='5':
                    DISPLAYSURF.blit(self.sand, (24*c, 24*h))
                    if self.dk==True and ( h+self.y==self.h0 or c+self.x==self.c0 or h==int(self.Y) or c==int(self.X)):
                        Inchu(h+self.y-self.h0,c+self.x-self.c0,h,c)
                if MANG[h+self.y][c+self.x]=='6':
                    DISPLAYSURF.blit(self.cay_sa_mac, (24*c, 24*h))
                    if self.dk==True and ( h+self.y==self.h0 or c+self.x==self.c0 or h==int(self.Y) or c==int(self.X)):
                        Inchu(h+self.y-self.h0,c+self.x-self.c0,h,c)
                if MANG[h+self.y][c+self.x]=='7':
                    DISPLAYSURF.blit(self.water_edge, (24*c, 24*h))
                    if self.dk==True and ( h+self.y==self.h0 or c+self.x==self.c0 or h==int(self.Y) or c==int(self.X)):
                        Inchu(h+self.y-self.h0,c+self.x-self.c0,h,c)
                if MANG[h+self.y][c+self.x]=='8':
                    DISPLAYSURF.blit(self.water_edge_down, (24*c, 24*h))
                    if self.dk==True and ( h+self.y==self.h0 or c+self.x==self.c0 or h==int(self.Y) or c==int(self.X)):
                        Inchu(h+self.y-self.h0,c+self.x-self.c0,h,c)
                if MANG[h+self.y][c+self.x]=='9':
                    DISPLAYSURF.blit(self.water_edge_left, (24*c, 24*h))
                    if self.dk==True and ( h+self.y==self.h0 or c+self.x==self.c0 or h==int(self.Y) or c==int(self.X)):
                        Inchu(h+self.y-self.h0,c+self.x-self.c0,h,c)
                if MANG[h+self.y][c+self.x]=='10':
                    DISPLAYSURF.blit(self.water_edge_right, (24*c, 24*h))
                    if self.dk==True and ( h+self.y==self.h0 or c+self.x==self.c0 or h==int(self.Y) or c==int(self.X)):
                        Inchu(h+self.y-self.h0,c+self.x-self.c0,h,c)
                if MANG[h+self.y][c+self.x]=='11':
                    DISPLAYSURF.blit(self.water_edge_bot_right, (24*c, 24*h))
                    if self.dk==True and ( h+self.y==self.h0 or c+self.x==self.c0 or h==int(self.Y) or c==int(self.X)):
                        Inchu(h+self.y-self.h0,c+self.x-self.c0,h,c)
                if MANG[h+self.y][c+self.x]=='12':
                    DISPLAYSURF.blit(self.water_edge_bot_left, (24*c, 24*h))
                    if self.dk==True and ( h+self.y==self.h0 or c+self.x==self.c0 or h==int(self.Y) or c==int(self.X)):
                        Inchu(h+self.y-self.h0,c+self.x-self.c0,h,c)
                if MANG[h+self.y][c+self.x]=='13':
                    DISPLAYSURF.blit(self.water_edge_left_up, (24*c, 24*h))
                    if self.dk==True and ( h+self.y==self.h0 or c+self.x==self.c0 or h==int(self.Y) or c==int(self.X)):
                        Inchu(h+self.y-self.h0,c+self.x-self.c0,h,c)
                if MANG[h+self.y][c+self.x]=='14':
                    DISPLAYSURF.blit(self.water_edge_right_up, (24*c, 24*h))
                    if self.dk==True and ( h+self.y==self.h0 or c+self.x==self.c0 or h==int(self.Y) or c==int(self.X)):
                        Inchu(h+self.y-self.h0,c+self.x-self.c0,h,c)
                if MANG[h+self.y][c+self.x]=='15':
                    DISPLAYSURF.blit(self.water_corner_top_right, (24*c, 24*h))
                    if self.dk==True and ( h+self.y==self.h0 or c+self.x==self.c0 or h==int(self.Y) or c==int(self.X)):
                        Inchu(h+self.y-self.h0,c+self.x-self.c0,h,c)
                if MANG[h+self.y][c+self.x]=='16':
                    DISPLAYSURF.blit(self.water_corner_upper_left, (24*c, 24*h))
                    if self.dk==True and ( h+self.y==self.h0 or c+self.x==self.c0 or h==int(self.Y) or c==int(self.X)):
                        Inchu(h+self.y-self.h0,c+self.x-self.c0,h,c)
                if MANG[h+self.y][c+self.x]=='17':
                    DISPLAYSURF.blit(self.water_corner_bot_left, (24*c, 24*h))
                    if self.dk==True and ( h+self.y==self.h0 or c+self.x==self.c0 or h==int(self.Y) or c==int(self.X)):
                        Inchu(h+self.y-self.h0,c+self.x-self.c0,h,c)
                if MANG[h+self.y][c+self.x]=='18':
                    DISPLAYSURF.blit(self.water_corner_bot_right, (24*c, 24*h))
                    if self.dk==True and ( h+self.y==self.h0 or c+self.x==self.c0 or h==int(self.Y) or c==int(self.X)):
                        Inchu(h+self.y-self.h0,c+self.x-self.c0,h,c)
        if self.dk==False:       
            Inchu(self.y+int(self.Y),self.x+int(self.X),int(self.Y),int(self.X))
   
# hàm cập nhật thông tin sau các vòng lặp
    def update(self, moveLeft, moveRight): # Hàm dùng để thay đổi vị trí con trỏ, phần tử trong mảng
        if moveLeft == True and self.x>0:
            self.x -= 1
        if moveRight == True and self.x<COT-cot:
            self.x += 1
        if moveUp == True and self.y>0:
            self.y -= 1
        if moveDown == True and self.y<HANG-hang:
            self.y += 1
            
        # sửa chữa thay đổi dữ liệu mảng
        self.vb=self.vb+vanban
        if vanban=='y':
            zzz=self.vb.strip('y')
            MANG[self.y+int(self.Y)][self.x+int(self.X)]=zzz
            self.vb=''
            b=open('test.txt','w',encoding='utf8') # lưu lại thay đổi vào file txt
            for i in MANG:
                for j in i:
                    b.write(j+' ')
                b.write('\n')   
            b.close()
        if vanban=='n':
            self.vb=''
        if vanban=='c':
            self.dk=True
            self.h0=self.y+int(self.Y)
            self.c0=self.x+int(self.X)
            self.vb=self.vb.strip('c')
        if vanban=='k':
            self.dk=False
            self.vb=self.vb.strip('k')
            
            mang=[]
            for h in range(min(self.h0,self.y+int(self.Y)),max(self.h0,self.y+int(self.Y))+1):
                H=[]
                for c in range(min(self.c0,self.x+int(self.X)),max(self.c0,self.x+int(self.X))+1):
                    H.append(MANG[h][c])
                mang.append(H)
            bb=open('map0'+self.vb+'.txt','w',encoding='utf8')
            for i in mang:
                for j in i:
                    bb.write(j+' ')
                bb.write('\n')   
            bb.close()
            self.vb=''

# for c in range(226,230):
#     for h in range(27,30):
#         MANG[h][c]='4'
        # giới hạn di chuyển con trỏ. k cho di chuyển ra ngoài màn hình
        if moveA == True and self.X>0:
            self.X -= 0.2
        if moveD == True and self.X<cot-1:
            self.X += 0.2
        if moveW == True and self.Y>0:
            self.Y -= 0.2
        if moveS == True and self.Y<hang-1:
            self.Y += 0.2
    
        
        
        
# khởi tạo các biến cho tương tác với các phím
car = Car()
moveLeft = False
moveRight = False
moveUp = False
moveDown = False
moveA = False
moveD = False
moveW = False
moveS = False
vanban = ''
while True: # đoạn này cài đặt phím bấm
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                moveLeft = True
            if event.key == K_RIGHT:
                moveRight = True
            if event.key == K_UP:
                moveUp = True
            if event.key == K_DOWN:
                moveDown = True
            if event.key == K_0:
                vanban = '0'
            if event.key == K_1:
                vanban = '1'
            if event.key == K_2:
                vanban = '2'
            if event.key == K_3:
                vanban = '3'
            if event.key == K_4:
                vanban = '4'
            if event.key == K_5:
                vanban = '5'
            if event.key == K_6:
                vanban = '6'
            if event.key == K_7:
                vanban = '7'
            if event.key == K_8:
                vanban = '8'
            if event.key == K_9:
                vanban = '9'
            if event.key == K_j:
                vanban = 'y'
            if event.key == K_i:
                vanban = 'n'
            if event.key == K_w:
                moveW = True
            if event.key == K_a:
                moveA = True
            if event.key == K_s:
                moveS = True
            if event.key == K_d:
                moveD = True
            if event.key == K_c:
                vanban = 'c'
            if event.key == K_k:
                vanban = 'k'
            
        
        if event.type == KEYUP:
            if event.key == K_LEFT:
                moveLeft = False
            if event.key == K_RIGHT:
                moveRight = False
            if event.key == K_UP:
                moveUp = False
            if event.key == K_DOWN:
                moveDown = False
            if event.key == K_w:
                moveW = False
            if event.key == K_a:
                moveA = False
            if event.key == K_s:
                moveS = False
            if event.key == K_d:
                moveD = False

    # đoạn này gọi. cập nhật dữ sau khi bấm nút
    DISPLAYSURF.fill(WHITE)
    
    car.draw()
    car.update(moveLeft, moveRight)
    vanban=''

    pygame.display.update()
    fpsClock.tick(FPS)