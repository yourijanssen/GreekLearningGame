# main.py

from player_stats import load_player_stats, save_player_stats
import time
from game.letters import play_letters
from game.combinations import play_combinations
from game.words import play_words
from game.sentences import play_sentences
from game.numbers import play_numbers
from game.fill_blanks import play_fill_blanks
from game.stats import show_stats

def main_menu(stats):
    while True:
        print("\n==== Greek Learning Game Menu ====")
        print("1. Letters")
        print("2. Combinations")
        print("3. Words")
        print("4. Sentences")
        print("5. Numbers")
        print("6. Fill-in-the-Blank")
        print("7. Show my stats")
        print("0. Quit")
        choice = input("\nYour choice: ").strip()
        print()
        if choice == "1":
            play_letters(stats)
        elif choice == "2":
            play_combinations(stats)
        elif choice == "3":
            play_words(stats)
        elif choice == "4":
            play_sentences(stats)
        elif choice == "5":
            play_numbers(stats)
        elif choice == "6":
            play_fill_blanks(stats)
        elif choice == "7":
            show_stats(stats)
        elif choice == "0":
            print("Goodbye and happy learning!")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    stats = load_player_stats()
    game_start_time = time.time()
    main_menu(stats)
    stats["playtime_seconds"] = stats.get("playtime_seconds", 0) + int(time.time() - game_start_time)
    save_player_stats(stats)