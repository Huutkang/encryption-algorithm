import pygame
from collections import deque
from .obj import Obj
from .char import Char
from .str import String

class Ds (Obj):
    index = 0
    width = 440
    height = 640
    m = []
    n = []
    
    def __init__(self):
        super().__init__(self.width, self.height)
        self.xy = [740, 100]
        self.dq = deque()
    
    def append(self, char, value):
        m = [Char(char, xy=(10, 35*len(self.dq)+12)), String(value, xy=(60, 35*len(self.dq)+19)), False]
        self.dq.append(m)
        self.lock_display = True
    
    def pop(self):
        r = self.dq.popleft()
        self.updateCoordinates()
        return r
    
    def getQuantity(self):
        return len(self.dq)
    
    def getCoordinates(self, l=None):
        if l is None:
            if len(self.dq)<18:
                l=len(self.dq)
            else:
                l=18
        x=self.xy[0]+10
        y=self.xy[1]+35*l+12
        return (x, y)
    
    def updateCoordinates(self):
        for i in range(len(self.dq)):
            self.setMoveTarget(self.dq[i], i+self.index)
    
    def forward(self):
        self.index -= 1
        for i in range(len(self.dq)):
            self.setMoveTarget(self.dq[i], i+self.index)
    
    def backward(self):
        self.index += 1
        for i in range(len(self.dq)):
            self.setMoveTarget(self.dq[i], i+self.index)
    
    def setMoveTarget(self, obj, target):
        obj[0].setMove((10, 35*target+12), 10)
        obj[1].setMove((60, 35*target+19), 10)
        obj[0].on = True
        obj[1].on = True
    
    def goto0(self):
        if type(self.index) != int:
            return False
        while True:
            if self.index == 0:
                self.updateCoordinates()
                return True
            elif self.index < 0:
                self.index += 1
            else:
                self.index -= 1
    
    def checkgoto0(self):
        if len(self.dq)>0:
            return self.dq[0][0].move(check=True)
        else:
            return False
    
    def moveTarget(self):
        for i in self.dq:
            i[0].move()
            i[1].move()
    
    def draw(self):
        for i in self.dq:
            if i[-1]:
                x = i[0].update()
                y = i[1].update()
                self.surface.blit(x[0], x[1])
                self.surface.blit(y[0], y[1])
    
    def update(self):
        pygame.draw.rect(self.surface, (20, 20, 20), (0, 0, 440, 650))
        pygame.draw.rect(self.surface, "blue", (50, 0, 2, 650))
        self.moveTarget()
        self.draw()
            
        return [self.surface, (self.xy[0], self.xy[1])]

    def unlock(self):
        for i in self.dq:
            if i[2]==False:
                i[2]=True
                return
    
    def reset(self):
        self.dq.clear()
        self.index = 0
        self.updateCoordinates()
