import pygame
import os
import configparser

from lootboxy import Lootbox

import random


from pygame import SurfaceType      # potrzebne do adnotacji
from pygame.mixer import Sound      # potrzebne do adnotacji
from pygame.font import Font        # potrzebne do adnotacji
from pygame.event import EventType  # potrzebne do adnotacji

# funkcja która ustawia main_screen na fullscreen albo na okienko i zarazem wybiera dobra wielkosc background
def toggle_fullscreen(info : bool, background : SurfaceType = None,  filename : str = None) -> SurfaceType:
    global main_screen
    if info:
        main_screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        if background == None:
            return pygame.Surface(main_screen.get_size())
        else:
            background = image_manager.scaled(filename, main_screen.get_size())
            return background
    else:
        main_screen = pygame.display.set_mode((1472,832))
        if background == None:
            return pygame.Surface((1472,832))
        else:
            background = image_manager.scaled(filename,(1472,832))
            return background


# plik konfiguracyjny
config = configparser.ConfigParser()
config_file = 'config.cfg'

# domyslny config
default_settings = {
    'Display': {'fullscreen': 'True'}
}

current_lootbox = None
lootbox_active = False

# sprawdza czy istnieje config, jak nie to go tworzy i uzupełnia z default_settings (config jest tylko lokalny i jest w .gitignore)
if not os.path.isfile(config_file):
    for section, options in default_settings.items():
        config[section] = options
        with open(config_file,'w') as configfile:
            config.write(configfile)
else:
    config.read(config_file)

# wczytanie config
fullscreen = config.getboolean('Display','fullscreen')
# koniec pliku konfiguracyjnego

# klasa tworzaca przycisk
# (ekran na ktorym wyswietlamy, pozycja ile pikseli od lewego gornego rogu otwartego okna(x,y), rozmiar przycisku, tekst na przycisku, kolor przycisku, odglos klikniecia, kolor tekstu, czcionka)
class Button:
    def __init__(self, screen : SurfaceType, x : int, y : int, width : int, height : int, text : str, color : tuple, hover_color : tuple, click_sound : Sound = None, text_color : tuple = (255, 255, 255), font : Font = None) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.click_sound = click_sound
        self.screen = screen
        self.text = text
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = font or pygame.font.SysFont(None, 36)
        self.active = True
    #rysuje przycisk
    def draw(self, screen : SurfaceType) -> None:
        if not self.active:
            return None
        mouse = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse)
        pygame.draw.rect(screen, self.hover_color if is_hovered else self.color, self.rect)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(centerx=self.rect.centerx, centery=self.rect.centery)
        screen.blit(text_surf, text_rect)
        return None

    # sprawdza czy przycisk zostal klikniety
    def handle_event(self, event : EventType) -> bool:
        if not self.active:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    if self.click_sound == None:
                        return True
                    else:
                        self.click_sound.s.play()
                    return True
        return False
# klasa sluzaca inicjalizowaniu odglosow w prosty sposob, aby uzyskac dzwiek trzeba uzyc .s
class Sound:
    def __init__(self, path : str) -> None:
        self.path = path
        self.running = None
        self.s = None
        self.type = type
        self.load()

    def load(self) -> None:
        base_dir = os.path.dirname(__file__)
        file = os.path.join(base_dir, self.path)
        sound=pygame.mixer.Sound(file)
        self.s=sound

# klasa sluzaca do odtwarzania glownej muzyki
class MusicManager:
    def __init__(self) -> None:
        self.menu_music_path = self.load("../Audio/menu_theme.mp3")
        self.game_music_path = self.load('../Audio/game_theme_low_stakes.mp3')
        self.gamble_music_path = self.load("../Audio/case_theme.wav")
        self.state = None

    def play_menu(self) -> None:
        if self.state != "MENU":
            pygame.mixer.music.load(self.menu_music_path)
            pygame.mixer.music.play(-1)
            self.state = "MENU"

    def play_game(self) -> None:
        if self.state != "GAME":
            pygame.mixer.music.load(self.game_music_path)
            pygame.mixer.music.play(-1)
            self.state = "GAME"


    def play_gamble(self) -> None:
        if self.state != "GAMBLE":
            pygame.mixer.music.load(self.gamble_music_path)
            pygame.mixer.music.play(-1)
            self.state = "GAMBLE"



    def stop_music(self) -> None:
        pygame.mixer.music.stop()
        self.state = None

    def load(self, path) -> str:
        base_dir = os.path.dirname(__file__)
        file = os.path.join(base_dir, path)
        return file

# klasa ktora inicjalizuje zdjecia i przetrzymuje odrazu w slowniku
class ImageManager:
    def __init__(self, path) -> None:
        base_dir = os.path.dirname(__file__)
        directory = os.path.join(base_dir, path)
        self.base_dir = directory
        self.cache = {}
        self.scaled_cache = {}

    # zwykle zdjecia
    def load(self, filename : str) -> SurfaceType:
        if filename not in self.cache:
            path = os.path.join(self.base_dir, filename)
            picture = pygame.image.load(path).convert()
            self.cache[filename] = picture
        return self.cache[filename]

    # przeskalowane zdjecia
    def scaled(self, filename : str, size : tuple) -> SurfaceType:
        if (filename, size) not in self.scaled_cache:
            path = os.path.join(self.base_dir, filename)
            picture = pygame.image.load(path).convert()
            picture = pygame.transform.scale(picture, size)
            self.scaled_cache[(filename,size)] = picture
        return self.scaled_cache[(filename, size)]

