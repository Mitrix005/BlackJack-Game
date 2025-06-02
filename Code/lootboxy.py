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
        self.height = 355
        self.is_open = False
        self.is_spinning = False
        self.spin_speed = 1
        self.selected_reward = None
        self.spin_progress = 0
        self.rarity = self.determinate_rarity()
        self.reward = self.load_rewards()
        self.current_texture = None
        self.open_sound = None
        self.animation_time = 0
        self.last_sound_time = 0
        self.czy_dzwiek = 0
        self.textura_skrzynki = pygame.image.load("../Graphics/paka.jpg")


    def determinate_rarity(self) -> Rarity:
        roll = random.random()
        if roll < 0.01: return Rarity.LEGENDARY                     #1% na legendary
        elif roll < 0.1: return Rarity.EPIC                         #9% na epic
        elif roll < 0.3: return Rarity.RARE                         #20% na rare
        else : return Rarity.COMMON                                 #70% na epica
        #return Rarity.LEGENDARY


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
                {"name": "skin11", "texture": pygame.image.load("../Graphics/rewers14.jpg")},
                {"name": "skin11", "texture": pygame.image.load("../Graphics/rewers15.jpg")},
                {"name": "skin11", "texture": pygame.image.load("../Graphics/rewers16.jpg")},
                {"name": "skin11", "texture": pygame.image.load("../Graphics/rewers17.jpg")},
                {"name": "skin11", "texture": pygame.image.load("../Graphics/rewers13.jpg")},
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
    def load_sounds(self, open_sound : pygame.mixer.Sound, spin_sound : pygame.mixer.Sound, jackpot_sound : pygame.mixer.Sound, case_opened : pygame.mixer.Sound) -> None:
        self.open_sound = open_sound
        self.spin_sound = spin_sound
        self.jackpot_sound = jackpot_sound
        self.case_opened =  case_opened


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
        current_time = pygame.time.get_ticks()
        if self.is_spinning:
            self.spin_progress = self.spin_progress + self.spin_speed
            #dodanie animacji spinowania
            if int(self.spin_progress) % 5 ==0:
                all_rewards = []
                for rarity in self.reward.values():
                    all_rewards.extend(rarity)
                random_reward = random.choice(all_rewards)
                self.current_texture = random_reward["texture"]
                if int(self.spin_progress) <96:
                    self.spin_sound.play()
                self.spin_speed -=0.023
            if self.spin_progress >= 100:
                self.is_spinning = False
                self.is_open = True
                self.select_reward()
                self.animation_time = pygame.time.get_ticks()
            if self.spin_sound and current_time - self.last_sound_time > 300: #naprawiono nakładajacy sie dzwiek spinow
                #self.spin_sound.play()
                self.last_sound_time = current_time
        elif self.spin_progress <= 100:
            self.current_texture = self.textura_skrzynki

    def draw(self, screen : pygame.Surface):
        #kszynka
        pygame.draw.rect(screen, (50, 50, 50), (self.x, self.y, self.width, self.height))
        #rysowanko tektury
        if self.current_texture:
            texture = pygame.transform.scale(self.current_texture, (self.width -20, self.height-20))
            screen.blit(texture, (self.x +10, self.y +10))
        #otwarcie
        if self.is_open and self.selected_reward:
            self.draw_reward_info(screen)

    def draw_reward_info(self, screen : pygame.Surface):
        font = pygame.font.SysFont("Arial", 24, bold=True)

        #kolor tekstu
        color = {
            Rarity.COMMON : (255, 255, 255),    #murzynski
            Rarity.RARE : (0, 100, 255),        #niebieski
            Rarity.EPIC : (150, 0, 255),        #fioletowy
            Rarity.LEGENDARY : (255, 165, 0 ),  #złoty

        }.get(self.rarity, (255,255,255))
        if self.rarity.value == "legendary" and self.czy_dzwiek == 0:
            self.jackpot_sound.play()
            self.czy_dzwiek = 1
        elif self.czy_dzwiek == 0:
            self.case_opened.play()
            self.czy_dzwiek =1


        text = font.render(f"{self.selected_reward["name"]} ({self.rarity.name})", True, color)
        screen.blit(text, (self.x, self.y -25))

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


