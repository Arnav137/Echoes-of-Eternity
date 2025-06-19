from typing import Any
from settings import *
import UI_codes
from sprites import lights,darker
from areas import *
from functions import get_image

class Player(pygame.sprite.Sprite):
    def __init__(self, pos , groups, layer, collision_sprites,lvl,xp,money,inventory):
        super().__init__(groups)
        self.collision_sprites = collision_sprites
        #player images
        image31 = get_image('images\player no 1.png',24,16,2,0,black)
        image41 = get_image('images\player no 1.png',24,16,3,0,black)
        image51 = get_image('images\player no 1.png',24,16,4,0,black)
        image61 = get_image('images\player no 1.png',24,16,5,0,black)
        image11 = get_image('images\player no 1.png',24,16,0,0,black)
        image71 = get_image('images\player no 1.png',24,16,6,0,black)
        image81 = get_image('images\player no 1.png',24,16,7,0,black)
        image21 = get_image('images\player no 1.png',24,16,1,0,black)
        image12 = get_image('images\player no 1.png',24,16,0,1,black)
        image22 = get_image('images\player no 1.png',24,16,1,1,black)
        image32 = get_image('images\player no 1.png',24,16,2,1,black)
        image42 = get_image('images\player no 1.png',24,16,3,1,black)
        image52 = get_image('images\player no 1.png',24,16,4,1,black)
        image62 = get_image('images\player no 1.png',24,16,5,1,black)
        image72 = get_image('images\player no 1.png',24,16,6,1,black)
        image82 = get_image('images\player no 1.png',24,16,7,1,black)
        image13 = get_image('images\player no 1.png',24,16,0,2,black)
        image23 = get_image('images\player no 1.png',24,16,1,2,black)
        image33 = get_image('images\player no 1.png',24,16,2,2,black)
        image43 = get_image('images\player no 1.png',24,16,3,2,black)
        image53 = get_image('images\player no 1.png',24,16,4,2,black)
        image63 = get_image('images\player no 1.png',24,16,5,2,black)
        image73 = get_image('images\player no 1.png',24,16,6,2,black)
        image83 = get_image('images\player no 1.png',24,16,7,2,black)

        #player image lists for each direction
        self.idle_images_lst = [image52,image72,image12,image32,image62,image82,image42,image22]
        self.up_images_lst = [image51,image52,image53]
        self.left_images_lst = [image71,image72,image73]
        self.down_images_lst = [image11,image12,image13]
        self.right_images_lst = [image31,image32,image33]
        self.upleft_images_lst = [image61,image62,image63]
        self.upright_images_lst = [image41,image42,image43]
        self.downleft_images_lst = [image81,image82,image83]
        self.downright_images_lst = [image21,image22,image23]
        #to index thru image list
        self.image_count = 0
        self.count = 0
        #to add character animation
        self.mov = False
        # to set current image list
        self.image_lst = self.idle_images_lst
        #to set image size
        self.image = image52
        self.image = pygame.transform.scale(self.image,(50,100))
        self.rect = self.image.get_frect(center = pos)
        self .layer_ = layer
        #player hitbox
        self.hitbox = self.rect.inflate(-self.rect.width/2, -60)
        #no clue what it does but its important for player centering
        self.direction = vector()
        #PLAYERSPEED
        self.v = 250
        #player name for text 
        self.name = 'player'
        # player stats(make stats screen in future)
        self.level = lvl
        self.health = self.level*5 +100
        self.total_health = self.health
        self.xp = xp
        self.total_xp = self.level**5 + 100
        self.dmg = 10
        self.money = money
        self.inv = inventory

    def input(self):#player direction
        keys = pygame.key.get_pressed()
        input_vector = vector()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            input_vector.y -= 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            input_vector.x -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            input_vector.y += 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            input_vector.x += 1
        self.direction = input_vector.normalize() if input_vector else input_vector

    def movt(self, dt):#for collision check and moving player
        self.rect.centerx += self.direction.x * self.v * dt
        self.hitbox.centerx = self.rect.centerx
        self.collision('horizontal')
        self.rect.centery += self.direction.y * self.v * dt
        self.hitbox.centery = self.rect.centery
        self.collision('vertical')
        self.anim()

    def anim(self):#character animation (dont mess with it too hard to fix)
        if self.direction.y == 0 and self.direction.x == 0:#idle
            self.image_lst = self.idle_images_lst
        elif self.direction.y > 0 and self.direction.x == 0:#up
            self.image_lst = self.up_images_lst
        elif self.direction.y == 0 and self.direction.x < 0:#left
            self.image_lst = self.left_images_lst
        elif self.direction.y < 0 and self.direction.x == 0:#down
            self.image_lst = self.down_images_lst
        elif self.direction.y == 0 and self.direction.x > 0:#right
            self.image_lst = self.right_images_lst
        elif self.direction.y > 0 and self.direction.x < 0:#upleft
            self.image_lst = self.upleft_images_lst
        elif self.direction.y < 0 and self.direction.x < 0:#downleft
            self.image_lst = self.downleft_images_lst
        elif self.direction.y > 0 and self.direction.x > 0:#upright
            self.image_lst = self.upright_images_lst
        elif self.direction.y < 0 and self.direction.x > 0:#downright
            self.image_lst = self.downright_images_lst
        else:
            self.image_lst = self.idle_images_lst#idle

    def collision(self,axis):#to define collision check
        for sprite in self.collision_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if axis == 'horizontal':
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    self.rect.centerx = self.hitbox.centerx
                if axis == 'vertical':
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    self.rect.centery = self.hitbox.centery

    def update(self, dt):#to call all player funtcions
        self.input()
        self.movt(dt)
        if len(self.image_lst) > 3:
                mouse = pygame.mouse.get_pos()
                center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2)
                if mouse[0] == center[0] and mouse[1] == center[1]:#idle
                    self.image = self.idle_images_lst[0]
                    print(1)
                elif mouse[0] in range(int(center[0]-25),int(center[0]+25)) and mouse[1] > center[1]:#up
                    self.image = self.idle_images_lst[0]
                    
                elif mouse[0] < center[0] and mouse[1] in range(int(center[1]-25),int(center[1]+25)):#left
                    self.image = self.idle_images_lst[1]
                    
                elif mouse[0] in range(int(center[0]-25),int(center[0]+25)) and mouse[1] < center[1]:#down
                    self.image = self.idle_images_lst[2]   
                    
                elif mouse[0] > center[0]and mouse[1] in range(int(center[1]-25),int(center[1]+25)):#right
                    self.image = self.idle_images_lst[3]
                    
                elif mouse[0] < center[0] and mouse[1] > center[1]:#upleft
                    self.image = self.idle_images_lst[4]
                    
                elif mouse[0] < center[0] and mouse[1] < center[1]:#downleft
                    self.image = self.idle_images_lst[5]
                    
                elif mouse[0] > center[0] and mouse[1] > center[1]:#upright
                    self.image = self.idle_images_lst[6]
                    
                elif mouse[0] > center[0] and mouse[1] < center[1]:#downright
                    self.image = self.idle_images_lst[7]
                    
                else:
                    self.image = self.idle_images_lst[0]
                    
        else:
            if self.mov:
                if self.image_count >= 2:
                    self.count = -1
                elif self.image_count <= 0:
                    self.count = +1
            
                self.image_count += self.count
                self.image = self.image_lst[self.image_count]
                
        self.image = pygame.transform.scale(self.image,(50,100))
        self.mov = False

