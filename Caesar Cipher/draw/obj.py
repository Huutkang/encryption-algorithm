import pygame
import math

class Obj:
    target = None
    step_x = 0
    step_y = 0
    
    def __init__(self, x, y, xy=[0, 0], on = False):
        self.surface = pygame.Surface((x, y), pygame.SRCALPHA)
        self.width = x
        self.height = y
        self.font1 = pygame.font.SysFont("Calibri", 28)
        self.font2 = pygame.font.SysFont("Calibri", 30, bold=True)
        self.font3 = pygame.font.SysFont("Calibri", 18)
        self.font4 = pygame.font.SysFont("Calibri", 100)
        self.font5 = pygame.font.SysFont("Calibri", 50)
        self.font6 = pygame.font.SysFont("Calibri", 36)
        self.xy = xy
        self.on = on
        self.step = 0

    def checkInObj(self, pos):
        if pos[0] < self.xy[0] or pos[0] > self.xy[0] + self.width:
            return False
        if pos[1] < self.xy[1] or pos[1] > self.xy[1] + self.height:
            return False
        return True

    def draw(self, obj):
        self.surface.blit(obj[0], obj[1])

    def setMove(self, target, speed):
        """
        Thiết lập tọa độ đích và bước di chuyển.
        :param target: Tọa độ đích (x, y).
        :param speed: Tốc độ di chuyển (khoảng cách mỗi bước).
        """
        self.target = target
        dx = target[0] - self.xy[0]
        dy = target[1] - self.xy[1]
        distance = math.sqrt(dx**2 + dy**2)

        if distance == 0:  # Nếu vật thể đã ở đích
            self.step_x = 0
            self.step_y = 0
        else:
            self.step_x = speed * dx / distance
            self.step_y = speed * dy / distance

    def move(self, check=False):
        if self.on==False: return False
        """
        Di chuyển vật thể tới gần đích.
        :return: True nếu đã tới đích, False nếu chưa.
        """
        if self.target is None:
            return False  # Không có đích để di chuyển

        dx = self.target[0] - self.xy[0]
        dy = self.target[1] - self.xy[1]
        distance = math.sqrt(dx**2 + dy**2)

        if distance <= math.sqrt(self.step_x**2 + self.step_y**2):
            # Đến đích hoặc gần đích
            self.xy = list(self.target)
            self.step_x = 0
            self.step_y = 0
            return True
        else:
            if check:
                return False
            # Tiến tới đích
            self.xy[0] += self.step_x
            self.xy[1] += self.step_y
            return False

    def setCoordinates(self, x, y):
        self.xy = [x, y]
    
    def update(self, xy, input=None):
        pass
