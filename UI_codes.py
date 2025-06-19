from typing import Any
from settings import *
import time
from functions import text_form
from items import sword1,sword2,sword3,sword4,sword5
# for dark back ground
def transparent_surf(screen):
    common_translucent_surface = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT),pygame.SRCALPHA)
    pygame.draw.rect(common_translucent_surface,(0,0,0,200),[0,0,WINDOW_WIDTH,WINDOW_HEIGHT])
    screen.blit(common_translucent_surface,(0,0))
#self explaintory
class Button(pygame.sprite.Sprite):
    def __init__(self, 
                 color, 
                 button_action, 
                 pos, size, 
                 text_size, 
                 text = '',
                 border_color = 'black',
                 border_width  = 0):
        super().__init__()
        self.pos = pos

        self.image = pygame.Surface((size))
        self.image.fill(border_color)
        self.rect = self.image.get_rect(topleft = self.pos)
        self.surface_RECT = self.rect.inflate((-border_width,-border_width))
        self.surface = pygame.Surface((self.surface_RECT[2],self.surface_RECT[3]))
        self.surface.fill(color)
        self.text = text_size.render(str(text),True,'white')
        self.text_Rect = self.text.get_rect(center = self.rect.center)
        self.action = button_action
        
    def draw(self,surf):
        surf.blit(self.image,(self.pos))
        surf.blit(self.surface,self.surface_RECT)
        surf.blit(self.text,(self.text_Rect))

    def funct(self,UI_name):
        pass
# dont use UI class as parent class jus copy the code u need from here
class UI(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = (1000,500)
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2)) 
        self.button_sprites = pygame.sprite.Group()
        
    def run(self,screen,pos,running):
        while running:
            screen.blit(self.image,pos)
            for i in self.button_sprites.sprites():
                i.draw(screen)
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
       
