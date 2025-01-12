import pyaudio, pygame, librosa
import numpy as np
from collections import deque
from threading import Thread
from lib.ham_ho_tro import load_obj
from lib.graphics import atdb, maurgb, maurgb, camxuc, thanhtiendo
import noisereduce as nr




class Realtime:
    '''nhận dạng âm thanh thời gian thực và hiển thị đồ họa trực quan
    
    các đối số đầu vào:
    path_cnn: đường dẫn tới file đối tượng cnn đã lưu, nếu bạn không cung cấp
    thì mặc định lấy file có id lớn nhất trong thư mục storage/CNN
    path_lstm: đường dẫn tới file đối tượng lstm đã lưu, nếu bạn không cung cấp
    thì mặc định lấy file có id lớn nhất trong thư mục storage/LSTM
    db_start: là ngưỡng để bắt đầu ghi âm nếu bạn không cung cấp
    thì sẽ lấy theo mặc định
    db_stop: là ngưỡng để dừng ghi âm nếu bạn không cung cấp
    thì sẽ lấy theo mặc định'''
    
    db_start = -50

    db_stop = -50
    
    run = True
    
    emotion_cnn = -1
    emotion_lstm = -1
    
    hs = 0
    
    at = deque([np.array(128*[1e-9])], maxlen=10)
    
    
    def __init__(self, path_cnn='cnn', path_lstm='lstm', db_start=None, db_stop=None):
        self.cnn_obj = load_obj(path_cnn)
        self.lstm_obj = load_obj(path_lstm)
        if db_start != None:
            self.db_start = db_start
        if db_stop != None:
            self.db_stop = db_stop
    
    def emotion(self, data):
        n = np.array(data)
        n = np.hstack(n)
        # ----------------------------------------------------
        # comment hoặc bỏ comment đoạn này xem nó như nào
        # n = nr.reduce_noise(n,sr=22050)
        # n = librosa.effects.pitch_shift(n, sr = 22050, n_steps = 2)
        # ----------------------------------------------------
        n = np.array([n])
        self.emotion_lstm = self.lstm_obj.predict(data = n)[0]
        self.emotion_cnn = self.cnn_obj.predict(data = n)[0]
    
    def display(self):
        self.cda = -100
        self.tiendo = 0
        self.cdatb = -100
        dt = True
        pygame.init()
        clock = pygame.time.Clock()
        dis_width = 1200
        dis_height = 800

        font = pygame.font.SysFont("Calibri", 28)
        fontt = pygame.font.SysFont("Cascadia Mono SemiBold", 60)

        dis = pygame.display.set_mode((dis_width, dis_height))
        pygame.display.set_caption('Nhập môn AI')

        text1 = font.render("Nguyễn Xuân An", True, "green") 
        text2 = font.render("Trần Ngọc Phúc", True, "green") 
        text3 = font.render("Nguyễn Hữu Thắng", True, "green") 
        lstm = fontt.render("LSTM", True, (252, 3, 244))
        cnn = fontt.render("CNN", True, (252, 3, 244))
        dangghi = font.render("Đang ghi", True, "green") 
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.run = False
                    if event.key == pygame.K_q:
                        self.run = False
                    if event.key == pygame.K_f:
                        dt = not dt
                    if event.key == pygame.K_1 and self.db_start<10:
                        self.db_start+=1
                    if event.key == pygame.K_2 and self.db_start>-100:
                        self.db_start-=1
                    if event.key == pygame.K_3 and self.db_stop<10:
                        self.db_stop+=1
                    if event.key == pygame.K_4 and self.db_stop>-100:
                        self.db_stop-=1
                    if event.key == pygame.K_UP and self.hs<100:
                        self.hs +=1
                    elif event.key == pygame.K_DOWN and self.hs>-100:
                        self.hs -=1
            be_mat1 = pygame.Surface((1200, 750), pygame.SRCALPHA)
            be_mat1.fill((0, 0, 0, 40))
            dis.blit(be_mat1, (0, 0))

            pygame.draw.rect(dis, "black", [0, 550, 1200, 200])
            if dt:
                db = atdb(self.at[0])+100
                if len(self.at)>1:
                    del self.at[0]
                mang_mau = maurgb()
                for i in range(128):
                    x = int(db[i])
                    if x >200:
                        x=200
                    red, green, blue=mang_mau[i]
                    pygame.draw.rect(dis, (red, green, blue), [24+9*i, 750-x, 4, 1000])

            pygame.draw.rect(dis, "green", [0, 750, 1200, 2], border_radius=10)
            pygame.draw.rect(dis, "black", [0, 752, 1200, 50])
            pygame.draw.rect(dis, (162, 168, 50), [590, 545, 20, -1.53*(self.cda+100)], border_radius=2)
            
            dis.blit(text1, (70, 760))
            dis.blit(text2, (515, 760))
            dis.blit(text3, (900, 760))
            dis.blit(lstm, (250, 170))
            dis.blit(cnn, (870, 170))
            
            cdtb = font.render("Cường độ TB:", True, "red")
            dis.blit(cdtb, (840, 40))
            text_cdatb = font.render(str(round(self.cdatb, 1))+' db', True, "red")
            dis.blit(text_cdatb, (1000, 40))
            volume = font.render("Volume:", True, "red")
            dis.blit(volume, (840, 80))
            if self.hs >= 0:
                t_hs = '+'+str(self.hs)+' db'
            else:
                t_hs = str(self.hs)+' db'
            text_cdatb = font.render(t_hs, True, "red")
            dis.blit(text_cdatb, (1000, 80))
            
            nguongtren = font.render("Ngưỡng ghi:", True, "red")
            dis.blit(nguongtren, (80, 40))
            
            text_cdatb = font.render(str(self.db_start)+' db', True, "red")
            dis.blit(text_cdatb, (250, 40))
            
            nguongduoi = font.render("Ngưỡng dừng:", True, "red")
            dis.blit(nguongduoi, (80, 80))
            
            text_cdatb = font.render(str(self.db_stop)+' db', True, "red")
            dis.blit(text_cdatb, (250, 80))
            
            dis.blit(camxuc(self.emotion_lstm), (50, 225))
            dis.blit(camxuc(self.emotion_cnn), (650, 225))
            dis.blit(thanhtiendo(self.tiendo), (475, 112))
            if self.tiendo!=0:
                dis.blit(dangghi, (550, 74))
                
            pygame.display.update()
            clock.tick(50)

    
    def sound(self):
        '''1 giây. âm thanh mà vượt quá một ngưỡng thì bắt đầu ghi, 5 giây dừng. 1 giây không nói. dừng.
        giá trị db nó phụ thuộc vào từng thiết bị. nên phải thử trước'''
        recording = False
        count = 0
        one_second = deque(maxlen=10)
        five_seconds = deque(maxlen=50)
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=22050, input=True, frames_per_buffer=2205)
        ml = True
        while self.run:
            data = stream.read(2205)
            audio_data = np.frombuffer(data, dtype=np.float32)
            audio_data = audio_data*10**(self.hs/20)
            one_second.append(audio_data)
            self.cdatb = librosa.amplitude_to_db(np.array(list(one_second))).mean()
            self.cda = librosa.amplitude_to_db(audio_data).mean()
            mel = librosa.feature.melspectrogram(y=audio_data, sr=22050).T
            for i in mel:
                self.at.append(i)
            
            if len(one_second)==10:
                if ml and self.cdatb>-50:
                    ml=False
                    self.db_start = self.db_stop = int(self.cdatb) + 4
            
            if recording == True:
                count+=1
                five_seconds.append(audio_data)
            
            if self.cdatb > self.db_start and recording == False and len(one_second)==10:
                # print("Bắt đầu ghi âm!")
                recording = True
                for i in one_second:
                    count += 1
                    five_seconds.append(i)
            
            self.tiendo = 2*len(five_seconds)
            
            if self.cdatb < self.db_stop and recording == True or count >= 50:
                # print("Dừng ghi âm!")
                recording = False
                dtarr = list(five_seconds)
                emo = Thread(target=self.emotion, args=(dtarr,))
                emo.start()
                count=0
                five_seconds.clear()
                one_second.clear()
                
        stream.stop_stream()
        stream.close()
        p.terminate()

    def start(self):
        c1 = Thread(target=self.display)
        c2 = Thread(target=self.sound)
        c1.start()
        c2.start()



