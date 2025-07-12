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
