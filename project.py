import json
import random
import os
from tabulate import tabulate

MAX_WRONG_GUESSES = 6
WORDS_FILE = "words.json"
LEADERBOARD_FILE = "leaderboard.json"

HANGMAN_STAGES = [
    """
       -----
       |   |
       |
       |
       |
       |
    ---------
    """,
    """
       -----
       |   |
       |   O
       |
       |
       |
    ---------
    """,
    """
       -----
       |   |
       |   O
       |   |
       |
       |
    ---------
    """,
    """
       -----
       |   |
       |   O
       |  /|
       |
       |
    ---------
    """,
    """
       -----
       |   |
       |   O
       |  /|\\
       |
       |
    ---------
    """,
    """
       -----
       |   |
       |   O
       |  /|\\
       |  /
       |
    ---------
    """,
    """
       -----
       |   |
       |   O
       |  /|\\
       |  / \\
       |
    ---------
    """,
]


def main():
    print("=" * 40)
    print("       WELCOME TO WORD DUEL")
    print("=" * 40)

    words_by_category = load_words()
    player_name = input("Enter your name: ").strip() or "Anonymous"
    try:

        category_choice = input(
            f"Choose a category ({', '.join(words_by_category.keys())}) "
            f"or press Enter for random: "
        ).strip().lower()

        category, word = choose_word(
            words_by_category, category_choice if category_choice else None
        )
        print(f"\nCategory: {category.title()}")
    except ValueError:
        print("write name of category")

    guessed_letters = set()
    wrong_guesses = 0
    hint_used = False

    while wrong_guesses < MAX_WRONG_GUESSES:
        print(HANGMAN_STAGES[wrong_guesses])
        print("Word:", mask_word(word, guessed_letters))
        print(f"Wrong guesses remaining: {MAX_WRONG_GUESSES - wrong_guesses}")

        if "_" not in mask_word(word, guessed_letters):
            print(f"\nYou won! The word was '{word}'.")
            break

        guess = input("Guess a letter (or type 'hint'): ").strip().lower()

        if guess == "hint" and not hint_used:
            reveal = next(c for c in word.lower() if c not in guessed_letters)
            guessed_letters.add(reveal)
            hint_used = True
            print(f"Hint: the letter '{reveal}' is in the word.")
            continue

        if not is_valid_guess(guess, guessed_letters):
            print("Invalid guess. Enter a single, unused letter.")
            continue

        guessed_letters.add(guess)
        if guess not in word.lower():
            wrong_guesses += 1
            print("Wrong guess!")
    else:
        print(HANGMAN_STAGES[wrong_guesses])
        print(f"\nYou lost! The word was '{word}'.")

    score = calculate_score(word, wrong_guesses, hint_used)
    print(f"\nYour score: {score}")

    leaderboard = save_score(player_name, score)
    print("\nLeaderboard (Top 10):")
    print(tabulate(
        [(i + 1, entry["name"], entry["score"]) for i, entry in enumerate(leaderboard)],
        headers=["#", "Name", "Score"],
        tablefmt="simple",
    ))


def load_words(filepath=WORDS_FILE):
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Could not find word file: {filepath}")

    with open(filepath, "r", encoding="utf-8") as file:
        words_by_category = json.load(file)

    if not words_by_category:
        raise ValueError("Word file is empty.")

    return words_by_category


def choose_word(words_by_category, category=None):
    if category:
        if category not in words_by_category:
            raise ValueError(f"Unknown category: {category}")
        chosen_category = category
    else:
        chosen_category = random.choice(list(words_by_category.keys()))

    word = random.choice(words_by_category[chosen_category])
    return chosen_category, word.lower()


def mask_word(word, guessed_letters):
    
    return " ".join(
        letter if letter.lower() in guessed_letters else "_"
        for letter in word
    )


def is_valid_guess(guess, guessed_letters):
    
    return (
        len(guess) == 1
        and guess.isalpha()
        and guess.lower() not in guessed_letters
    )


def calculate_score(word, wrong_guesses, hint_used):
    score = len(word) * 10
    score -= wrong_guesses * 5
    if hint_used:
        score -= 15
    return max(score, 0)


def save_score(name, score, filepath=LEADERBOARD_FILE):

    leaderboard = []
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            try:
                leaderboard = json.load(file)
            except json.JSONDecodeError:
                leaderboard = []

    leaderboard.append({"name": name, "score": score})
    leaderboard = sorted(leaderboard, key=lambda entry: entry["score"], reverse=True)[:10]

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(leaderboard, file, indent=4)

    return leaderboard


if __name__ == "__main__":
    main()
