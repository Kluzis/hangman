from flask import Flask, render_template, request, session
import random
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
app.secret_key = "hangman_secret"

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

# Load words and sentences
def load_text(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return ["default phrase"]

# Load word lists
words = load_text("words.txt")
sentences = load_text("sentences.txt")

# Function to start a new game
def start_new_game(mode):
    text_list = words if mode == "word" else sentences
    chosen_text = random.choice(text_list).lower()
    session["text"] = chosen_text
    session["guessed_letters"] = []
    session["attempts"] = 6
    session["hint_used"] = False  # Track if hint was used
    session["success"] = {"vowels": set(), "consonants": set()}
    session["failures"] = {"vowels": set(), "consonants": set()}
    return chosen_text

# Function to get a hint
def get_hint(text, guessed_letters):
    remaining_letters = [char for char in text if char.isalpha() and char not in guessed_letters]
    return random.choice(remaining_letters) if remaining_letters else None

# Function to generate the success/failure plot
def generate_plot():
    labels = ["Success Vowels", "Success Consonants", "Fail Vowels", "Fail Consonants"]
    values = [len(session["success"]["vowels"]), len(session["success"]["consonants"]),
              len(session["failures"]["vowels"]), len(session["failures"]["consonants"])]

    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color=["green", "lightgreen", "red", "lightcoral"])
    plt.xlabel("Category")
    plt.ylabel("Count")
    plt.title("Hangman Success & Failure Analysis")

    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url

@app.route("/", methods=["GET", "POST"])
def index():
    if "mode" not in session:  # ✅ If no mode selected, go to start page
        return render_template("start.html")

    # ✅ Ensure all session variables exist
    session.setdefault("hint_used", False)
    session.setdefault("success", {"vowels": [], "consonants": []})
    session.setdefault("failures", {"vowels": [], "consonants": []})

    text = session["text"]
    guessed_letters = session["guessed_letters"]
    attempts = session["attempts"]
    hint_used = session["hint_used"]

    message = ""  # ✅ Message to show results of the guess

    if request.method == "POST":
        guess = request.form.get("letter")

        if guess:
            guess = guess.lower().strip()

            if guess == "hint":
                if not hint_used:
                    hint_letter = get_hint(text, guessed_letters)
                    if hint_letter:
                        guessed_letters.append(hint_letter)
                        session["hint_used"] = True
                        message = f"Hint used! The letter '{hint_letter}' is in the word."
                session.modified = True  # ✅ Ensure Flask recognizes the session update
            else:
                if len(guess) == 1 and guess.isalpha():
                    if guess not in guessed_letters:
                        guessed_letters.append(guess)
                        if guess not in text:
                            session["attempts"] -= 1  # ✅ Decrease attempts **before** updating the image
                            message = f"Wrong guess! '{guess}' is not in the phrase."
                            if guess in "aeiou":
                                session["failures"]["vowels"].append(guess)
                            else:
                                session["failures"]["consonants"].append(guess)
                        else:
                            message = f"Good guess! '{guess}' is in the phrase!"
                            if guess in "aeiou":
                                session["success"]["vowels"].append(guess)
                            else:
                                session["success"]["consonants"].append(guess)

                    session["guessed_letters"] = guessed_letters
                    session.modified = True  # ✅ Ensure the session updates immediately

    display_text_game = display_text(text, guessed_letters)
    game_over = "_" not in display_text_game or session["attempts"] == 0

    # ✅ Fix: Calculate the correct Hangman image **after attempts decrease**
    hangman_img = HANGMAN_PICS[min(6, 6 - session["attempts"])]  

    plot_url = generate_plot() if game_over else None

    return render_template("index.html", text=display_text_game, attempts=session["attempts"],
                           game_over=game_over, original_text=text,
                           hangman_img=hangman_img, hint_used=session["hint_used"],
                           plot_url=plot_url, message=message)


def start_new_game(mode):
    text_list = words if mode == "word" else sentences
    chosen_text = random.choice(text_list).lower()
    session["text"] = chosen_text
    session["guessed_letters"] = []
    session["attempts"] = 6
    session["hint_used"] = False  # Track if hint was used
    session["success"] = {"vowels": [], "consonants": []}  # ✅ Use lists instead of sets
    session["failures"] = {"vowels": [], "consonants": []}  # ✅ Use lists instead of sets
    return chosen_text

@app.route("/new_game", methods=["GET", "POST"])
def new_game():
    session.clear()  # ✅ Úplně smaže session, aby se znovu objevil výběr módu

    if request.method == "POST":  # ✅ Správně zpracuje POST request z tlačítek
        mode = request.form.get("mode")
        if mode in ["word", "sentence"]:  # ✅ Ověří, že mód je platný
            session["mode"] = mode
            start_new_game(mode)
            return index()  # ✅ Spustí hru s vybraným módem

    return render_template("start.html")  # ✅ Pokud něco selže, vrátí výběr módu


def display_text(text, guessed_letters):
    return " ".join([char if char in guessed_letters or char == " " else "_" for char in text])



if __name__ == "__main__":
    app.run(debug=True)
