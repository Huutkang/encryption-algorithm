import pygame
from .obj import Obj


class Button (Obj):
    
    def __init__(self):
        super().__init__(60, 40)
        self.xy = [600, 90]
    
    
    def update(self):
        text = self.font2.render("go", True, "black") 
        pygame.draw.rect(self.surface, "red", [0, 0, self.width, self.height], border_radius=int(min(self.width, self.height)/10))
        self.surface.blit(text, (7, 0))
        return [self.surface, (self.xy[0], self.xy[1])]
    