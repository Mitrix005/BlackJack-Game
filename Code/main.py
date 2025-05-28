import pygame
import os

class Button:
    def __init__(self, screen, x, y, width, height, text, color, hover_color, text_color=(255, 255, 255), font=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.screen = screen
        self.text = text
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = font or pygame.font.SysFont(None, 36)

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()[0]
        is_hovered = self.rect.collidepoint(mouse)
        pygame.draw.rect(screen, self.hover_color if is_hovered else self.color, self.rect)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(centerx=self.rect.centerx, centery=self.rect.centery)
        screen.blit(text_surf, text_rect)

        return is_hovered and clicked

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

main_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

button = Button(main_screen,300,100,200, 60,"Button", (40,40,40),(32,32,32))

gamble_button = Button(main_screen, 300, 200, 200, 60, "$Gamble$", (255,215,0), (255,190,0))

base_dir = os.path.dirname(__file__)
jackpot_audio_path = os.path.join(base_dir, '..', 'Audio', 'Jackpot.wav')
jackpot_audio_path = os.path.normpath(jackpot_audio_path)


jackpot_sound = pygame.mixer.Sound(jackpot_audio_path)
jackpot_sound.set_volume(0.1)

running = True
while running:
    main_screen.fill((105, 105, 105))

    if button.draw(main_screen):
        print("Sigma")

    if gamble_button.draw(main_screen):
        jackpot_sound.play()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
pygame.quit()