class enemey(pygame.sprite.Sprite):
    def __init__(self, pos , groups, layer, collision_sprites,player_sprite,area_lvl,enemy):#almost same as player but dumber
        super().__init__(groups)

        self.sheet = enemy
        self.collision_sprites = collision_sprites
        # enemy images
        image11 = get_image(self.sheet,100,100,0,3,black)
        image12 = get_image(self.sheet,100,100,1,3,black)
        image13 = get_image(self.sheet,100,100,2,3,black)        

        image21 = get_image(self.sheet,100,100,0,1,black)
        image22 = get_image(self.sheet,100,100,1,1,black)
        image23 = get_image(self.sheet,100,100,2,1,black)

        image31 = get_image(self.sheet,100,100,0,2,black)
        image32 = get_image(self.sheet,100,100,1,2,black)
        image33 = get_image(self.sheet,100,100,2,2,black)

        image41 = get_image(self.sheet,100,100,0,0,black)
        image42 = get_image(self.sheet,100,100,1,0,black)
        image43 = get_image(self.sheet,100,100,2,0,black)
        

        
        


        self.idle_images_lst = [image12,image22,image32,image42]
        self.up_images_lst = [image41,image42,image43]
        self.left_images_lst = [image21,image22,image23]
        self.down_images_lst = [image11,image12,image13]
        self.right_images_lst = [image31,image32,image33]
        
        
        self.image_count = 0
        self.count = 0

        self.mov = False

        self.image_lst = self.idle_images_lst

        self.image = image12
        self.image = pygame.transform.scale(self.image,(100,100))
        self.rect = self.image.get_frect(center = pos)

        self .layer_ = layer
        
        self.hitbox = self.rect.inflate(-self.rect.width/2, -60)
        
        self.player_sprite = player_sprite

        self.direction = vector()

        self.name = 'enemy'

        self.level = area_lvl
        self.health = 100 + self.level * 10
        self.dmg = 10 
        self.give_xp = self.level*2

    def input(self):#for player direction 
        keys = pygame.key.get_pressed()
        input_vector = vector()
        dir = random.choice(['up','down','left','right'])
        if dir == 'up':
            input_vector.y -= 1
        if dir == 'left':
            input_vector.x -= 1
        if dir == 'down':
            input_vector.y += 1
        if dir == 'right':
            input_vector.x += 1
        self.direction = input_vector.normalize() if input_vector else input_vector
        self.anim()

    def movt(self, dt):#random movement of enemy
        self.rect.centerx += self.direction.x * 100 * dt
        self.hitbox.centerx = self.rect.centerx
        self.collision('horizontal')
        
        self.rect.centery += self.direction.y * 100 * dt
        self.hitbox.centery = self.rect.centery
        self.collision('vertical') 

    def anim(self):#animating movement 
        if self.direction.y == 0 and self.direction.x == 0:#idle
            self.image_lst = self.idle_images_lst
        elif self.direction.y > 0 and self.direction.x == 0:#up
            self.image_lst = self.up_images_lst
        elif self.direction.y == 0 and self.direction.x < 0:#left
            self.image_lst = self.left_images_lst
        elif self.direction.y < 0 and self.direction.x == 0:#down
            self.image_lst = self.down_images_lst
        elif self.direction.y == 0 and self.direction.x > 0:#right
            self.image_lst = self.right_images_lst
        else:
            self.image_lst = self.idle_images_lst#idle

    def collision(self,axis):#enemy collision
        for sprite in self.collision_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if axis == 'horizontal':
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    self.rect.centerx = self.hitbox.centerx
                if axis == 'vertical':
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    self.rect.centery = self.hitbox.centery

    def update(self, dt):#to call enemy functions
        self.movt(dt)         
        if self.mov:
                if self.image_count >= 2:
                    self.count = -1
                elif self.image_count <= 0:
                    self.count = +1
                self.image_count += self.count
                
                self.image = self.image_lst[self.image_count]
                
        self.image = pygame.transform.scale(self.image,(100,100))
        self.mov = False