class Battle(UI):
    def __init__(self,enemy_obj,player_obj,area,):
        super().__init__()
        if area == 'jungle1':
            self.image = pygame.image.load(r'forest1bakground.png')
        else:#more back grounds if more areas in the future
            self.image = pygame.image.load(r'forest1bakground.png')
        self.image = pygame.transform.scale(self.image,(1000,500))
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        #to call the strating 3 buttons
        self.bat_start()

        self.surf_rect = self.rect.inflate(20,200)
        self.surf_rect.center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2)
        #monster and player objects
        self.monster = enemy_obj
        self.player = player_obj
        #healths tuple (enemy,player)
        self.healths = [self.monster.health,self.player.health]
        #calling helathbar class to make healthbar ui
        self.player_bar = healthbar(self.healths[1],self.player.total_health,self.player)
        self.enemy_bar = healthbar(self.healths[0],self.monster.health,self.monster)

        

    def run(self,screen,pos,running):
        #call dark surface
        transparent_surf(screen)
        while running:
            #background of ui
            pygame.draw.rect(screen,'black',self.surf_rect.inflate(5,5))
            pygame.draw.rect(screen,(50,50,50),self.surf_rect)
            screen.blit(self.image,self.rect)
            self.image.blit(self.player.image,(200,350))
            self.image.blit(self.monster.image,(670,350))
            #blitting the buttons
            for i in self.button_sprites.sprites():
                i.draw(screen)
            #events
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                #mouse input
                if e.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    m = pygame.Surface((5,5))
                    m_rect = m.get_rect(center = mouse)
                    for j in self.button_sprites.sprites():
                        if m_rect.colliderect(j.rect):
                           if j.action == 'close':#close ui
                                running = False
                                xp = 0
                                return self.healths[1],xp,0
                           else:#different attacks
                                if j.action == 'attack':
                                    self.attack()
                                if j.action == 'attack1':
                                    health = self.attacks(1)
                                if j.action == 'attack2':
                                    health = self.attacks(2)
                                if j.action == 'attack3':
                                    health = self.attacks(3)
                                if j.action == 'cancel':
                                    self.bat_start() 
            try:
                if health:
                    self.healths = health
            except:
                pass
            #update the healths
            self.player_bar.update(self.healths[1])
            self.enemy_bar.update(self.healths[0])
            self.player_bar.draw((200,300),self.image) 
            self.enemy_bar.draw((670,300),self.image)               
            pygame.display.update()
            xp = 0
            try:
                if self.healths[0] <= 0:
                    xp = self.monster.give_xp
                    drop = random.choice([sword1,sword2,sword3,sword4,sword5])
                    return self.healths[1],xp,drop
                    
                elif self.healths[1] <= 0:
                    xp = 0
                    return self.healths[1],xp,0
            except:
                return 100,0,0#returns player health and xp
        

    def bat_start(self):#starting 3 buttons
        self.button_sprites.empty()
        self.attack_button = Button('red', 'attack',(950,610),(200,50),size30,'ATTACK')
        self.item_button = Button('blue', 'item',(750,610),(200,50),size30,'ITEMS')
        self.run_button = Button('green', 'close',(750,660),(400,50),size30,'RUN')
        self.button_sprites.add(self.attack_button,self.item_button,self.run_button)
    def attack(self):#3 attack buttons 1 cancel button
        self.button_sprites.empty()
        attack1 = Button('gray', 'attack1',(750,610),(200,50),size30, 'ATTACK1', border_width=3)  
        attack2 = Button('gray', 'attack2',(950,610),(200,50),size30, 'ATTACK2', border_width=3)
        attack3 = Button('gray', 'attack3',(750,660),(200,50),size30, 'ATTACK3', border_width=3)
        cancel = Button('red','cancel',(950,660),(200,50),size30,'CANCEL','brown',3)
        self.button_sprites.add(attack1, attack2, attack3, cancel) 
    def attacks(self, attack_number):#attack dmg to vary in the future
        if attack_number == 1:
            attack_dmg = 10
        elif attack_number == 2:
            attack_dmg = 20
        elif attack_number == 3:
            attack_dmg = 30
        else:
            attack_dmg = 0
        healths = self.attack_dmg(attack_dmg,
                                  self.player.dmg,
                                  self.monster.dmg,
                                  self.healths[0],
                                  self.healths[1])
        return healths
    #to reduce the healths
    def attack_dmg(self,attackdmg,player_dmg,monster_dmg,monster_health,player_health):
        dmg = player_dmg + attackdmg
        monster_health -= dmg
        mon_dmg = monster_dmg
        player_health -= mon_dmg
        return monster_health,player_health
    #to update the health after every battle
    def update(self,player_health):
        self.healths = (self.monster.health,player_health)
        self.player_bar.update(self.healths[1])

class healthbar(pygame.sprite.Sprite):#dont bother reading used only in 2 places
    def __init__(self,health,total_health,name):
        super().__init__()
        self.total_health = total_health
        self.surf = pygame.Surface((150,50))
        self.surf.fill((100,100,255))
        self.total_rect = pygame.Surface((100,20))
        self.txt = size12.render(str(name.name) + '  lvl. ' + str(name.level),True,'black')
        try:
            length = (health/self.total_health)*100
            if length < 0:
                length = 1
        except:
            length = 1
        self.health_rect = pygame.Surface((length,20))
        self.total_rect.fill('white')
        self.health_rect.fill('green')
    def draw(self,pos,screen):
        screen.blit(self.surf,pos)
        screen.blit(self.total_rect,(pos[0]+10,pos[1]+25))
        screen.blit(self.health_rect,(pos[0]+10,pos[1]+25))
        screen.blit(self.txt,(pos[0]+10,pos[1]+5))
    def update(self,health):
        try:
            length = (health/self.total_health)*100
            if length < 0:
                length = 1
        except:
            length = 1
        self.health_rect = pygame.Surface((length,20))
        self.health_rect.fill('green')

