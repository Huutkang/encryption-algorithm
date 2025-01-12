import pygame
from .obj import Obj


class Char (Obj):
    
    def __init__(self, char, xy=None, value=None):
        super().__init__(30, 30, [30, 94], value=value)
        self.char = char
        if xy is not None:
            self.xy = [xy[0], xy[1]]
    
    def update(self, xy=None, input=None):
        if xy is not None:
            self.xy = xy
        if input is not None:
            text = self.font2.render(input, True, "black")
        else:
            text = self.font2.render(self.char, True, "black")
        pygame.draw.rect(self.surface, "green", [0, 0, self.width, self.height], border_radius=int(min(self.width, self.height)/10))
        self.surface.blit(text, (4, 0))
        return [self.surface, (self.xy[0], self.xy[1])]
    