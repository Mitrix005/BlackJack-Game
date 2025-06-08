import configparser
from locale import currency

import pygame
import random
import sys
import time
from enum import Enum
from rarity import Rarity

pygame.init()

config = configparser.ConfigParser()
config_file = 'config.cfg'

class Inventory():
    def __init__(self, x : int, y : int) -> None:
        self.x = x
        self.y = y
        self.width = 200
        self.height = 355
        self.my_cards = []
        self.load_from_config()
        self.type = Rarity.COMMON
        self.all_cards = {
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

    def load_from_config(self):
        config.read(config_file)
        cards = config.get('Shelf', 'cards', fallback='')
        self.my_cards = cards.split(',')

    def change_type(self, type1: Rarity):
        self.type = type1

    def add_card(self, name: str):
        config.read(config_file)
        current_cards_str = config.get('Shelf', 'cards', fallback='')
        current_cards = [card.strip() for card in current_cards_str.split(',') if card.strip()]

        if name not in current_cards:
            current_cards.append(name)
            updated_cards_str = ','.join(current_cards)
            config.set('Shelf', 'cards', updated_cards_str)

            with open(config_file, 'w') as configfile:
                config.write(configfile)

    def draw(self, screen : pygame.Surface):
        gap = 300
        i=1
        for skin in self.all_cards[self.type]:
            if skin['name'] in self.my_cards:
                texture = skin["texture"]
                scaled_texture = pygame.transform.scale(texture, (self.width - 10, self.height - 60))
                screen.blit(scaled_texture, (-170 + i * gap, 250))
                i += 1

