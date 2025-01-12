import pygame
from .obj import Obj


class Unicode (Obj):
    
    def __init__(self):
        super().__init__(180, 60)
        self.xy = [266, 200]
    
    def update(self):
        text = self.font5.render("Unicode", True, "black")
        pygame.draw.rect(self.surface, "#00CCFF", [0, 0, self.width, self.height], border_radius=int(min(self.width, self.height)/10))
        self.surface.blit(text, (4, 10))
        return [self.surface, (self.xy[0], self.xy[1])]
    