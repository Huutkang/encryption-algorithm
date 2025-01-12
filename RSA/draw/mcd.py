import pygame
from .obj import Obj


class Mcd (Obj):
    
    def __init__(self):
        super().__init__(500, 100)
        self.xy = [130, 250]
    
    def update(self):
        text = self.font4.render("m=c  mod n", True, "black")
        pygame.draw.rect(self.surface, "#00CCFF", [0, 0, self.width, self.height], border_radius=int(min(self.width, self.height)/10))
        text2 = self.font5.render("d", True, "black")
        self.surface.blit(text, (10, 10))
        self.surface.blit(text2, (180, 4))
        return [self.surface, (self.xy[0], self.xy[1])]
    