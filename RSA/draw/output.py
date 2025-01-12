import pygame
from .obj import Obj


class Output (Obj):
    
    def update(self, xy=None, input=''):
        if xy is not None:
            self.xy = xy
        text = self.font1.render(input, True, "black") 
        pygame.draw.rect(self.surface, (100, 100, 100), [0, 0, self.width, self.height], border_radius=int(min(self.width, self.height)/10))
        self.surface.blit(text, (10, 5))
        return [self.surface, (self.xy[0], self.xy[1])]
    