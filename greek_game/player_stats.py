import json
import os
import time

STATS_FILE = "player_stats.json"

DEFAULT_STATS = {
    "playtime_seconds": 0,
    "games_played": {
        "letters": 0,
        "combinations": 0,
        "words": 0,
        "sentences": 0,
        "numbers": 0,
        "fill_blanks": 0
    },
    "correct_answers": {
        "letters": 0,
        "combinations": 0,
        "words": 0,
        "sentences": 0,
        "numbers": 0,
        "fill_blanks": 0
    },
    "best_streak": {
        "letters": 0,
        "combinations": 0,
        "words": 0,
        "sentences": 0,
        "numbers": 0,
        "fill_blanks": 0
    },
    "last_played": None  # Timestamp
}

def load_player_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return DEFAULT_STATS.copy()

def save_player_stats(stats):
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

def update_mode_stats(stats, mode, correct, streak):
    stats["games_played"][mode] += 1
    stats["correct_answers"][mode] += correct
    if streak > stats["best_streak"][mode]:
        stats["best_streak"][mode] = streak
    stats["last_played"] = int(time.time())