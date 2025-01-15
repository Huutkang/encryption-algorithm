import pygame
from .obj import Obj


class Char (Obj):
    
    def __init__(self, char, xy=None, type=None):
        super().__init__(30, 30, [30, 124])
        self.char = char
        if xy is not None:
            self.xy = [xy[0], xy[1]]
        self.type = type
        self.color = "green"
        self.on = True
    
    def update(self, xy=None, input=None):
        if xy is not None:
            self.xy = xy
        if input is not None:
            text = self.font2.render(input, True, "black")
        else:
            text = self.font2.render(self.char, True, "black")
        pygame.draw.rect(self.surface, self.color, [0, 0, self.width, self.height], border_radius=int(min(self.width, self.height)/10))
        self.surface.blit(text, (4, 1))
        return [self.surface, (self.xy[0], self.xy[1])]
    