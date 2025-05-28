import pygame
#Ale gówno
pygame.init()
#Co my żyjemy pod kamieniem? Zrób 1280x720 przynajmniej
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#Po chuj ci running jak to i tak nie działa?
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
#Tak to każdy umie wychodzić!
pygame.quit
#cwelu
