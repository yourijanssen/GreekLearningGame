# main.py

import time
from data import *
from utils import *
from player_stats import load_player_stats, save_player_stats
from games import (
    play_letters, play_words, play_numbers, play_combinations, play_sentences, play_fill_blanks
)

def print_menu_header(): ...
def show_stats(stats): ...

def main_menu(stats):
    while True:
        print_menu_header()
        # menu printing code, as before...
        choice = input().strip()
        if choice == "1":
            play_letters(stats)
        # ... etc as before
        elif choice == "0":
            print("Bye! Happy learning!")
            break

if __name__ == "__main__":
    stats = load_player_stats()
    game_start_time = time.time()
    main_menu(stats)
    stats["playtime_seconds"] += int(time.time() - game_start_time)
    save_player_stats(stats)