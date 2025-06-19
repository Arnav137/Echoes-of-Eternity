import pygame
import time
import threading

black = (0,0,0)

def get_key(spritesheet,height,width,letter,colour,size):#to get image from spritesheet
    sheet = pygame.image.load(spritesheet)
    image = pygame.Surface((width,height)).convert_alpha()
    letters =  ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    x_pos = letters.index(letter)%5
    y_pos = letters.index(letter)//5
    image.blit(sheet,(0,0),(width*x_pos,height*y_pos,width,height))
    image.set_colorkey(colour)
    image = pygame.transform.scale(image,(size,size))
    return image

def text_form(text,sze,font):
    txt = str(text)
    text_surf = pygame.surface.Surface((sze*(len(txt)),sze)).convert_alpha()
    text_surf.set_colorkey(black)
    x = 0 
    for i in text:
        
        text_surf.blit(get_key(str(font),16,16,i.upper(),black,sze),(sze*(x),0))
        x += 1
    return text_surf

def get_image(spritesheet,height,width,x_pos,y_pos,colour):#to get image from spritesheet
    sheet = pygame.image.load(spritesheet)
    if not(spritesheet == 'images\player no 1.png'):
        sheet = pygame.transform.scale(sheet,(300,400))
    else:
        sheet = pygame.transform.scale(sheet,(128,72))
    image = pygame.Surface((width,height)).convert_alpha()
    image.blit(sheet,(0,0),(width*x_pos,height*y_pos,width,height))
    image.set_colorkey(colour)
    return image
