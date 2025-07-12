
import sys

def color(text, code):
    return f"\033[{code}m{text}\033[0m" if sys.stdout.isatty() else text

def green(text):    return color(text, '92')
def red(text):      return color(text, '91')
def yellow(text):   return color(text, '93')
def blue(text):     return color(text, '94')
def magenta(text):  return color(text, '95')
def cyan(text):     return color(text, '96')
def bold(text):     return color(text, '1')

def congrats_streak(streak):
    if streak >= 20: 
        print(bold(green(f"🌟 WOW! {streak} answers in a row! You're a legend! 🌟\n")))
    elif streak >= 10: 
        print(yellow(f"🔥 {streak} correct in a row! Keep going! 🔥\n"))
    elif streak >= 5: 
        print(blue(f"👏 {streak} correct answers streak! 👏\n"))