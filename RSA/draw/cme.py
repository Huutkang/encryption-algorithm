import pygame
from .obj import Obj


class Cme (Obj):
    
    def __init__(self):
        super().__init__(200, 100)
        self.xy = [260, 360]
    
    def update(self):
        text = self.font4.render("c=m", True, "black")
        pygame.draw.rect(self.surface, "#00CCFF", [0, 0, self.width, self.height], border_radius=int(min(self.width, self.height)/10))
        text2 = self.font5.render("e", True, "black")
        self.surface.blit(text, (4, 10))
        self.surface.blit(text2, (165, 0))
        return [self.surface, (self.xy[0], self.xy[1])]
    