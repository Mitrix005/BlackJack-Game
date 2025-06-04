import configparser

import pygame
import random
import sys
import time
from enum import Enum
from lootboxy import Rarity

pygame.init()

config = configparser.ConfigParser()
config_file = 'config.cfg'

class Inventory():
    def __init__(self, x : int, y : int) -> None:
        self.x = x
        self.y = y
        self.width = 200
        self.height = 355
        self.load_from_config()
        self.textura_skrzynki = pygame.image.load("../Graphics/paka.jpg")
        self.all_cards = \
            [{"name" : "skin2", "texture" : pygame.image.load("../Graphics/rewers2.jpg")},
            {"name": "skin11", "texture": pygame.image.load("../Graphics/rewers14.jpg")}]



#Określenie jaki skin jest jak rzadki

    def load_from_config(self):
        config.read(config_file)

        if not config.has_section('Shelf'):
            config.add_section('Shelf')
            config.set('Shelf', "cards", "skin1")

            with open(config_file, 'w') as configfile:
                config.write(configfile)

    def get_cards(self):
        config.read(config_file)
        if config.has_section('Shelf'):
            cards = config.get('Shelf', 'cards', fallback='')
            lista = cards.split(',')
            print("Karty w inwentarzu:", lista if cards else "Brak kart")

        else:
            print("Brak sekcji Shelf w configu.")

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


        text = font.render(f"{self.selected_reward['name']} ({self.rarity.name})", True, color)
        screen.blit(text, (self.x, self.y -25))

    pass

i = Inventory(100, 200)
i.add_card('skin2')
i.get_cards()