class currentstats(pygame.sprite.Sprite):# to display current stats
    def __init__(self,health,xp,total_health,total_xp,money,lvl):
        super().__init__()
        self.health = health
        self.total_health = total_health
        self.xp = xp
        self.total_xp = total_xp
        self.lvl = lvl
        self.money = money
        
    def draw(self,screen,pos):
        pygame.draw.rect(screen,(30,30,30),[pos[0],pos[1],250,100],border_top_right_radius=5)
        health_length = (self.health/self.total_health)*150
        xp_lenth = (self.xp/self.total_xp)*150
        health_txt = size12.render('HEALTH:',True,'white')
        health_no_txt = size12.render(str(self.health)+'/'+str(self.total_health),True,'white')
        xp_txt = size12.render('EXP:lvl.'+str(self.lvl),True,'white')
        xp_no_txt = size12.render(str(self.xp)+'/'+str(self.total_xp),True,'white')
        money_txt = size12.render('MONEY:'+str(self.money)+'$',True,'white')
        screen.blit(health_txt,(pos[0]+5,pos[1]+7))
        screen.blit(health_no_txt,(pos[0]+155,pos[1]+20))
        screen.blit(xp_txt,(pos[0]+5,pos[1]+47))
        screen.blit(xp_no_txt,(pos[0]+155,pos[1]+60))
        screen.blit(money_txt,(pos[0]+5,pos[1]+80))

        pygame.draw.rect(screen,
                         'white',
                         [pos[0],pos[1]+20,150,20],
                         border_top_right_radius=5,
                         border_bottom_right_radius=5)
        pygame.draw.rect(screen,
                         'green',
                         [pos[0],pos[1]+20,health_length,20],
                         border_top_right_radius=5,
                         border_bottom_right_radius=5)
        pygame.draw.rect(screen,
                         'black',
                         [pos[0],pos[1]+60,150,10],
                         border_top_right_radius=5,
                         border_bottom_right_radius=5)
        pygame.draw.rect(screen,
                         (200,200,255),
                         [pos[0],pos[1]+60,xp_lenth,10],
                         border_top_right_radius=5,
                         border_bottom_right_radius=5)

        pause_button = pygame.image.load(r'images\pause button.png')
        pause_button = pygame.transform.scale(pause_button,(30,30))
        screen.blit(pause_button,(1250,0))

    def update(self,health,total_health,xp,total_xp,money,lvl):
        self.health = health
        self.total_health = total_health
        self.xp = xp
        self.total_xp = total_xp
        self.money = money 
        self.lvl = lvl

class Pause(UI):#pause menu
    def __init__(self):
        self.image = pygame.Surface((1000,700))
        self.image.fill((50,50,50))    
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2)) 
        self.button_sprites = pygame.sprite.Group()
        play_button = Button((200,200,0),
                             'play',
                             (WINDOW_WIDTH/2 - 100,WINDOW_HEIGHT/2 - 100),
                             (200,50),
                             size20_bold,'PLAY',
                             5)
        settings_button = Button((200,200,0),
                                 'setings',
                                 (WINDOW_WIDTH/2 - 100,WINDOW_HEIGHT/2 - 40),
                                 (200,50),size20_bold,
                                 'SETTINGS',
                                 5)
        quit_button = Button((200,200,0),
                             'quit',
                             (WINDOW_WIDTH/2 - 100,WINDOW_HEIGHT/2 + 20),
                             (200,50),size20_bold,
                             'Quit',
                             5)
        self.button_sprites.add(play_button,settings_button,quit_button)
    def run(self, screen, pos, running):
        while running:
            screen.blit(self.image,(self.rect.x,self.rect.y))
            for i in self.button_sprites.sprites():
                i.draw(screen)
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
                            if j.action == 'play':
                                running = False
                                break
                            elif j.action == 'settings':
                                print('settings not added yet')
                            elif j.action == 'quit':
                                pygame.quit()
                                exit()
            pygame.display.update()               

class item_stats_ui(pygame.sprite.Sprite):#to display the item stats whenhover over item
    def __init__(self,pos,item):
        self.image = pygame.Surface((100,150),pygame.SRCALPHA)
        self.pos = pos
        self.type = item['type']
        self.name_text = size20_bold.render(str(item['name']),True,'green')
        self.level_text = size12.render(str(item['level'])+'-'+str(item['level']+10),True,'gray')
        if self.type == 'sword':
            self.attribute_txt = size12.render('dmg:'+ str(item['dmg']),True,'gray')
        elif self.type == 'armor':
            self.attribute_txt = size12.render('health:'+ str(item['health']),True,'gray')
        else:size22.render('error',True,'gray')
    def draw(self,screen):
        pygame.draw.rect(self.image,(0,0,0,200),[self.pos[0],self.pos[1],100,150])
        screen.blit(self.image,(self.pos))
        screen.blit(self.name_text,(self.pos[0]+3,self.pos[1]+3))
        screen.blit(self.level_text,(self.pos[0]+3,self.pos[1]+25))
        screen.blit(self.attribute_txt,(self.pos[0]+3,self.pos[1]+50))

