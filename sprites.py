
from settings import *
from areas import areas

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, layer = world_layers['ground']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.layer_ = layer

        self.hitbox = self.rect.copy()

class border_sprite(Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy()

class transit_sprite(Sprite):
    def __init__(self, pos, size, target, groups, ):
        surf = pygame.surface.Surface(size)
        super().__init__(pos, surf, groups)
        self.target = target

class spawn_sprite(Sprite):
    def __init__(self,pos,groups,area):
        surf = pygame.surface.Surface((1,1))
        self.mobs = areas[area]['enemies']
        super().__init__(pos,surf,groups)
        self.x = pos[0]
        self.y = pos[1]

def darker(scr,dark):
    darkness = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT),pygame.SRCALPHA)
    d = dark 
    pygame.draw.rect(darkness,(0,0,0,d),[0,0,WINDOW_WIDTH,WINDOW_HEIGHT])
    scr.blit(darkness,(0,0))
    
class lights(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.amt = 0
    def update(self,amt):
        self.amt = amt