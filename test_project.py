import json
import pytest

from project import (
    load_words,
    choose_word,
    mask_word,
    is_valid_guess,
    calculate_score,
    save_score,
)


def test_load_words(tmp_path):
    sample = {"animals": ["cat", "dog"]}
    filepath = tmp_path / "words.json"
    filepath.write_text(json.dumps(sample))

    result = load_words(str(filepath))
    assert result == sample

    with pytest.raises(FileNotFoundError):
        load_words(str(tmp_path / "missing.json"))


def test_choose_word():
    words_by_category = {"animals": ["cat", "dog"], "colors": ["red"]}

    category, word = choose_word(words_by_category, "colors")
    assert category == "colors"
    assert word == "red"

    category, word = choose_word(words_by_category, "animals")
    assert word in ["cat", "dog"]

    with pytest.raises(ValueError):
        choose_word(words_by_category, "unknown_category")


def test_mask_word():
    assert mask_word("cat", set()) == "_ _ _"
    assert mask_word("cat", {"c", "t"}) == "c _ t"
    assert mask_word("cat", {"c", "a", "t"}) == "c a t"


def test_is_valid_guess():
    assert is_valid_guess("a", set()) is True
    assert is_valid_guess("a", {"a"}) is False
    assert is_valid_guess("1", set()) is False
    assert is_valid_guess("ab", set()) is False


def test_calculate_score():
    assert calculate_score("cat", 0, False) == 30
    assert calculate_score("cat", 2, False) == 20
    assert calculate_score("cat", 0, True) == 15
    assert calculate_score("cat", 10, True) == 0


def test_save_score(tmp_path):
    filepath = tmp_path / "leaderboard.json"

    leaderboard = save_score("Alice", 50, str(filepath))
    assert leaderboard == [{"name": "Alice", "score": 50}]

    leaderboard = save_score("Bob", 80, str(filepath))
    assert leaderboard[0] == {"name": "Bob", "score": 80}
    assert leaderboard[1] == {"name": "Alice", "score": 50}