class shop_item_ui(pygame.sprite.Sprite):#to create clickable object in shop
    def __init__(self,item,pos_y=1,):
        super().__init__()
        self.y = pos_y
        self.image = pygame.Surface((200,50))
        self.rect = self.image.get_rect(topleft = (100,50*self.y + 100))
        self.item = item
        img = self.item['image']
        self.item_image = pygame.image.load(img,'item_img')
        self.item_image = pygame.transform.scale(self.item_image,(40,40))
        self.text = size20_bold.render(str(self.item['name']),True,('white'))
        self.buy_txt = size12.render('buy:'+str(self.item['buy_amt']),True,'white')
        self.sell_txt = size12.render('sell:'+str(self.item['sell_amt']),True,'white')

    
    def draw(self,scr):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse[0]-140,mouse[1]-110):
            self.image.fill('yellow')
        else:
            self.image.fill('black')
        self.name_txt = size22.render(self.item['name'],True,'white')
        #pygame.draw.rect(self.image,(50,50,50),[2,2,self.rect.width-4,self.rect.height-4],border_radius=10)
        self.image.blit(self.item_image,(5,5))
        self.image.blit(self.text,(55,5))
        self.image.blit(self.buy_txt,(55,30))
        self.image.blit(self.sell_txt,(120,30))
        scr.blit(self.image,self.rect)

    def stats(self):
        if self.item['type'] == 'sword':
            atr = 'dmg:' + str(self.item['dmg'])
        elif self.item['type'] == 'armor':
            atr = 'health:' + str(self.item['health'])
        name = self.item['name']
        level = self.item['level']
        extra = self.item['desc']
        image = pygame.image.load(self.item['image'])
        lst = [atr,name,level,extra,image]
        return lst

