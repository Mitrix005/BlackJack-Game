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
        is_hovered = self.rect.collidepoint(mouse)
        pygame.draw.rect(screen, self.hover_color if is_hovered else self.color, self.rect)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(centerx=self.rect.centerx, centery=self.rect.centery)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    return True
        return False

pygame.init()

SCREEN_WIDTH = 1472
SCREEN_HEIGHT = 832

main_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BlackJack-Game")

button = Button(main_screen,300,100,200, 60,"Button", (40,40,40),(32,32,32))

gamble_button = Button(main_screen, 300, 200, 200, 60, "$Gamble$", (255,215,0), (255,190,0))

#Zmienne Gry

base_dir = os.path.dirname(__file__)

main_menu_audio_path = os.path.join(base_dir,'../Audio/menu_theme.mp3')

jackpot_audio_path = os.path.join(base_dir,'../Audio/Jackpot.wav')

main_menu_background_path = os.path.join(base_dir,'../Graphics/menu_background.jpg')

logo_path = os.path.join(base_dir,'../Graphics/logo.jpg')

main_menu_audio = pygame.mixer.Sound(main_menu_audio_path)
main_menu_audio.set_volume(0.5)

jackpot_sound = pygame.mixer.Sound(jackpot_audio_path)
jackpot_sound.set_volume(0.5)

main_menu_background = pygame.image.load(main_menu_background_path)

logo = pygame.image.load(logo_path)

pygame.display.set_icon(logo)

running = True
main_menu_audio.play()
while running:
    #main_screen.fill((105, 105, 105))
    main_screen.blit(main_menu_background, (0, 0))

    button.draw(main_screen)

    gamble_button.draw(main_screen)


    for event in pygame.event.get():
        if button.handle_event(event):
            print("siggma")
        if gamble_button.handle_event(event):
            jackpot_sound.play()
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
pygame.quit()