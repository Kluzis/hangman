import random #náhodný výběr slova
import pygame #hnihovna
import sys #pro ukočení programu

# Inicializace Pygame ABY SE MOHLO POUŽÍVAT (př.kreslení)
pygame.init()

# Nastavení barev RGB formátu
WHITE, BLACK, RED, GREEN = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0)

# Velikost okna
WIDTH, HEIGHT = 900, 700 #pixelů
window = pygame.display.set_mode((WIDTH, HEIGHT)) #hlavní okno
pygame.display.set_caption("Hangman Game") #název okna

# Nastavení fontů
font = pygame.font.SysFont("Arial", 40) #hlavní font por zobrazení textu
small_font = pygame.font.SysFont("Arial", 30)

## Výběr slova ze seznamu
def choose_word():
    words = ["python", "hangman", "developer", "artificial", "intelligence", "challenge", "education", "keyboard"]
    return random.choice(words)

## Zobrazení slova s hádanými písmeny
def display_word(word, guessed_letters): # zobrazí slova s podtržítky pro neuhádnutá písmena a odhalená pro uhádnutá
                                         # př. slovo python uhodnutá písmena {"p", "y"} --> výstup "p y _ _ _ _"
    display = " ".join([letter if letter in guessed_letters else "_" for letter in word])
    return display 

#  Zobrazení oběšence podle počtu zbývajících pokusů (attempts)
def draw_hangman(attempts): #každá část oběšence se kreslí pokud klesne počet pokusů
    # Hlava
    if attempts <= 5:
        pygame.draw.circle(window, BLACK, (150, 250), 30, 5)  # hlava
    # Tělo
    if attempts <= 4:
        pygame.draw.line(window, BLACK, (150, 280), (150, 350), 5)  # tělo
    # Ruka - levá
    if attempts <= 3:
        pygame.draw.line(window, BLACK, (150, 300), (100, 325), 5)  # L ruka
    # Ruka - pravá
    if attempts <= 2:
        pygame.draw.line(window, BLACK, (150, 300), (200, 325), 5)  # P ruka
    # Nohy - levá
    if attempts <= 1:
        pygame.draw.line(window, BLACK, (150, 350), (100, 400), 5)  # L noha
    # Nohy - pravá
    if attempts <= 0:
        pygame.draw.line(window, BLACK, (150, 350), (200, 400), 5)  # P noha

    # Kladka (oběšný rám)
    if attempts <= 5:
        pygame.draw.line(window, BLACK, (75, 150), (75, 450), 5)  # vertikální sloup
        pygame.draw.line(window, BLACK, (75, 150), (150, 150), 5)  # vodorovná tyč
        pygame.draw.line(window, BLACK, (150, 150), (150, 200), 5)  # závěs pro hlavu

# Hlavní třída pro hru
class HangmanGame:
    def __init__(self):
        self.word = choose_word() # Výběr tajného slova
        self.guessed_letters = set() # Množina uhodnutých písmen
        self.attempts = 6 # Počet zbývajících pokusů
        self.game_over = False # Stav hry (true = hra skončila)
        self.win = False # Výsledek hry (true = pokud hráč vyhraje)

    def handle_guess(self, guess): #zpracuje hádané písmeno a aktualizuje stav hry
        if len(guess) == 1 and guess.isalpha():
            if guess in self.guessed_letters:
                return
            self.guessed_letters.add(guess)
            if guess not in self.word:
                self.attempts -= 1
            self.check_game_status()

    def check_game_status(self): #kotrola hráč prohra/výhra
        if set(self.word).issubset(self.guessed_letters):
            self.win = True
            self.game_over = True
        elif self.attempts == 0:
            self.game_over = True

# Hlavní herní smyčka
def main(): #zpracovává události (stisk klávesy, zavření okna). aktuální stav hry (slovo, počet pokusů, oběšenec). Kontrola hry, skončila, výsledek
    game = HangmanGame()

    while True:
        window.fill(WHITE) # Barva okna
        
        # Zpracování událostí (přerušení hry, zadání písmen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and not game.game_over:
                guess = pygame.key.name(event.key).lower()
                if len(guess) == 1 and guess.isalpha():
                    game.handle_guess(guess)

        # Zobrazení aktuálního stavu hry
        word_display = display_word(game.word, game.guessed_letters)
        word_text = font.render(word_display, True, BLACK)
        window.blit(word_text, (WIDTH // 2 - word_text.get_width() // 2, 100))

        # Zobrazení pokusů a oběšence
        attempts_text = small_font.render(f"Attempts left: {game.attempts}", True, BLACK)
        window.blit(attempts_text, (WIDTH // 2 - attempts_text.get_width() // 2, 200))

        # Oběšenec vykreslený vlevo
        draw_hangman(game.attempts)

        # Pokud hra skončila (výhra/prohra)
        if game.game_over:
            if game.win:
                result_text = font.render("You Win!", True, GREEN)
            else:
                result_text = font.render(f"Game Over! The word was: {game.word}", True, RED)
            window.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2))

        # Aktualizace obrazovky
        pygame.display.update()

##
if __name__ == "_main_": #hra se spustí, když je skript spuštěn přímo (ne když je importován jako modul).
    main()