class shop_ui(pygame.sprite.Sprite):#to make shop object
    def __init__(self,item_lst,inv):
        super().__init__()
        self.item_lst = item_lst
        self.size = (1000,500)
        self.surf = pygame.image.load(r'images\shop gui.png')
        self.surf = pygame.transform.scale(self.surf,self.size)
        self.rect = self.surf.get_rect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2)) 
        self.button_sprites = pygame.sprite.Group()
        
        self.item_sprites = pygame.sprite.Group()
        self.x = 0
        

        self.selected_item = None
        
        self.inv = inv

        self.button()
        self.item_box()        

    def button(self):
        buy_button = Button('green','buy',(750,400),(100,50),size20_bold,'BUY',(10,200,10),15)
        sell_button = Button('red','sell',(860,400),(100,50),size20_bold,'SELL',(200,10,10),15)
        self.close_buttom = Button('red','close',(950,0),(20,20),size20_bold,'X',border_width= 15)
        self.button_sprites.add(buy_button,sell_button,self.close_buttom)

    def item_box(self):
        for i in self.item_lst:
            self.item_sprites.add(shop_item_ui(i,self.item_lst.index(i)))
    
    def print_stats(self,surf):
        pygame.draw.rect(surf,(50,50,50),[730,70,200,300],border_radius=15)
        self.item_image = self.cur_info[4]
        self.item_image = pygame.transform.scale(self.item_image,(100,100))
        self.name_txt = size20_bold.render(str(self.cur_info[1]),True,('green'))
        self.atr_txt = size20.render(str(self.cur_info[0]),True,'blue')
        self.lvl_txt = size20.render('level:'+str(self.cur_info[2])+'+',True,'red')
        self.desc_txt = size12.render('description: \n'+ str(self.cur_info[3]),True,'gray')
        surf.blit(self.name_txt,(795,70))
        surf.blit(self.item_image,(780,100))
        surf.blit(self.lvl_txt,(740,220))
        surf.blit(self.atr_txt,(740,250))
        surf.blit(self.desc_txt,(740,280))

    def run(self,screen,running,bal):
        self.x = bal
        
        while running:
            self.curbal_text = size20.render('current balance:'+str(self.x),True,'white',black)
            self.surf.blit(self.curbal_text,(70,33))
            screen.blit(self.surf,self.rect)
            for sprite in self.button_sprites.sprites():
                sprite.draw(self.surf)
            for item in self.item_sprites.sprites():
                item.draw(self.surf)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    for i in self.item_sprites.sprites():
                        if i.rect.collidepoint(mouse[0]-140,mouse[1]-110):
                            self.cur_info = i.stats()
                            self.print_stats(self.surf)
                            self.selected_item = i
                        else:
                            screen.blit(self.surf,self.rect) 
                    if self.button_sprites.sprites()[2].rect.collidepoint(mouse[0]-140,mouse[1]-110):
                        return self.x,self.inv  
                    if self.selected_item:
                        for j in self.button_sprites.sprites():
                            if j.rect.collidepoint(mouse[0]-140,mouse[1]-110):
                                if j.action == 'close':
                                    return self.x,self.inv
                                elif j.action == 'buy':
                                        amt = self.selected_item.item['buy_amt']
                                        if self.x >= amt:
                                            self.x -= amt
                                            self.inv[len(self.inv)] = self.selected_item.item
                                    
                                elif j.action == 'sell':
                                    if self.selected_item.item in list(self.inv.values()):
                                        amt = self.selected_item.item['sell_amt']
                                        self.x += amt
                                        for i in self.inv:
                                            if self.inv[i] == self.selected_item.item:
                                                del(self.inv[i])
                                                break
                                    
                            
            clock.tick(60)
            pygame.display.update()

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
        if self.rect.collidepoint(mouse[0]-240-self.pos[0],mouse[1]- 210 -self.pos[1]):
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
        self.X_txt = size22.render('X',True,(0,0,0))
        self.X_rect = self.X_txt.get_rect(center = (970,30))
        self.y_rect = self.X_rect.inflate(30,30)
    def item_boxes(self):
        x = 5
        y = 5
        self.boxes_screen.fill((55,55,55))
        for i in self.inv:
            if y <= 400:
                box = item_box((x,y),self.inv[i])
                self.item_box_sprites.add(box)
                box.draw(self.boxes_screen)
                x += 55
                if x >= 350:
                    x = 5
                    y += 55
            
        self.image.blit(self.boxes_screen,(100,100))

    def run(self,screen,running = True):
        while running:
            pygame.draw.circle(self.image,'red',(970,30),30)
            self.image.blit(self.X_txt,self.X_rect)
            screen.blit(self.image,self.rect)
            self.item_boxes()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if self.y_rect.collidepoint(mouse[0]-140,mouse[1]-100):
                        running = False
                        break
                            
    
            pygame.display.update()

class start_screen():
    def __init__(self,):
        self.button_group = pygame.sprite.Group()
        self.buttons()
        self.loading_text = size20_bold.render('LOADING..',True,'white')
        echoes_txt = text_form('echoes',75,r'fonts\yellowblueletter.png')
        of_txt = text_form('of',75,r'fonts\yellowblueletter.png')
        eternity_txt = text_form('eternity',75,r'fonts\yellowblueletter.png')
        self.game_name = {echoes_txt:(415,100),of_txt:(565,175),eternity_txt:(340,250)}
        


    def buttons(self):
        play_button = Button('gray','quit',(540,400),(200,50),size20_bold,'PLAY',(50,50,50),10)
        cred_button = Button('gray','credits',(540,460),(200,50),size20_bold,'credits',(50,50,50),10)
        self.button_group.add(play_button,cred_button)

    def run(self,surf):
        run1 = True
        while run1:
            surf.fill('gray')
            for i in self.game_name.keys():
                surf.blit(i,self.game_name[i])
            for button in self.button_group.sprites():
                button.draw(surf)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    for b in self.button_group:
                        if b.rect.collidepoint(mouse):
                            if b.action == 'quit':
                                surf.fill('black')
                                surf.blit(self.loading_text,(500,300))
                                run1 = False
                                break
            pygame.display.update()

