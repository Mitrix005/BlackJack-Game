import pygame
import sys

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moja gra w Pygame")

# Kolory (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Zegar do kontrolowania FPS
clock = pygame.time.Clock()
FPS = 60

# Główna pętla gry
running = True
while running:
    # Obsługa zdarzeń
    #for event in pygame.event.get():
       # if event.type == pygame.QUIT:
           # running = False

    # Logika gry tutaj

    # Czyszczenie ekranu
    #screen.fill(BLACK)

    # Rysowanie na ekranie tutaj

    # Aktualizacja ekranu
    #pygame.display.flip()

    # Kontrola FPS
#clock.tick(FPS)

# Zakończenie Pygame
pygame.quit()
sys.exit()
