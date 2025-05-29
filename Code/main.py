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
        self.active = True

    def draw(self, screen):
        if not self.active:
            return False
        mouse = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse)
        pygame.draw.rect(screen, self.hover_color if is_hovered else self.color, self.rect)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(centerx=self.rect.centerx, centery=self.rect.centery)
        screen.blit(text_surf, text_rect)
        return True

    def handle_event(self, event):
        if not self.active:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    return True
        return False

class Sound:
    def __init__(self,path):
        self.path = path
        self.running = None
        self.s = None #sound
        self.type = type
        self.load()

    def load(self):
        base_dir = os.path.dirname(__file__)
        file = os.path.join(base_dir, self.path)
        sound=pygame.mixer.Sound(file)
        self.s=sound


class MusicManager:
    def __init__(self):
        self.menu_music_path = self.load("../Audio/menu_theme.mp3")
        self.game_music_path = self.load('../Audio/soundtrack.mp3')
        self.state = None

    def play_menu(self):
        if self.state != "MENU":
            pygame.mixer.music.load(self.menu_music_path)
            pygame.mixer.music.play(-1)
            self.state = "MENU"

    def play_game(self):
        if self.state != "GAME":
            pygame.mixer.music.load(self.game_music_path)
            pygame.mixer.music.play(-1)
            self.state = "GAME"

    def stop_music(self):
        pygame.mixer.music.stop()
        self.state = None

    def load(self, path):
        base_dir = os.path.dirname(__file__)
        file = os.path.join(base_dir, path)
        return file

class ImageManager:
    def __init__(self, path):
        base_dir = os.path.dirname(__file__)
        directory = os.path.join(base_dir, path)
        self.base_dir = directory
        self.cache = {}

    def load(self, filename):
        if filename not in self.cache:
            path = os.path.join(self.base_dir, filename)
            picture = pygame.image.load(path).convert()
            self.cache[filename] = picture
        return self.cache[filename]


pygame.init()

SCREEN_WIDTH = 1472
SCREEN_HEIGHT = 832

main_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BlackJack-Game")

play_button = Button(main_screen,636,400,200, 60,"Play", (40,40,40),(32,32,32))

gamble_button = Button(main_screen, 636, 500, 200, 60, "$ Gamble $", (255,215,0), (255,190,0))

quit_button = Button(main_screen, 636, 600, 200, 60, "Quit", (40,40,40), (32,32,32))

back_to_menu = Button(main_screen,1100, 650, 200, 60, "Back", (40,40,40),(32,32,32))

#Zmienne Gry
music_manager = MusicManager()
image_manager = ImageManager('../Graphics')

jackpot_sound = Sound('../Audio/Jackpot.wav')

main_menu_background=image_manager.load("menu_background.jpg")
logo=image_manager.load("logo.jpg")
table=image_manager.load("stol.jpg")

pygame.mixer.music.set_volume(0.5)
jackpot_sound.s.set_volume(0.5)

pygame.display.set_icon(logo)

state="MENU"

menu_music_playing=False
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if state=="MENU":
            if play_button.handle_event(event):
                state="GAME"
            if gamble_button.handle_event(event):
                jackpot_sound.s.play()
            if quit_button.handle_event(event):
                running = False
        if state=="GAME":
            back_to_menu.draw(main_screen)
            if back_to_menu.handle_event(event):
                state="MENU"



    if state == "MENU":
        if music_manager.state!="MENU":
            music_manager.play_menu()
        back_to_menu.active = False
        play_button.active = True
        gamble_button.active = True
        quit_button.active = True

        main_screen.blit(main_menu_background, (0, 0))

        play_button.draw(main_screen)

        gamble_button.draw(main_screen)

        quit_button.draw(main_screen)
    if state == "GAME":
        play_button.active = False
        gamble_button.active = False
        quit_button.active = False
        back_to_menu.active = True
        if music_manager.state!="GAME":
            music_manager.play_game()

        main_screen.blit(table, (0, 0))
        back_to_menu.draw(main_screen)


    pygame.display.flip()
pygame.quit()