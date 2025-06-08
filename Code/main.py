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

#funkcja do wczytania pliku tekstowego z instrukcja
def load_instructions(path="instrukcja_dla_gracza.txt"):
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as file:
            return file.readlines()
    return ["Brak instrukcji"]

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

        if fullscreen:
            screen_width, screen_height = main_screen.get_size()
            scaled_x = self.x
            scaled_y = self.y
            scaled_x = scaled_x*(screen_width/1472)
            scaled_y = scaled_y*(screen_height/832)
            self.rect = pygame.Rect(scaled_x, scaled_y, self.width, self.height)
            mouse = pygame.mouse.get_pos()
            is_hovered = self.rect.collidepoint(mouse)
            pygame.draw.rect(screen, self.hover_color if is_hovered else self.color, self.rect)
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(centerx=self.rect.centerx, centery=self.rect.centery)
            screen.blit(text_surf, text_rect)
            return None
        if not fullscreen:
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
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
        self.deck = []
        self.player_hand = []
        self.dealer_hand = []
        self.player_standing = False
        self.result = ""

    def reset(self):
        self.deck = [value + suit for value in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
                         for suit in '♠♥♦♣']
        random.shuffle(self.deck)
        self.player_hand = []
        self.dealer_hand = []
        self.player_standing = False
        self.result = ""
        self.deal_initial_cards()

    def reset_deck(self):
        self.deck = [value + suit for value in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
                     for suit in '♠♥♦♣']
        random.shuffle(self.deck)


    def deal_initial_cards(self):
        if len(self.deck) >= 4:
            self.player_hand = [self.deck.pop(), self.deck.pop()]
            self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        else:
            self.reset_deck()
            self.deal_initial_cards()

    def hand_value(self, hand) -> int:
        score = 0
        aces = 0
        for card in hand:
            rank = card[:-1]
            if rank in ['J', 'Q', 'K']:
                score += 10
            elif rank == 'A':
                aces += 1
                score += 11
            else:
                score += int(rank)
        while score > 21 and aces:
            score -= 10
            aces -= 1
        return score

    def hit(self): #dobranie karty przez garcza

         if not self.player_standing and self.result == "":
            if len(self.deck) > 0:
                self.player_hand.append(self.deck.pop())
                if self.hand_value(self.player_hand) > 21:
                    self.result = "Dealer wins."

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
lootbox_spin_sound = Sound("../Audio/case_spin2.wav")
lootbox_spin_sound.s.set_volume(0.5)
button_click_sound = Sound('../Audio/rozdanie_karty.mp3')
button_click_sound.s.set_volume(0.5)
lootbox_opened_sound = Sound("../Audio/case_opened3.wav")
lootbox_opened_sound.s.set_volume(1)


# przyciski

play_button = Button(main_screen,636,300,200, 60,"Play", (40,40,40),(32,32,32), button_click_sound)

gamble_button = Button(main_screen, 636, 400, 200, 60, "$ Gamble $", (255,215,0), (255,190,0), button_click_sound)

quit_button = Button(main_screen, 636, 700, 200, 60, "Quit", (40,40,40), (32,32,32), button_click_sound)

back_to_menu = Button(main_screen,1100, 650, 200, 60, "Back", (40,40,40),(32,32,32), button_click_sound)

options_button = Button(main_screen,  636,500, 200, 60, "Options", (40,40,40), (32,32,32), button_click_sound)

instruction_button = Button(main_screen, 636, 600, 200, 60, "Instruction", (40,40,40), (32,32,32), button_click_sound)

fullscreen_button_info = Button(main_screen,300, 300, 200, 60, "Fullscreen", (40,40,40), (40,40,40))

fullscreen_button= Button(main_screen, 600, 300, 200, 60, "", (40,40,40), (32,32,32), button_click_sound)

hit_button = Button(main_screen, 636,400,200, 60,"Hit", (40,40,40),(32,32,32), button_click_sound)

stand_button = Button(main_screen, 636,500,200, 60,"Stand", (40,40,40),(32,32,32), button_click_sound)

deal_button = Button(main_screen, 636,700,200, 60,"Deal", (40,40,40),(32,32,32), button_click_sound)

