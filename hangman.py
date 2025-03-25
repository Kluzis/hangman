import random
import matplotlib.pyplot as plt


# ASCII Hangman Stages
HANGMAN_PICS = [
    """
       ------
       |    |
            |
            |
            |
            |
    =========""",
    """
       ------
       |    |
       O    |
            |
            |
            |
    =========""",
    """
       ------
       |    |
       O    |
       |    |
            |
            |
    =========""",
    """
       ------
       |    |
       O    |
      /|    |
            |
            |
    =========""",
    """
       ------
       |    |
       O    |
      /|\   |
            |
            |
    =========""",
    """
       ------
       |    |
       O    |
      /|\   |
      /     |
            |
    =========""",
    """
       ------
       |    |
       O    |
      /|\   |
      / \   |
            |
    ========="""
]

# Game mode 
def choose_game_mode():
    while True:
        mode = input("\nChoose your game mode:\n1️⃣ Words (single words)\n2️⃣ Sentences (full sentences)\nEnter 1 or 2: ").strip()
        if mode in ["1", "2"]:
            return mode
        print("❌ Invalid input! Please enter '1' for Words or '2' for Sentences.")

# Load Function
def choose_text(mode):
    file_path = "C:\\ONEBOND\\skola\\words.txt" if mode == "1" else "C:\\ONEBOND\\skola\\sentences.txt"
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file.readlines()]
        return random.choice(lines) if lines else "default word"
    except FileNotFoundError:
        print(f"⚠️ File {file_path} not found! Using default list.")
        return "default sentence example" if mode == "2" else "defaultword"

# Function to display the word/sentence with guessed letters
def display_text(text, guessed_letters, mode):
    return " ".join([char if char in guessed_letters or char == " " else "_" for char in text])

# Function to get a hint
def get_hint(text, guessed_letters):
    remaining_letters = [char for char in text if char.isalpha() and char not in guessed_letters]
    return random.choice(remaining_letters) if remaining_letters else None

# Function to plot success and failure rates
def plot_success_rate(successful, unsuccessful, repeated):
    labels = ["Successful Consonants", "Successful Vowels", "Unsuccessful Consonants", "Unsuccessful Vowels", "Repeated Letters"]
    values = [len(successful["consonants"]), len(successful["vowels"]), len(unsuccessful["consonants"]), len(unsuccessful["vowels"]), len(repeated)]
    
    plt.figure(figsize=(8, 6))
    plt.bar(labels, values, color=["green", "lightgreen", "red", "lightcoral", "blue"])
    
    plt.xlabel("Category")
    plt.ylabel("Number of Letters")
    plt.title("Hangman Success & Failure Analysis")
    
    plt.show()

# Main Hangman game function
def hangman():
    mode = choose_game_mode()  # Ask if user wants words or sentences
    text = choose_text(mode).lower()  # Get word/sentence from file
    guessed_letters = set()
    successful_guesses = {"consonants": set(), "vowels": set()}
    unsuccessful_guesses = {"consonants": set(), "vowels": set()}
    repeated_guesses = set()
    attempts = 6
    hint_used = False
    vowels = {"a", "e", "i", "o", "u"}

    print("\n🎮 Welcome to Hangman! 🎮")
    print("Type 'hint' if you need a letter revealed (Only once!)")

    while attempts > 0:
        # Show ASCII Hangman before the guess
        print(HANGMAN_PICS[6 - attempts])
        print("\n" + display_text(text, guessed_letters, mode))  # Show current progress

        # Ask for input
        guess = input("\nGuess a letter (or type 'hint'): ").lower().strip()

        # Handle hint system
        if guess == "hint":
            if hint_used:
                print("⚠️ You've already used your hint!")
            else:
                hint_letter = get_hint(text, guessed_letters)
                if hint_letter:
                    guessed_letters.add(hint_letter)
                    print(f"💡 Hint used! The sentence contains the letter: **{hint_letter}**")
                    hint_used = True
            continue

        # Input validation
        if len(guess) != 1 or not guess.isalpha():
            print("❌ Invalid input. Please enter a **single letter**.")
            continue

        if guess in guessed_letters:
            print("⚠️ You already guessed that letter!")
            repeated_guesses.add(guess)  # Track repeated guesses
            continue

        # Add guessed letter
        guessed_letters.add(guess)

        # Check if guess is in the text
        if guess in text:
            if guess in vowels:
                successful_guesses["vowels"].add(guess)
            else:
                successful_guesses["consonants"].add(guess)
        else:
            attempts -= 1
            print(f"❌ Wrong guess! You have {attempts} attempts left.")
            if guess in vowels:
                unsuccessful_guesses["vowels"].add(guess)
            else:
                unsuccessful_guesses["consonants"].add(guess)

        # Check if player has won
        if set(text.replace(" ", "")).issubset(guessed_letters):  # Ignore spaces in check
            print(HANGMAN_PICS[6 - attempts])  # Show final Hangman state
            print(f"\n🎉 Congratulations! You guessed it: **{text}** 🎉")
            plot_success_rate(successful_guesses, unsuccessful_guesses, repeated_guesses)
            break
    else:
        print(HANGMAN_PICS[-1])  # Show full Hangman
        print(f"💀 Game Over! The correct answer was: **{text}**.")
        plot_success_rate(successful_guesses, unsuccessful_guesses, repeated_guesses)

# Run the game
if __name__ == "__main__":
    hangman()
