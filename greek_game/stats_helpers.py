import time
import datetime
from ui_helpers import green, cyan, magenta, yellow, bold

def load_player_stats():
    import json, os
    if os.path.exists("player_stats.json"):
        with open("player_stats.json", "r", encoding="utf-8") as f:
            stats = json.load(f)
    else:
        stats = {
            "playtime_seconds": 0,
            "games_played": {},
            "correct_answers": {},
            "best_streak": {},
            "fastest_times": {},
            "last_played": None
        }
    return stats

def save_player_stats(stats):
    import json
    with open("player_stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

def update_mode_stats(stats, mode, count, streak):
    stats["games_played"][mode] = stats["games_played"].get(mode, 0) + 1
    stats["correct_answers"][mode] = stats["correct_answers"].get(mode, 0) + count
    stats["best_streak"][mode] = max(streak, stats["best_streak"].get(mode, 0))
    stats['last_played'] = int(time.time())

def show_stats(stats):
    def minutes_seconds(secs):
        mins = int(secs) // 60
        s = int(secs) % 60
        return f"{mins} min {s} sec"

    print(bold(magenta("\n🏆 === Your Greek Learning Stats === 🏆")))
    print(f"⏱️  Total play time: {yellow(minutes_seconds(stats.get('playtime_seconds',0)))}")

    games_played = stats.get('games_played', {})
    correct_answers = stats.get('correct_answers', {})
    best_streak = stats.get('best_streak', {})
    modes = set(games_played) | set(correct_answers) | set(best_streak)

    fastest = stats.get("fastest_times", {})
    if "letters" in fastest:
        mins = int(fastest["letters"] // 60)
        secs = fastest["letters"] % 60
        print(yellow(f"🏁 Fastest time for all letters: {mins} min {secs:.2f} sec"))

    if not modes:
        print(cyan("(No games played yet!)"))
    else:
        for mode in sorted(modes):
            print(bold(f"\n📚 {mode.capitalize()}"))
            print(f"   🎮 Games played:  {green(games_played.get(mode, 0))}")
            print(f"   ✅ Correct:       {cyan(correct_answers.get(mode, 0))}")
            print(f"   🔥 Best streak:   {yellow(best_streak.get(mode, 0))}")

    lp = stats.get('last_played', None)
    if lp:
        # Supports if it's epoch or already string
        if isinstance(lp, (int, float)):
            dt = datetime.datetime.fromtimestamp(lp)
        else:
            dt = lp
        print(f"\n⌛ Last played: {bold(str(dt))}")
    print(magenta("="*36)+"\n")