open_case_button = Button(main_screen, 636, 750, 200, 60,"Otwórz paczke", (255, 190, 0), (255, 190, 0), button_click_sound)

buttons = [play_button, gamble_button, quit_button, back_to_menu, options_button, fullscreen_button_info, fullscreen_button, hit_button, stand_button, deal_button, instruction_button, open_case_button]



# wczytanie pliku tekstowego z instrukcja
instructions_text = load_instructions()

# Zmienne Gry
music_manager = MusicManager()
image_manager = ImageManager('../Graphics')
game_logic = Game_Logic()


# wczytanie obrazow
main_menu_background=image_manager.load("menu_background.jpg")
logo=image_manager.load("logo.jpg")
table=image_manager.load("stol.jpg")
case_background = image_manager.load("case_background.jpg")
instruction_background = image_manager.load("instruction_background.jpg")

# backgrounds
main_menu_background=toggle_fullscreen(fullscreen,main_menu_background,"menu_background.jpg")
table=toggle_fullscreen(fullscreen,table,"stol.jpg")
case_background = toggle_fullscreen(fullscreen,case_background, "case_background.jpg")
instruction_background = toggle_fullscreen(fullscreen, instruction_background, "instruction_background.jpg")
# glosnosc glownej muzyki
pygame.mixer.music.set_volume(0.5)

# ustawienie logo
pygame.display.set_icon(logo)

state = "MENU" # stan gry
running = True # czy gra dziala

