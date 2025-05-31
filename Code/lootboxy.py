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


#Określenie jaki skin jest jak rzadki

    def load_rewards(self) -> dict:
        return{
            Rarity.COMMON : [
                {"name" : "skin1", "texture" : pygame.image.load("../Graphics/rewers1.jpg")},
                {"name": "skin6", "texture": pygame.image.load("../Graphics/rewers6.jpg")},
                {"name": "skin7", "texture": pygame.image.load("../Graphics/rewers7.jpg")},
                {"name": "skin8", "texture": pygame.image.load("../Graphics/rewers8.jpg")},
                {"name": "skin9", "texture": pygame.image.load("../Graphics/rewers9.jpg")},
                {"name": "skin10", "texture": pygame.image.load("../Graphics/rewers10.jpg")},

            ],
            Rarity.RARE : [
                {"name" : "skin2", "texture" : pygame.image.load("../Graphics/rewers2.jpg")},
                {"name": "skin11", "texture": pygame.image.load("../Graphics/rewers11.jpg")},
            ],
            Rarity.EPIC : [
                {"name" : "skin4", "texture" : pygame.image.load("../Graphics/rewers4.jpg")},
                {"name": "skin12", "texture": pygame.image.load("../Graphics/rewers12.jpg")},
            ],
            Rarity.LEGENDARY : [
                {"name": "skin5", "texture": pygame.image.load("../Graphics/rewers5.jpg")},
                {"name": "skin13", "texture": pygame.image.load("../Graphics/rewers13.jpg")},
            ]
        }
    def load_sounds(self, open_sound : pygame.mixer.Sound, spin_sound : pygame.mixer.Sound) -> None:
        self.open_sound = open_sound
        self.spin_sound = spin_sound

    def open(self):
        if not self.is_open and not self.is_spinning:
            self.is_spinning = True
            self.spin_progress = 0
            if self.open_sound:
                self.open_sound.play()

    def select_reward(self):
        reward_pool = self.reward[self.rarity]
        self.selected_reward = random.choice(reward_pool)
        self.current_texture = self.selected_reward["texture"]


    def update(self):
        if self.is_spinning:
            self.spin_progress = self.spin_progress + self.spin_speed
            if self.spin_progress >= 100:
                self.is_spinning = False
                self.is_open = True
                self.select_reward()
            elif self.spin_sound and int(self.spin_progress) % 10 ==0:
                self.spin_sound.play()




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


