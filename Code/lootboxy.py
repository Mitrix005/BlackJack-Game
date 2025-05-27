import pygame
import random
import sys
import time

pygame.init()


SZEROKOSC_EKRANU: int = 800
WYSOKOSC_EKRANU: int = 600


screen = pygame.display.set_mode((SZEROKOSC_EKRANU, WYSOKOSC_EKRANU))
pygame.display.set_caption("Skrzynki")
