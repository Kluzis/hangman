import random
from termcolor import colored

def choose_word():
    words = ["python", "hangman", "developer", "artificial", "intelligence", "challenge", "education", "keyboard"]
    return random.choice(words)

def display_word(word, guessed_letters):
    return " ".join([letter if letter in guessed_letters else "_" for letter in word])

def hangman():
    word = choose_word()
    guessed_letters = set()
    attempts = 6

    print("Welcome to Hangman!")

    while attempts > 0:
        print("\n" + display_word(word, guessed_letters))
        guess = input("Guess a letter: ").lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Invalid input. Please enter a single letter.")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter.")
            continue

        guessed_letters.add(guess)

        if guess not in word:
            attempts -= 1
            print(f"Wrong guess! You have {attempts} attempts left.")

        if set(word).issubset(guessed_letters):
            print(colored(f"Congratulations! You guessed the word: {word}", "red"))
            break
    else:
        print(colored(f"Game over! The word was: {word}", "red"))

if __name__ == "__main__":
    hangman()

