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
    def __init__(self, x : int, y : int) -> None:
        self.x = x
        self.y = y
        self.width = 200
        self.height = 200
        self.is_open = False
        self.is_spinning = False
        self.spin_speed = 1.5
        self.selected_reward = None
        self.spin_progress = 0
        self.rarity = self.determinate_rarity()
        self.color = self.rarity.value
        self.reward = self.load_rewards()
        self.current_texture = None
        self.open_sound = None


    def determinate_rarity(self) -> Rarity:
        roll = random.random()
        if roll < 0.01: return Rarity.LEGENDARY
        elif roll < 0.1: return Rarity.EPIC
        elif roll < 0.3: return Rarity.RARE
        else : return Rarity.COMMON

    def load_rewards(self) -> dict:
        return{
            Rarity.COMMON : [
                {"name" : "czarmuch", "texture" : pygame.image.load("../Graphics/rewers2.png")}
            ]
            Rarity.RARE : [
                {"name" : "garnuch", "texture" : pygame.image.load("../Graphics/")}
            ]
        }



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