clock = pygame.time.Clock()
FPS = 60
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
            if instruction_button.handle_event(event):
                state = "INSTRUCTION"
            if quit_button.handle_event(event):
                running = False
        if state == "GAMBLE":
            if back_to_menu.handle_event(event):
                state = "MENU"
                current_lootbox = None
                lootbox_active = False
            if open_case_button.handle_event(event):
                current_lootbox.open()
                lootbox_active = True
                current_lootbox.animation_time = pygame.time.get_ticks()


        if state == "INSTRUCTION":
            if back_to_menu.handle_event(event):
                state="MENU"
        if state == "GAME":                                     # wszystkie zdarzenia w game
            if back_to_menu.handle_event(event):
                state = "MENU"
            if hit_button.handle_event(event):
                game_logic.hit()
            if stand_button.handle_event(event):
                game_logic.stand()
            if deal_button.handle_event(event):
                game_logic.reset()
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
                instruction_background = toggle_fullscreen(fullscreen, instruction_background, "instruction_background.jpg")



    if state == "MENU":                                      #zarzadzanie muzyka i rysowaniem obiektow
        if music_manager.state != "MENU":
            music_manager.play_menu()

        back_to_menu.active = False
        play_button.active = True
        gamble_button.active = True
        options_button.active = True
        quit_button.active = True
        fullscreen_button.active = False
        fullscreen_button_info.active = False
        instruction_button.active = True

        main_screen.blit(main_menu_background, (0, 0))

        play_button.draw(main_screen)
        options_button.draw(main_screen)
        gamble_button.draw(main_screen)
        quit_button.draw(main_screen)
        instruction_button.draw(main_screen)

    if state == "GAME":
        if state == "GAME":
            play_button.active = False
            gamble_button.active = False
            options_button.active = False
            quit_button.active = False
            fullscreen_button.active = False
            fullscreen_button_info.active = False
            instruction_button.active = False
            hit_button.active = len(game_logic.player_hand) > 0 and not game_logic.player_standing and game_logic.result == ""
            stand_button.active = len(game_logic.player_hand) > 0 and not game_logic.player_standing and game_logic.result == ""
            deal_button.active = True
            back_to_menu.active = True

            if music_manager.state != "GAME":
                music_manager.play_game()

            main_screen.blit(table, (0, 0))

            back_to_menu.draw(main_screen)
            hit_button.draw(main_screen)
            stand_button.draw(main_screen)
            deal_button.draw(main_screen)

            # Wyświetl karty
            card_font = pygame.font.SysFont("Arial", 48)
            result_font = pygame.font.SysFont("Arial", 36)

            # Karty gracza
            y_offset = 100
            x = 200
            main_screen.blit(card_font.render("Player:", True, (255, 255, 255)), (x, y_offset))
            for i, card in enumerate(game_logic.player_hand):
                suit = card[-1]
                color = (255, 0, 0) if suit in '♥♦' else (0, 0, 0)
                card_text = card_font.render(card, True, color)
                main_screen.blit(card_text, (x + i * 60, y_offset + 50))

            # Karty krupiera
            y_offset = 250
            main_screen.blit(card_font.render("Dealer:", True, (255, 255, 255)), (x, y_offset))
            for i, card in enumerate(game_logic.dealer_hand):
                if i == 0 or game_logic.result:
                    display_card = card
                    suit = card[-1]
                    color = (255, 0, 0) if suit in '♥♦' else (0, 0, 0)
                else:
                    display_card = "??"
                    color = (255, 255, 255)
                card_text = card_font.render(display_card, True, color)
                main_screen.blit(card_text, (x + i * 60, y_offset + 50))

            # Wynik
            if game_logic.result:
                result_text = result_font.render(f"Result: {game_logic.result}", True, (255, 215, 0))
                main_screen.blit(result_text, (x, 500))
    if state == "OPTIONS":
        play_button.active = False
        gamble_button.active = False
        options_button.active = False
        quit_button.active = False
        fullscreen_button.active = True
        fullscreen_button_info.active = True
        back_to_menu.active = True
        instruction_button.active = False

        fullscreen_button.text = "Yes" if fullscreen else "No"

        main_screen.blit(main_menu_background, (0,0))

        fullscreen_button.draw(main_screen)
        fullscreen_button_info.draw(main_screen)
        back_to_menu.draw(main_screen)

    if state == "INSTRUCTION" :
        play_button.active = False
        gamble_button.active = False
        options_button.active = False
        quit_button.active = False
        fullscreen_button.active = True
        fullscreen_button_info.active = True
        back_to_menu.active = True

        main_screen.blit(instruction_background, (0, 0))
        back_to_menu.draw(main_screen)

        #obliczam dostepne miejsce w oknie instrukcja
        screen_width , screen_height = main_screen.get_size()
        margin_x = 50
        margin_y = 50
        available_screen_w = screen_width - 2 * margin_x
        available_screen_h = screen_height - 2 * margin_y

        #funkcja dostosowywuja rozklad i rozmiar tekstu do okna
        line_count = len(instructions_text)
        max_font = 28
        min_font = 14

        font_size = max_font
        found = False

        while font_size >= min_font and found is False:

            font = pygame.font.SysFont (None,font_size)
            line_height = font_size + 6
            max_lines_in_col = available_screen_h // line_height
            col_count = (line_count + max_lines_in_col - 1)// max_lines_in_col

            if col_count * (font.size("M")[0] * 40) < available_screen_w:
                found = True
            else:
                font_size -=1

        if not found:

            font_size = min_font
            font = pygame.font.SysFont (None, font_size)
            line_height = font_size + 6
            max_lines_in_col = available_screen_h // line_height
            col_count = (line_count + max_lines_in_col -1) // max_lines_in_col

        column_width = available_screen_w // col_count

        for i, line in enumerate (instructions_text):
            col = i // max_lines_in_col
            row = i % max_lines_in_col
            x = margin_x + col * column_width
            y = margin_y + row * line_height

            text_surface=font.render(line.strip(), True, (255, 255, 255))
            main_screen.blit(text_surface, (x, y))


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
                jackpot_sound = jackpot_sound.s,
                case_opened = lootbox_opened_sound.s

            )
            current_lootbox.animation_time = pygame.time.get_ticks()

        #rysowanko
        if current_lootbox:
            current_lootbox.update()
            current_lootbox.draw(main_screen)
            #przycisk Otwórz kszynke kiedy lootbox sienie kreci
            '''
            open_case_button = Button(
                main_screen, main_screen.get_width()//2 -100, 750 ,200,60,
                "Otwórz paczke", (255, 190, 0), (255, 190, 0), button_click_sound
            )
            '''
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
            if pygame.time.get_ticks() - current_lootbox.animation_time > 2000:  # 5 sekund
                lootbox_active = False
                current_lootbox = None


    pygame.display.flip() #odswiezenie ekranu
    clock.tick(FPS)
pygame.quit() #wyjscie z gry