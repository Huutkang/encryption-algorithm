import serial
import pygame, math



run = True

arduinoData = serial.Serial('com3', 9600)


def xyz(n):
    be_mat4 = pygame.Surface((700, 28))
    be_mat4.set_colorkey((0, 0, 0))
    be_mat5 = so(n)
    be_mat4.blit(be_mat5, (614, 0))
    return be_mat4

def kc(d):
    global be_mat2
    if 0<d<=40:
        pygame.draw.rect(be_mat2, "green", [0, 0, 620, 8], border_radius=10)
        pygame.draw.rect(be_mat2, "red", [15*d, 0, 600 - 15*d, 8], border_radius=10)
    else:
        pygame.draw.rect(be_mat2, "green", [0, 0, 620, 8], border_radius=10)

def so(n):
    global font2
    be_mat = pygame.Surface((28, 28))
    be_mat.set_colorkey((0, 0, 0))
    text = font2.render(str(n), True, "green")
    if n <100:
        be_mat.blit(text, (5, 0))
    else:
        be_mat.blit(text, (0, 0))
    return pygame.transform.rotate(be_mat, -90)

def quay(be_mat, tam, goc):    # đầu vào góc trong khoảng 0 đến 180 thôi nhá. lười xét trường hợp
    g = (2*goc*math.pi)/360
    dai, rong = be_mat.get_size()
    x = tam[0]
    y= tam[1]
    if (0<=goc<=90):
        x = x - (rong/2)*math.sin(g) - (rong/2)*math.cos(g)
        y = y - dai*math.sin(g) - (rong/2)*math.cos(g) + (rong/2)*math.sin(g)
    elif (90<goc<=180):
        x = x + dai*math.cos(g) - (rong/2)*math.sin(g) - (rong/2)*math.cos(g)
        y = y - dai*math.sin(g) + (rong/2)*math.cos(g) + (rong/2)*math.sin(g)
    q = pygame.transform.rotate(be_mat, goc)
    
    dis.blit(q, (x, y))
    


pygame.init()
clock = pygame.time.Clock()
dis_width = 1200
dis_height = 700

font1 = pygame.font.SysFont("comicsansms", 28)
font2 = pygame.font.SysFont("arial", 20)

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Hệ Thống Nhúng - Nhóm 8')

be_mat1 = pygame.Surface((600, 2))
be_mat1.set_colorkey((0, 0, 0))
pygame.draw.rect(be_mat1, "green", [0, 0, 600, 2], border_radius=10)

be_mat2 = pygame.Surface((620, 8))
be_mat2.set_colorkey((0, 0, 0))
pygame.draw.rect(be_mat2, "green", [0, 0, 620, 8], border_radius=10)

be_mat3 = pygame.Surface((1200,700), pygame.SRCALPHA)
be_mat3.fill((0, 0, 0, 10))

text1 = font1.render("Nhóm 8", True, "green") 
text2 = font1.render("Angle: ", True, "green") 
text3 = font1.render("Distance: ", True, "green") 
text4 = font2.render("10 cm", True, "green") 
text5 = font2.render("20 cm", True, "green") 
text6 = font2.render("30 cm", True, "green") 
text7 = font2.render("40 cm", True, "green") 
text_angle = font1.render(str(120), True, "green") 
text_distance = font1.render(str(40), True, "green") 


try:
    while run:        
        while (arduinoData.in_waiting==0):
            pass
        dataPacket = arduinoData.readline().decode('utf-8').strip('\r\n')
        arr = dataPacket.split(',')
        angle = int(arr[0])
        distance = int(arr[1])
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    run=False
                if event.key == pygame.K_q:
                    run=False

        text_angle = font1.render(str(angle), True, "green")
        text_distance = font1.render(str(distance), True, "green") 

        dis.blit(be_mat3, (0, 0))
        
        pygame.draw.circle(dis, "green", [600, 650], 140, 2, draw_top_left=True, draw_top_right=True)
        pygame.draw.circle(dis, "green", [600, 650], 280, 2, draw_top_left=True, draw_top_right=True)
        pygame.draw.circle(dis, "green", [600, 650], 420, 2, draw_top_left=True, draw_top_right=True)
        pygame.draw.circle(dis, "green", [600, 650], 560, 2, draw_top_left=True, draw_top_right=True)
        pygame.draw.rect(dis, "green", [0, 650, 1200, 2], border_radius=10)
        pygame.draw.rect(dis, "green", [600-2, 50, 2, 600], border_radius=10)
        pygame.draw.rect(dis, "black", [0, 652, 1200, 50])
        
        kc(distance)
        quay(be_mat2, (600, 650), angle)
        quay(be_mat1, (600, 650), 30)
        quay(be_mat1, (600, 650), 60)
        quay(be_mat1, (600, 650), 120)
        quay(be_mat1, (600, 650), 150)
        quay(xyz(30), (600, 650), 30)
        quay(xyz(60), (600, 650), 60)
        quay(xyz(90), (600, 650), 90)
        quay(xyz(120), (600, 650), 120)
        quay(xyz(150), (600, 650), 150)
        
        dis.blit(text1, (200, 655))
        dis.blit(text2, (670, 655))
        dis.blit(text3, (900, 655))
        dis.blit(text4, (690, 625))
        dis.blit(text5, (830, 625))
        dis.blit(text6, (970, 625))
        dis.blit(text7, (1110, 625))
        dis.blit(text_angle, (760, 655))
        
        if distance<40:
            dis.blit(text_distance, (1032, 655))
        
        pygame.display.update()
        # clock.tick(60)
        if run==False:
            r=False
    pygame.quit()

except:
    arduinoData.close()