#klasa implementująca logikę gry
class Game_Logic:
    def __init__(self): #początkowy stan przed rozpoczęciem gry
        self.reset()

    def reset(self) -> None:
        self.deck = [value + suit for value in '23456789TJQKA' for suit in '♠♥♦♣']
        random.shuffle(self.deck)
        self.player_hand=[]
        self.dealer_hand=[]
        self.player_standing = False
        self.result = ""
        self.deal_initial_cards()

    def deal_initial_cards(self) -> None:  #dobranie kart na początku
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]

    def hand_value(self, hand):  #liczenie wartości ręki gracza
        score = 0
        aces = 0
        for card in hand:
            rank = card[0]
            if rank in 'TJQK':
                score += 10
            elif rank == 'A':
                aces += 1
                score += 11
            else:
                score += int(rank)
        while score > 21 and aces:
            value -= 10
            aces -= 1
        return score

    def hit(self): #dobranie karty przez garcza
        if not self.player_standing and self.result == "":
            self.player_hand.append(self.deck.pop())
            if self.hand_value(self.player_hand) > 21:
                self.result = "Bust! Dealer wins."

    def stand(self): #gracz przestaje dobierać karty
        if not self.player_standing and self.result == "":
            self.player_standing = True
            while self.hand_value(self.dealer_hand) < 17:
                self.dealer_hand.append(self.deck.pop())
            self.winner()

    def winner(self): # wybór zwycięzcy
        player = self.hand_value(self.player_hand)
        dealer = self.hand_value(self.dealer_hand)
        if dealer > 21:
            self.result = "You win"
        elif player > dealer:
            self.result = "You win"
        elif dealer == player:
            self.result = "Draw"
        else:
            self.result = "Dealer wins"

    # zainicjowanie gry
pygame.init()

# domyslny rozmiar okna
SCREEN_WIDTH = 1472
SCREEN_HEIGHT = 832

# sprawdzenie czy wlaczamy w fullscreen
if fullscreen:
    main_screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
else:
    main_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# nazwa okienka gry
pygame.display.set_caption("BlackJack-Game")

# dzwieki
jackpot_sound = Sound('../Audio/Jackpot.wav')
jackpot_sound.s.set_volume(0.5)
lootbox_open_sound = Sound("../Audio/case_opening.wav")
lootbox_open_sound.s.set_volume(0.5)
lootbox_spin_sound = Sound("../Audio/case_spin.wav")
lootbox_spin_sound.s.set_volume(0.5)
button_click_sound = Sound('../Audio/rozdanie_karty.mp3')
button_click_sound.s.set_volume(0.5)

# przyciski

play_button = Button(main_screen,636,400,200, 60,"Play", (40,40,40),(32,32,32), button_click_sound)

gamble_button = Button(main_screen, 636, 500, 200, 60, "$ Gamble $", (255,215,0), (255,190,0), button_click_sound)

quit_button = Button(main_screen, 636, 700, 200, 60, "Quit", (40,40,40), (32,32,32), button_click_sound)

back_to_menu = Button(main_screen,1100, 650, 200, 60, "Back", (40,40,40),(32,32,32), button_click_sound)

options_button = Button(main_screen,  636,600, 200, 60, "Options", (40,40,40), (32,32,32), button_click_sound)

fullscreen_button_info = Button(main_screen,300, 300, 200, 60, "Fullscreen", (40,40,40), (40,40,40))

fullscreen_button= Button(main_screen, 600, 300, 200, 60, "", (40,40,40), (32,32,32), button_click_sound)

hit_button = Button(main_screen, 636,400,200, 60,"Hit", (40,40,40),(32,32,32), button_click_sound)

stand_button = Button(main_screen, 636,500,200, 60,"Stand", (40,40,40),(32,32,32), button_click_sound)

deal_button = Button(main_screen, 636,700,200, 60,"Deal", (40,40,40),(32,32,32), button_click_sound)

buttons = [play_button, gamble_button, quit_button, back_to_menu, options_button, fullscreen_button_info, fullscreen_button, hit_button, stand_button, deal_button]


# Zmienne Gry
music_manager = MusicManager()
image_manager = ImageManager('../Graphics')


# wczytanie obrazow
main_menu_background=image_manager.load("menu_background.jpg")
logo=image_manager.load("logo.jpg")
table=image_manager.load("stol.jpg")
case_background = image_manager.load("case_background.jpg")

# backgrounds
main_menu_background=toggle_fullscreen(fullscreen,main_menu_background,"menu_background.jpg")
table=toggle_fullscreen(fullscreen,table,"stol.jpg")
case_background = toggle_fullscreen(fullscreen,case_background, "case_background.jpg")
# glosnosc glownej muzyki
pygame.mixer.music.set_volume(0.5)

