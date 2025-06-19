import pygame
from pygame.math import Vector2 as vector 
from sys import exit 
import random

pygame.init()

clock = pygame.time.Clock()

#window properties
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TILE_SIZE = 100


#used to check order of bliting surfaces
world_layers = {
'ground' : 0 ,
'house/tree' : 2 ,
'objects' : 3 ,
}

#fonts:
size20 = pygame.font.SysFont('FreeMono,Monospace',20)
size20_bold = pygame.font.SysFont('freesansbold', 20)
size22 = pygame.font.SysFont('FreeMono,Monospace', 22)
size12 = pygame.font.SysFont('FreeMono,Monospace', 12)
size30 = pygame.font.SysFont('freesansbold', 30)
size25 = pygame.font.SysFont('FreeMono,Monospace', 25)
size50 = pygame.font.SysFont('freesansbold', 50) 

black = (0,0,0)