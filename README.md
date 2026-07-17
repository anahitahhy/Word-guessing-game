 Word Duel
 
Description:

Word Duel is a terminal-based word-guessing game inspired by classic Hangman.
Players choose a category — animals, countries, programming terms, or
movies — and try to guess a hidden word one letter at a time before running
out of attempts. An ASCII-art hangman drawing updates with each wrong guess,
giving instant visual feedback on how much room for error remains. Players
can also request a single hint per game at the cost of some points, adding a
small risk/reward decision to the gameplay.

At the end of each round, the game calculates a score based on word length,
number of wrong guesses, and whether a hint was used, then saves the result
to a local JSON-based leaderboard, keeping only the top 10 all-time scores.
This gives the game a light sense of progression and replayability, since
players can try to beat their own (or a friend's) previous high score.

## Files

- **`project.py`** — Contains `main()` and all core game logic:
  - `load_words()` reads the category/word data from `words.json`.
  - `choose_word()` picks a random word, either from a specific category or
    a random one, and validates that the requested category exists.
  - `mask_word()` builds the partially-revealed word display (e.g. `_ a _`)
    based on which letters have been guessed so far.
  - `is_valid_guess()` checks that a guess is a single, unused letter before
    it's accepted by the game loop.
  - `calculate_score()` computes the final score for a round.
  - `save_score()` reads, updates, sorts, and rewrites the JSON leaderboard.

- **`test_project.py`** — A `pytest` suite with one test function per
  non-`main` function above (`test_load_words`, `test_choose_word`,
  `test_mask_word`, `test_is_valid_guess`, `test_calculate_score`,
  `test_save_score`). File-based functions are tested using `pytest`'s
  `tmp_path` fixture so tests don't touch real project data.

- **`words.json`** — The word bank, organized by category, loaded at
  runtime rather than hard-coded, so new categories/words can be added
  without touching the game logic.

- **`requirements.txt`** — Lists `tabulate`, used to pretty-print the
  leaderboard as a formatted table at the end of each game.

## Design decisions

I chose to store words in an external JSON file instead of a Python
dictionary inside `project.py` so the word bank could grow (or be
localized/translated) without editing code — a pattern that mirrors how
real applications separate data from logic. Similarly, the leaderboard is
persisted to its own JSON file rather than kept only in memory, so scores
survive between runs, which felt important for a game that's meant to be
replayed.

I capped the leaderboard at the top 10 entries to keep the file small and
the printed table readable, rather than storing every game ever played.

## How to run

pip install -r requirements.txt
python project.py

## Running tests

pytest test_project.py