class item(pygame.sprite.Sprite):

    def __init__(self, item):
        super().__init__()
        #item image rect and surface
        self.item = item
        self.image = pygame.image.load(self.item['image']).convert_alpha()
        self.image = pygame.transform.scale(self.image,(50,50))
        self.rect = self.image.get_rect()
        self.surf_rect = self.rect.inflate(5,5)
        self.surf = pygame.Surface((self.surf_rect[2],self.surf_rect[3]))
        
        #item stats
        self.name = self.item['name']#item name for text
        self.type = type
        if self.type == 'sword':
            self.dmg = self.item['dmg']
        elif self.type == 'armor':
            self.health == self.item['health']
        self.level = self.item['level']
        self.buy_amt = self.item['amt']
        self.sell_amt = self.buy_amt - (self.item['amt'])/10

    def draw(self, pos, screen):
        #item draw and glow on hover function
        self.rect.topleft = pos
        self.surf_rect.center = self.rect.center
        self.stats_ui = UI_codes.item_stats_ui(self.surf_rect.topright,self.item)
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse[0],mouse[1]):
            self.surf.fill('yellow')
            self.stats_ui.draw(screen)
        else:
            self.surf.fill('black')
        screen.blit(self.surf,(self.surf_rect[0],self.surf_rect[1]))
        screen.blit(self.image,(pos))

class npc(pygame.sprite.Sprite):
    def __init__(self,place,pos,layer,name):
        super().__init__()
        self.image = pygame.image.load(r'images\npc1.png')
        self.image = pygame.transform.scale(self.image,(70,100))
        self.rect = self.image.get_rect(topleft = pos)
    
        self.layer_ = layer
        #npc properties
        self.pos = place#tiled map entity(DO NOT CHANGE) 
        self.name = name
        self.items = []
        self.items_lst = areas[str(place)]['shop']
        for i in self.items_lst:
            self.items.append(i)
        #for future npc dialogues
        self.text = size20.render('blah blah blah',True,'white')
    #to display shop item
    def shop(self,surf,money,inv):
        shopui = UI_codes.shop_ui(self.items,inv)
        money,inv = shopui.run(surf,True,money)
        return money,inv

class npc_interact(pygame.sprite.Sprite):#rect to interact with npc(no need to touch)
    def __init__(self,place,rectval,name):
        super().__init__()
        self.pos = place
        self.surf = pygame.Surface((rectval[2],rectval[3]))
        self.rect = self.surf.get_rect(topleft = (rectval[0],rectval[1]))
        self.name = name
        