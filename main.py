from settings import *
from pytmx.util_pygame import load_pygame
import json

from sprites import Sprite,border_sprite,transit_sprite,spawn_sprite,lights,darker
from entities import Player,enemey,npc,npc_interact
from groups import allsprites,light_sprites
from UI_codes import Battle,currentstats,Pause,start_screen,Inventory
from items import sword1,sword2,sword3,sword4,sword5

map_n = 'world'
spawn_p = 'house'
lst_spawn_maps = ['jungle1']
upd = False

class game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('echoes of eternity test')
        
        sscreen = start_screen()
        sscreen.run(self.display_surface)

        self.ob_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ob_timer,2000)

        self.move_time = pygame.USEREVENT + 2 
        pygame.time.set_timer(self.move_time,150)

        self.enemy_dir = pygame.USEREVENT + 3
        pygame.time.set_timer(self.enemy_dir,4000)

        self.dark = pygame.USEREVENT + 4
        pygame.time.set_timer(self.dark,3000)

        self.battle_bool = False

        # groups 
        self.all_sprites = allsprites()
        self.collision_sprites = pygame.sprite.Group()
        self.transition_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.spawn_sprites = pygame.sprite.Group() 
        self.light_sprites = light_sprites()
        self.interact_sprites = pygame.sprite.Group()
        self.npc_sprites = pygame.sprite.Group()

        self.change = 1
        self.dark_amt = 1

        #JSON SAVE
        try:
            with open('game_save','r') as game_save:
                self.save_file = json.load(game_save)
                print(self.save_file)
                self.lvl = self.save_file['lvl']
                self.xp = self.save_file['xp']
                self.money = self.save_file['money']
                self.inventory = self.save_file['inv']
        except:
            self.lvl = 0
            self.xp = 0
            self.money = 100
            self.inventory = {}
        self.save_file = {'lvl':self.lvl,
                          'xp':self.xp,
                          'money':self.money,
                          'inv':self.inventory}
        self.import_assets()
        self.setup(self.tmx_maps['{}'.format(map_n)], '{}'.format(spawn_p))

        

    #tiled files
    def import_assets(self):
            self.tmx_maps = {
                'world': load_pygame('STARTER TOWN.tmx'),
                'shop': load_pygame('shop.tmx'),
                'jungle1' : load_pygame('junglemap1.tmx'),
                'guildhall': load_pygame('guildhall.tmx'),
                }
        
            
    def setup(self, tmx_map, player_start_pos):
        #import tile maps
        for x, y, surf in tmx_map.get_layer_by_name('ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, world_layers['ground'])
        
        if map_n in ['shop','guildhall']:
            for x, y, surf in tmx_map.get_layer_by_name('table').tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE),
                        surf, (self.all_sprites,self.collision_sprites) ,
                          world_layers['house/tree'])
        #house
        for obj in tmx_map.get_layer_by_name('objects'):
            if str(obj.name).startswith('tree'):
                groups_tuple = (self.all_sprites)
            else:
                groups_tuple = (self.all_sprites,self.collision_sprites)
            if obj.image:
                Sprite((obj.x,obj.y), obj.image, groups_tuple, world_layers['house/tree'])  
        # transits
        for obj in tmx_map.get_layer_by_name('transit'):
            transit_sprite((obj.x,obj.y),
                           (obj.width,obj.height),
                           (obj.properties['target'],
                            obj.properties['pos']),
                            self.transition_sprites)  
                 
        for obj in tmx_map.get_layer_by_name('collisions'):
            border_sprite((obj.x,obj.y),pygame.Surface((obj.width,obj.height)),self.collision_sprites)

        for obj in tmx_map.get_layer_by_name('entities'):
            if obj.name == 'Player' and obj.properties['pos'] == player_start_pos:#player
                self.player = Player((obj.x, obj.y), 
                                     self.all_sprites, 
                                     world_layers['house/tree'],
                                     self.collision_sprites,
                                     self.save_file['lvl'],
                                     self.save_file['xp'],
                                     self.save_file['money'],
                                     self.save_file['inv'])
                self.curstats_ui = currentstats(self.player.health,
                                                self.xp,self.player.total_health,
                                                self.player.total_xp,
                                                self.player.money,
                                                self.player.level)
                self.player_light = lights()
                self.light_sprites.add(self.player_light)
            if obj.name == 'ShopNPC':#NPC
                npc_= npc(obj.properties['pos'],
                          (obj.x,obj.y),
                          world_layers['house/tree'],
                          obj.properties['name_'])
                self.all_sprites.add(npc_)
                self.npc_sprites.add(npc_)

            if obj.name == 'NPCinteract':#npc iteract rect
                self.interact_sprites.add(npc_interact(obj.pos,
                                                       [obj.x,obj.y,obj.width,obj.height],
                                                       obj.properties['name_'],))


        for obj in tmx_map.get_layer_by_name('entities'):
            if obj.image:
                Sprite((obj.x,obj.y),obj.image,self.all_sprites, world_layers['entity'])
        
        #spawns
        if map_n in lst_spawn_maps:
            for spawn in tmx_map.get_layer_by_name('spawns'):
                self.spawn_sprites.add(spawn_sprite((spawn.x,spawn.y),
                                                    self.spawn_sprites,
                                                    spawn.properties['pos'])) 
    
    def run(self):
            while True:
                #clock
                dt = clock.tick() / 1000
                 # player level up
                if self.xp >= self.player.total_xp:
                    self.player.level += 1
                    self.lvl = self.player.level
                    self.xp = 0
                    self.player.total_xp = self.player.level**5 + 100
                    self.player.total_health = self.player.level*5 + 100
                #save file
                self.save_file = {'lvl':self.lvl,
                                  'xp':self.xp,
                                  'money':self.money,
                                  'inv':self.inventory}
                with open('game_save','w') as game_save:
                    json.dump(self.save_file,game_save)

                #events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.save_file = {'lvl':self.lvl,
                                          'xp':self.xp,
                                          'money':self.money,
                                          'inv':self.inventory}
                        with open('game_save','w') as game_save:
                            json.dump(self.save_file,game_save)
                        pygame.quit()
                        exit()
                    #user event to spawn enemy
                    if event.type == self.ob_timer:
                        if map_n == 'jungle1' and len(self.enemy_sprites.sprites()) < 5:
                            spawn_pos = random.choice(self.spawn_sprites.sprites())
                            enem = random.choice(spawn_pos.mobs)
                            self.enemy_sprites.add(enemey((spawn_pos.x,spawn_pos.y),
                                                          (self.enemy_sprites,self.all_sprites),
                                                          world_layers['objects'],
                                                          self.collision_sprites,self.player,
                                                          random.randint(5,10),enem))
                    #to move enemy sprite
                    if event.type == self.move_time:
                        self.player.mov = True   
                        for e in self.enemy_sprites.sprites():
                            e.mov = True
                    #to change enemy direction 
                    if event.type == self.enemy_dir:
                        for e in self.enemy_sprites.sprites():
                            e.input()
                    # for day night cycle
                    if event.type == self.dark:
                        if self.dark_amt >= 200:
                            self.change = -1 
                        if self.dark_amt <= 0:
                            self.change = +1 
                        self.dark_amt += self.change
                    # to get mouse input
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse = pygame.mouse.get_pos()
                        #pause screen
                        if (mouse[0] in range(1250,1280) and mouse[1] in range(0,30)):
                            pause_screen =   Pause()
                            pause_screen.run(self.display_surface,(140,360),True) 
                    #to get keyboard input
                    keys = pygame.key.get_pressed()
                    #pause screen
                    if keys[pygame.K_ESCAPE]:
                        pause_screen =   Pause()
                        pause_screen.run(self.display_surface,(140,360),True)  
                    #to interact with npc
                    if keys[pygame.K_SPACE]:
                        for i in self.interact_sprites.sprites():
                            if self.player.rect.colliderect(i.rect):
                                for j in self.npc_sprites.sprites():
                                    if i.name == j.name:
                                        self.player.money,self.inventory = j.shop(self.display_surface,
                                                                                  self.player.money,
                                                                                  self.inventory)
                                        self.money = self.player.money
                    if keys[pygame.K_e]:
                        self.inv_obj = Inventory(self.inventory)
                        self.inv_obj.run(self.display_surface)
                self.transitions()#to call transition
                #enemy collision
                for enemy in self.enemy_sprites.sprites():        
                    if self.player.rect.colliderect(enemy.rect):
                        self.player.image = pygame.transform.scale(self.player.idle_images_lst[3],(100,100))
                        enemy.image = pygame.transform.scale(enemy.idle_images_lst[1],(100,100))
                        battle_screen = Battle(enemy,self.player,'jungle1')
                        self.battle_bool = True
                        self.enemy_sprites.remove(enemy)
                        self.all_sprites.remove(enemy)  
                                     
                #batttle
                if self.battle_bool:
                    health_,xp,drops = battle_screen.run(self.display_surface,(200,100),True)
                    self.battle_bool = False
                    if drops:
                        self.inventory[len(self.inventory)+1] = drops
                    self.player.health = health_
                    self.xp += xp
                    self.save_file = {'lvl':self.lvl,
                                      'xp':self.xp,
                                      'money':self.money,
                                      'inv':self.inventory}
                    print(self.save_file['xp'])
                    with open('game_save','w') as game_save:
                            json.dump(self.save_file,game_save) 
                    battle_screen.update(self.player.health)
                    
                #display
                self.all_sprites.update(dt)
                self.display_surface.fill('black')
                self.all_sprites.draw(self.player.rect.center)
                darker(self.display_surface,self.dark_amt)
                self.curstats_ui.update(self.player.health,
                                        self.player.total_health,
                                        self.xp,self.player.total_xp,
                                        self.player.money,
                                        self.player.level)
                self.curstats_ui.draw(self.display_surface,(0,620))
                self.light_sprites.update(self.dark_amt)
                self.light_sprites.draw(self.display_surface,100,
                                        (WINDOW_WIDTH/2,WINDOW_HEIGHT/2),
                                        self.player)
                
                pygame.display.update()
                
                #also for transition to other map
                if upd:
                    self.all_sprites.empty()
                    self.collision_sprites.empty()
                    self.transition_sprites.empty()
                    self.enemy_sprites.empty()
                    self.display_surface.fill('black')
                    self.transit()
                        
    #transition to other map       
    def transitions(self):
        global upd
        sprites = [sprite for sprite in self.transition_sprites
                    if sprite.rect.colliderect(self.player.hitbox)]
        if sprites:
            self.cur_target = sprites[0].target
            upd = True
              
    def transit(self):
        global map_n,spawn_p
        global upd
        map_n = self.cur_target[0]
        spawn_p = self.cur_target[1]
        self.save_file = {'lvl':self.lvl,
                          'xp':self.xp,
                          'money':self.money,
                          'inv':self.inventory}
        with open('game_save','w') as game_save:
            json.dump(self.save_file,game_save)
        self.setup(self.tmx_maps[self.cur_target[0]],self.cur_target[1])
        
        upd = False
        
        Game.run()
        
if __name__ == '__main__':
    Game = game()
    Game.run()
