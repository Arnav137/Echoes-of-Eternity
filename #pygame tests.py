#pygame tests
import pygame
import sys
from settings import *
from entities import Player,enemey,item
from UI_codes import UI,Battle,currentstats,shop_ui
from items import *
screen = pygame.display.set_mode((1280,700))
clock = pygame.time.Clock()

pygame.init()

x_ = 0
y_ = 0
black = (0,0,0)

class item_box(pygame.sprite.Sprite):
    def __init__(self,pos,item):
        super().__init__()
        self.image = pygame.surface.Surface((50,50))
        self.pos = pos
        self.rect = self.image.get_rect()
        self.item = item
        self.item_img = pygame.image.load(self.item['image'])
        self.item_img = pygame.transform.scale(self.item_img,(44,44))
    def draw(self,screen):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse[0]-205-self.pos[0],mouse[1]-205 - self.pos[1]):
            self.image.fill('yellow')
        else:
            self.image.fill('black')
        self.image.blit(self.item_img,(2,2))
        screen.blit(self.image,self.pos)

class Inventory(UI):#under construction
    def __init__(self,inv):
        super().__init__()
        self.size = (1000,500)
        self.image = pygame.image.load('images\inventory ui.png')
        self.image = pygame.transform.scale(self.image,(self.size))
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2)) 
        self.item_box_sprites = pygame.sprite.AbstractGroup()
        self.boxes_screen = pygame.surface.Surface((400,350))
        self.inv = inv
    def item_boxes(self):
        x = 5
        y = 5
        self.boxes_screen.fill((55,55,55))
        for i in self.inv.keys():
            if y <= 400:
                box = item_box((x,y),self.inv[i])
                self.item_box_sprites.add(box)
                box.draw(self.boxes_screen)
                x += 55
                if x >= 400:
                    x = 5
                    y += 55
            
        self.image.blit(self.boxes_screen,(100,100))

    def run(self,screen,running = True):
        while running:
            screen.blit(self.image,self.rect)
            self.item_boxes()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    m = pygame.Surface((5,5))
                    m_rect = m.get_rect(center = mouse)
                    for j in self.button_sprites.sprites():
                        if m_rect.colliderect(j.rect):
                           if j.action == 'close':
                                running = False
                                break
                           else:
                                j.funct(self)  
                            
    
            pygame.display.update()

size = (WINDOW_WIDTH,WINDOW_HEIGHT)

item_lst = {1:sword1,2:sword2,3:sword3,4:sword4,5:sword5}

while True:
    screen.fill((0,0,0))
    pygame.draw.rect(screen,(20,20,20),[10,10,50,50])

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if (mouse[0] in range(10,60)) and (mouse[1] in range(10,60)):
                inv_obj = Inventory(item_lst)
                inv_obj.run(screen,(100,100),True)

            
    pygame.display.update()
    clock.tick(60)