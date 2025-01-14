import pygame
from .obj import Obj


class String (Obj):
    
    bgrcl = [20, 20, 20]
    
    def __init__(self, string, bgrcl = None, xy=None, type=None):
        l = len(string)
        super().__init__(int(9.4*l)+10, 18)
        self.string = string
        if bgrcl is not None:
            self.bgrcl = bgrcl
        if xy is not None:
            self.xy = [xy[0], xy[1]]
        self.type = type
    
    def update(self, xy=None):
        if xy is not None:
            self.xy = xy
        text = self.font3.render(self.string, True, "red")
        pygame.draw.rect(self.surface, self.bgrcl, [0, 0, self.width, self.height])
        self.surface.blit(text, (4, 0))
        return [self.surface, (self.xy[0], self.xy[1])]
    