# ustawienie logo
pygame.display.set_icon(logo)

state = "MENU" # stan gry
running = True # czy gra dziala
while running:

    for event in pygame.event.get():                            #petla zdarzen
        if event.type == pygame.QUIT:
            running = False
        if state == "MENU":                                     # wszystkie zdarzenia w menu
            if play_button.handle_event(event):
                state = "GAME"
            if gamble_button.handle_event(event):
                jackpot_sound.s.play()
                state = "GAMBLE"
            if options_button.handle_event(event):
                state = "OPTIONS"
            if quit_button.handle_event(event):
                running = False
        if state == "GAMBLE":
            if back_to_menu.handle_event(event):
                state = "MENU"
                current_lootbox = None
                lootbox_active = False

        if state == "GAME":                                     # wszystkie zdarzenia w game
            if back_to_menu.handle_event(event):
                state = "MENU"
        if state == "OPTIONS":                                  # wszystkie zdarzenia w options
            if back_to_menu.handle_event(event):
                state="MENU"
            if fullscreen_button.handle_event(event):
                fullscreen = not fullscreen

                if fullscreen:
                    config.set('Display', 'fullscreen', 'True')
                else:
                    config.set('Display', 'fullscreen', 'False')
                with open(config_file, 'w') as configfile:
                    config.write(configfile)

                main_menu_background=toggle_fullscreen(fullscreen,main_menu_background,"menu_background.jpg")
                table=toggle_fullscreen(fullscreen,table,"stol.jpg")
                case_background = toggle_fullscreen(fullscreen, case_background, "case_background.jpg")



    if state == "MENU":                                                 #zarzadzanie muzyka i rysowaniem obiektow
        if music_manager.state != "MENU":
            music_manager.play_menu()

        back_to_menu.active = False
        play_button.active = True
        gamble_button.active = True
        options_button.active = True
        quit_button.active = True
        fullscreen_button.active = False
        fullscreen_button_info.active = False

        main_screen.blit(main_menu_background, (0, 0))

        play_button.draw(main_screen)
        options_button.draw(main_screen)
        gamble_button.draw(main_screen)
        quit_button.draw(main_screen)

    if state == "GAME":
        play_button.active = False
        gamble_button.active = False
        options_button.active = False
        quit_button.active = False
        back_to_menu.active = True
        fullscreen_button.active = False
        fullscreen_button_info.active = False

        if music_manager.state != "GAME":
            music_manager.play_game()

        main_screen.blit(table, (0, 0))

        back_to_menu.draw(main_screen)

    if state == "OPTIONS":
        play_button.active = False
        gamble_button.active = False
        options_button.active = False
        quit_button.active = False
        fullscreen_button.active = True
        fullscreen_button_info.active = True
        back_to_menu.active = True

        fullscreen_button.text = "Yes" if fullscreen else "No"

        main_screen.blit(main_menu_background, (0,0))

        fullscreen_button.draw(main_screen)
        fullscreen_button_info.draw(main_screen)
        back_to_menu.draw(main_screen)


    if state == "GAMBLE":

        play_button.active = False
        gamble_button.active = False
        options_button.active = False
        quit_button.active = False
        fullscreen_button.active = False
        fullscreen_button_info.active = False
        back_to_menu.active = True

        main_screen.blit(case_background, (0, 0))
        back_to_menu.draw(main_screen)

        if music_manager.state != "GAMBLE":
            music_manager.play_gamble()

        if current_lootbox is None:
            current_lootbox = Lootbox(
                x = main_screen.get_width()//2 -100,
                y = main_screen.get_height()//2 -250,


            )
            current_lootbox.load_sounds(
                open_sound = lootbox_open_sound.s,
                spin_sound =  lootbox_spin_sound.s,
                jackpot_sound = jackpot_sound.s

            )
            current_lootbox.animation_time = pygame.time.get_ticks()

        #rysowanko
        if current_lootbox:
            current_lootbox.update()
            current_lootbox.draw(main_screen)
            #przycisk Otwórz kszynke kiedy lootbox sienie kreci
            open_case_button = Button(
                main_screen, main_screen.get_width()//2 -100, 800 ,200,60,
                "Otwórz kszynke", (255, 190, 0), (255, 190, 0), button_click_sound
            )
            open_case_button.active = (current_lootbox is None or (not current_lootbox.is_spinning and not current_lootbox.is_open))
            open_case_button.draw(main_screen)

        #obsługa przycisku


        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and open_case_button.handle_event(event):
                current_lootbox.open()
                lootbox_active = True
                current_lootbox.animation_time = pygame.time.get_ticks()

        #resecik
        if lootbox_active and not current_lootbox.is_spinning:
            if pygame.time.get_ticks() - current_lootbox.animation_time > 5000:  # 5 sekund
                lootbox_active = False
                current_lootbox = None


    pygame.display.flip() #odswiezenie ekranu
pygame.quit() #wyjscie z gry