from typing import Any, Iterable
from pygame.sprite import AbstractGroup
from settings import *

class allsprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector(100,20)

    def draw(self, player_center):
        self.offset.x = -(player_center[0] - WINDOW_WIDTH/2)
        self.offset.y = -(player_center[1] - WINDOW_HEIGHT/2)

        _ground = [sprite for sprite in self if sprite.layer_ == 0]
        _house = sorted([sprite for sprite in self if sprite.layer_ == 2],key = lambda sprite: sprite.rect.centery)
        _objects = sorted([sprite for sprite in self if sprite.layer_ == 3],key= lambda sprite : sprite.rect.centery)

        for layer in (_ground, _house, _objects):
            for sprite in layer:
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)

class light_sprites(pygame.sprite.Group):
    def draw(self,surf,r,pos,player):
        r += self.amt
        l_surf = pygame.Surface((r*2,r*2),pygame.SRCALPHA)
        rect = l_surf.get_rect(center = pos)
        l = 0
        for i in range(r,0,-1):
                pygame.draw.circle(l_surf,(255,255,255,l),((r*2)/2,(r*2)/2),i)
                if l < 20:
                    l += 2
        surf.blit(l_surf,rect)
        l_surf.blit(player.image,rect.center)
    def update(self,amt):
        self.amt = amt