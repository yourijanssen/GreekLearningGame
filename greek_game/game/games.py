# games.py

from greek_game.game.utility import *
from data import *
from player_stats import update_mode_stats

def play_letters():
    print("Type 'm' to return to the main menu.\n")
    items = list(greek_letters)
    random.shuffle(items)
    streak, correct_count, best_streak = 0, 0, 0
    quit_early = False

    # Start timing!
    start_time = time.time()

    while items:
        letter, name = items[0]
        ans = input(f"Type this Greek letter: {strip_greek_accents(letter)} ({name}): ")
        if ans == 'm':
            print(f"Your final streak was {streak}!\n")
            quit_early = True
            break
        elif strip_greek_accents(ans) == strip_greek_accents(letter):
            streak += 1
            correct_count += 1
            best_streak = max(best_streak, streak)
            if ans == letter:
                print(green(f"✅ Correct! (with accents) Streak: {streak}  | Progress: {correct_count}/{len(greek_letters)}"))
            else:
                print(yellow(f"✅ Correct (without accents)! The proper spelling is: {letter}"))
                print(yellow(f"Current streak: {streak} | Progress: {correct_count}/{len(greek_letters)}\n"))
            congrats_streak(streak)
            items.pop(0)
        else:
            print(red(f"❌ Incorrect. The correct letter was: {letter} ({name})."))
            print(red(f"Your streak was: {streak}"))
            streak = 0
            random.shuffle(items)
    else:
        # Only runs if loop is not exited early (all items completed)
        total_time = time.time() - start_time  # in seconds
        minutes = int(total_time // 60)
        seconds = total_time % 60
        print(green("🎉 Congratulations! You typed all Greek letters correctly in this round! 🎉\n"))
        print(yellow(f"⏱️ You completed {len(greek_letters)} letters in {minutes} min {seconds:.2f} sec."))

        # Store/check/update record in stats!
        # Prepare key for time records
        if "fastest_times" not in stats:
            stats["fastest_times"] = {}
        prev_best = stats["fastest_times"].get("letters")

        # If first run or new record, update and celebrate
        if (prev_best is None) or (total_time < prev_best):
            stats["fastest_times"]["letters"] = total_time
            print(green("\n🎊 NEW RECORD! You set your fastest letters time! 🎊"))
            print(yellow(f" 🏁 New record: {minutes} min {seconds:.2f} sec\n"))
        else:
            # Show all-time best as well
            pmin = int(prev_best // 60)
            psec = prev_best % 60
            print(cyan(f"Your best all-time is {pmin} min {psec:.2f} sec."))

    update_mode_stats(stats, "letters", correct_count, best_streak)


def play_words():
    print("Type 'm' to return to the main menu.\n")
    items = list(greek_words)
    random.shuffle(items)
    streak = 0
    correct_count = 0
    best_streak = 0
    quit_early = False  # Track manual exit

    while items:
        word, meaning = items[0]
        ans = input(f"Type this Greek word: {strip_greek_accents(word)} (means: {meaning}): ")
        if ans == 'm':
            print(f"Your final streak was {streak}!\n")
            quit_early = True
            break
        elif strip_greek_accents(ans) == strip_greek_accents(word):
            streak += 1
            correct_count += 1
            best_streak = max(best_streak, streak)
            if ans == word:
                print(green(f"✅ Correct! (with proper accents) Streak: {streak}  | Progress: {correct_count}/{len(greek_words)}"))
            else:
                print(yellow(f"✅ Correct (without accents)! The proper spelling is: {word}"))
                print(yellow(f"Current streak: {streak} | Progress: {correct_count}/{len(greek_words)}\n"))
            congrats_streak(streak)
            items.pop(0)
        else:
            print(red(f"❌ Incorrect. The correct word was: {word}."))
            print(red(f"Your streak was: {streak}"))
            streak = 0
            random.shuffle(items)
    else:
        print(green("🎉 Congratulations! You typed all Greek words correctly in this round! 🎉\n"))

    update_mode_stats(stats, "words", correct_count, best_streak)

def play_sentences():
    print("Type 'm' to return to the main menu.\n")
    print("Choose mode:")
    print("1) Type the Greek for the given English meaning 🎯")
    print("2) Type the English for the given Greek sentence 🚀")
    print("3) Copy the Greek sentence to practice typing (copy mode) ✍️")
    mode = input("Your choice (1, 2 or 3): ").strip()
    items = list(greek_sentences)
    random.shuffle(items)
    streak = correct_count = best_streak = 0

    while items:
        sentence, translation = items[0]

        if mode == '1':  # English to Greek
            print(f"\nEnglish meaning: {yellow(translation)}")
            ans = input("Type the Greek sentence (no accents required):\n> ")
            if ans == 'm':
                print(f"Your final streak was {streak}!\n")
                break
            if strip_greek_accents(ans) == strip_greek_accents(sentence):
                streak += 1
                correct_count += 1
                best_streak = max(best_streak, streak)
                if ans == sentence:
                    print(green("✅ Correct! (with accents)"))
                else:
                    print(yellow(f"✅ Correct (no accents). Full sentence with accents is:\n  {sentence}"))
                print(yellow(f"Streak: {streak} | Progress: {correct_count}/{len(greek_sentences)}"))
                congrats_streak(streak)
                items.pop(0)
            else:
                print(red(f"❌ Incorrect. Correct Greek sentence was:\n  {sentence}"))
                print(yellow(f"English meaning: {translation}"))
                print(red(f"Your streak was: {streak}\n"))
                streak = 0
                random.shuffle(items)

        elif mode == '2':  # Greek to English
            print(f"\nGreek sentence: {yellow(sentence)}")
            print(f"English meaning: {yellow(translation)}")  # Always show, as requested
            ans = input("Type the English translation:\n> ")
            if ans == 'm':
                print(f"Your final streak was {streak}!\n")
                break
            if ans.strip().lower() == translation.strip().lower():
                streak += 1
                correct_count += 1
                best_streak = max(best_streak, streak)
                print(green("✅ Correct!"))
                print(yellow(f"Streak: {streak} | Progress: {correct_count}/{len(greek_sentences)}"))
                congrats_streak(streak)
                items.pop(0)
            else:
                print(red(f"❌ Incorrect. The correct English was:\n  {translation}"))
                print(red(f"Your streak was: {streak}\n"))
                streak = 0
                random.shuffle(items)

        elif mode == '3':  # Copy/Typing practice
            print(f"\nPractice typing this Greek sentence:")
            print(f"{yellow(sentence)}")
            print(f"English meaning: {yellow(translation)}")
            ans = input("Type the Greek sentence (no accents required):\n> ")
            if ans == 'm':
                print(f"Your final streak was {streak}!\n")
                break
            if strip_greek_accents(ans) == strip_greek_accents(sentence):
                streak += 1
                correct_count += 1
                best_streak = max(best_streak, streak)
                if ans == sentence:
                    print(green("✅ Correct! (with accents)"))
                else:
                    print(yellow(f"✅ Correct (no accents). Proper spelling is:\n  {sentence}"))
                print(yellow(f"Streak: {streak} | Progress: {correct_count}/{len(greek_sentences)}"))
                congrats_streak(streak)
                items.pop(0)
            else:
                print(red(f"❌ Incorrect. Correct Greek sentence was:\n  {sentence}"))
                print(yellow(f"English meaning: {translation}"))
                print(red(f"Your streak was: {streak}\n"))
                streak = 0
                random.shuffle(items)

        else:
            print(red("Invalid mode choice. Please restart this section.\n"))
            break
    else:
        print(green("🎉 Congratulations! You completed all Greek sentences this round! 🎉\n"))
    update_mode_stats(stats, "sentences", correct_count, best_streak)

def play_combinations():
    print("Type 'm' to return to the main menu.\n")
    items = list(greek_combinations)
    random.shuffle(items)
    streak, correct_count, best_streak = 0, 0, 0
    quit_early = False

    while items:
        combo, sound = items[0]
        ans = input(f"Type this Greek combination: {strip_greek_accents(combo)} (pronounced: {sound}): ")
        if ans == 'm':
            print(f"Your final streak was {streak}!\n")
            quit_early = True
            break
        elif strip_greek_accents(ans) == strip_greek_accents(combo):
            streak += 1
            correct_count += 1
            best_streak = max(best_streak, streak)
            if ans == combo:
                print(green(f"✅ Correct! (with accents) Streak: {streak} | Progress: {correct_count}/{len(greek_combinations)}"))
            else:
                print(yellow(f"✅ Correct (without accents)! The proper spelling is: {combo}"))
                print(yellow(f"Current streak: {streak} | Progress: {correct_count}/{len(greek_combinations)}\n"))
            congrats_streak(streak)
            items.pop(0)
        else:
            print(red(f"❌ Incorrect. The correct combination was: {combo}"))
            print(red(f"Your streak was: {streak}"))
            streak = 0
            random.shuffle(items)
    else:
        print(green("🎉 Congratulations! You typed all Greek combinations correctly in this round! 🎉\n"))
    update_mode_stats(stats, "combinations", correct_count, best_streak)

def play_numbers():
    print("Type 'm' to return to the main menu.\n")
    print("Choose practice range:")
    print("1) Numbers 1-10")
    print("2) Numbers 1-100")
    choice = input("Your choice (1 or 2): ").strip()
    if choice == '1':
        number_range = set(str(i) for i in range(1, 11))
        items = [x for x in greek_numbers if x[0] in number_range]
    elif choice == '2':
        items = list(greek_numbers)
    else:
        print(red("Invalid selection. Returning to menu.\n"))
        return

    random.shuffle(items)
    streak, correct_count, best_streak = 0, 0, 0
    quit_early = False
    total = len(items)   # <<< Store the starting total for progress display

    while items:
        number, greek = items[0]
        if random.choice([True, False]):
            ans = input(f"How do you write {yellow(number)} in Greek? ")
            if ans == 'm':
                print(f"Your final streak was {streak}!\n")
                quit_early = True
                break
            elif strip_greek_accents(ans) == strip_greek_accents(greek):
                streak += 1
                correct_count += 1
                best_streak = max(best_streak, streak)
                if ans == greek:
                    print(green(f"✅ Correct! (with accents) {number} is '{greek}'. Streak: {streak}"))
                else:
                    print(yellow(f"✅ Correct (without accents)! The proper spelling is: '{greek}'"))
                print(yellow(f"Current streak: {streak} | Progress: {correct_count}/{total}\n"))
                congrats_streak(streak)
                items.pop(0)
            else:
                print(red(f"❌ Incorrect. {number} in Greek is: '{greek}'"))
                print(red(f"Your streak was: {streak}"))
                streak = 0
                random.shuffle(items)
        else:
            ans = input(f"Which number is '{yellow(strip_greek_accents(greek))}'? ")
            if ans == 'm':
                print(f"Your final streak was {streak}!\n")
                quit_early = True
                break
            elif ans == number:
                streak += 1
                correct_count += 1
                best_streak = max(best_streak, streak)
                print(green(f"✅ Correct! '{greek}' is {number}"))
                print(yellow(f"Current streak: {streak} | Progress: {correct_count}/{total}\n"))
                congrats_streak(streak)
                items.pop(0)
            else:
                print(red(f"❌ Incorrect. '{greek}' is: {number}"))
                print(red(f"Your streak was: {streak}"))
                streak = 0
                random.shuffle(items)
    else:
        print(green("🎉 Congratulations! You typed all selected Greek numbers correctly in this round! 🎉\n"))
    update_mode_stats(stats, "numbers", correct_count, best_streak)

def play_fill_blanks():
    print("Type 'm' to return to the main menu.\n")
    items = list(greek_fill_blanks)
    random.shuffle(items)
    streak, correct_count, best_streak = 0, 0, 0
    quit_early = False

    while items:
        sentence, correct, hint = items[0]
        ans = input(f"Fill in the blank: {sentence}\nHint: {hint}\n> ")
        if ans == 'm':
            print(f"Your final streak was {streak}!\n")
            quit_early = True
            break
        elif strip_greek_accents(ans) == strip_greek_accents(correct):
            streak += 1
            correct_count += 1
            best_streak = max(best_streak, streak)
            if ans == correct:
                print(green("✅ Correct!"))
            else:
                print(yellow(f"✅ Correct (without accents)! The proper spelling is: {correct}"))
            print(yellow(f"Current streak: {streak} | Progress: {correct_count}/{len(greek_fill_blanks)}\n"))
            congrats_streak(streak)
            items.pop(0)
        else:
            print(red(f"❌ Incorrect. The correct answer is: {correct}"))
            print(red(f"Your streak was: {streak}"))
            streak = 0
            random.shuffle(items)
    else:
        print(green("🎉 Congratulations! You solved all fill-in-the-blank questions!\n"))
    update_mode_stats(stats, "fill_blanks", correct_count, best_streak)
