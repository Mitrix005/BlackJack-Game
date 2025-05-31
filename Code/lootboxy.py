import pygame
import random
import sys
import time
from enum import Enum
pygame.init()

'''
SZEROKOSC_EKRANU: int = 1920
WYSOKOSC_EKRANU: int = 1080
'''

class Rarity(Enum):
    COMMON = "common"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"

class Lootbox():

    pass





'''
screen = pygame.display.set_mode((SZEROKOSC_EKRANU, WYSOKOSC_EKRANU))
pygame.display.set_caption("Skrzynki")
clock = pygame.time.Clock()

asik = pygame.image.load('../Graphics/logo.jpg').convert()
asik = pygame.transform.scale(asik,(100,100))
running = True
x=0
while running:
    screen.fill((255,255,255))
    screen.blit(asik, (x,100))

    x+=1
    for event in pygame.event.get():
        if event.type == pygame.quit:
            running = False


    pygame.display.flip()
    clock.tick(60)


pygame.quit()
'''


