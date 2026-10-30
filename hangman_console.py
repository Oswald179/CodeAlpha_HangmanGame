"""
TASK 1: Hangman Game (Console) — CodeAlpha Python Internship
Intern: Nyamedor Oswald Ayiku | ID: CA/DF1/322006
"""

import random
import os

WORDS = ["planet", "rocket", "galaxy", "meteor", "cosmos"]
MAX_WRONG = 6


class C:
    RESET = "\033[0m"; BOLD = "\033[1m"; DIM = "\033[2m"
    RED = "\033[91m"; GREEN = "\033[92m"; YELLOW = "\033[93m"
    CYAN = "\033[96m"; WHITE = "\033[97m"


def enable_ansi():
    if os.name == "nt":
        os.system("")


def clear():
    os.system("cls" if os.name == "nt" else "clear")


GALLOWS = [
    r"""
        ╔══════════════════════════════════════╗
        ║              ☀  ☾  ✦                 ║
        ║           🚀  (safe & sound)          ║
        ║          /|\                         ║
        ║          / \                         ║
        ╚══════════════════════════════════════╝""",
    r"""
        ╔══════════════════════════════════════╗
        ║              ☀  ☾  ✦                 ║
        ║           🚀  (oxygen low)            ║
        ║          /|\                         ║
        ║          / \                         ║
        ╚══════════════════════════════════════╝""",
    r"""
        ╔══════════════════════════════════════╗
        ║              ☀  ☾  ✦                 ║
        ║           🚀  (hull crack!)           ║
        ║          /|                          ║
        ║          /                           ║
        ╚══════════════════════════════════════╝""",
    r"""
        ╔══════════════════════════════════════╗
        ║              ☀  ☾  ✦                 ║
        ║           🚀  (engine fire)           ║
        ║          /                           ║
        ║                                      ║
        ╚══════════════════════════════════════╝""",
    r"""
        ╔══════════════════════════════════════╗
        ║              ☀  ☾  ✦                 ║
        ║           🚀  (drifting...)           ║
        ║                                      ║
        ║                                      ║
        ╚══════════════════════════════════════╝""",
    r"""
        ╔══════════════════════════════════════╗
        ║              ☀  ☾  ✦                 ║
        ║           💥  (explosion!)            ║
        ║                                      ║
        ║                                      ║
        ╚══════════════════════════════════════╝""",
    r"""
        ╔══════════════════════════════════════╗
        ║              ☀  ☾  ✦                 ║
        ║           ☠  (lost in space)          ║
        ║                                      ║
        ║                                      ║
        ╚══════════════════════════════════════╝""",
]


def render_hearts(wrong):
    return f"{C.RED}{'❤ ' * (MAX_WRONG - wrong)}{C.DIM}{'♡ ' * wrong}{C.RESET}"


def render_word(word, guessed):
    return "  ".join(
        f"{C.GREEN}{C.BOLD}{c.upper()}{C.RESET}" if c in guessed
        else f"{C.DIM}_{C.RESET}" for c in word)


def render_keyboard(guessed, word):
    """Render QWERTY keyboard. Guaranteed to contain all 26 letters."""
    rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
    # Sanity check — ensure all 26 letters exist exactly once
    all_letters = "".join(rows)
    assert len(all_letters) == 26, f"Keyboard has {len(all_letters)} letters"
    assert set(all_letters) == set("ABCDEFGHIJKLMNOPQRSTUVWXYZ"), \
        "Keyboard is missing letters!"

    out = []
    for row in rows:
        line = []
        for letter in row:
            low = letter.lower()
            if low in guessed:
                if low in word:
                    line.append(f"{C.GREEN}{C.BOLD}{letter}{C.RESET}")
                else:
                    line.append(f"{C.RED}{C.DIM}{letter}{C.RESET}")
            else:
                line.append(f"{C.WHITE}{letter}{C.RESET}")
        out.append("  " + " ".join(line))
    return "\n".join(out)


def render_screen(word, guessed, wrong, message=""):
    clear()
    print(f"\n{C.CYAN}{C.BOLD}   🚀  HANGMAN — SPACE RESCUE   {C.RESET}\n")
    print(GALLOWS[min(wrong, MAX_WRONG)])
    print(f"\n  {C.YELLOW}LIVES:{C.RESET}  {render_hearts(wrong)}")
    print(f"  {C.YELLOW}WORD :{C.RESET}  {render_word(word, guessed)}\n")
    print(f"  {C.CYAN}KEYBOARD:{C.RESET}")
    print(render_keyboard(guessed, word))
    print()
    if message:
        print(f"  {message}")
    print()


def play_round():
    word = random.choice(WORDS)
    guessed, wrong = [], 0
    message = f"{C.CYAN}Guess a letter to save the astronaut!{C.RESET}"

    while wrong < MAX_WRONG:
        render_screen(word, guessed, wrong, message)
        if all(c in guessed for c in word):
            render_screen(word, guessed, wrong,
                          f"{C.GREEN}{C.BOLD}🚀 MISSION SUCCESS!{C.RESET}")
            return True

        guess = input(f"  {C.YELLOW}➤ Guess a letter:{C.RESET} ").lower().strip()

        if not guess:
            message = f"{C.RED}⚠  No input.{C.RESET}"; continue
        if len(guess) != 1:
            message = f"{C.RED}⚠  Exactly ONE letter.{C.RESET}"; continue
        if not guess.isalpha():
            message = f"{C.RED}⚠  Letters only.{C.RESET}"; continue
        if guess in guessed:
            message = f"{C.YELLOW}⚠  Already tried '{guess.upper()}'.{C.RESET}"; continue

        guessed.append(guess)
        if guess in word:
            message = f"{C.GREEN}✅ '{guess.upper()}' is in the word!{C.RESET}"
        else:
            wrong += 1
            message = (f"{C.RED}❌ '{guess.upper()}' is not there. "
                       f"{MAX_WRONG - wrong} lives left.{C.RESET}")

    render_screen(word, guessed, wrong,
                  f"{C.RED}{C.BOLD}💀 LOST IN SPACE...{C.RESET}")
    print(f"  {C.RED}The word was:{C.RESET} {C.BOLD}{word.upper()}{C.RESET}\n")
    return False


def main():
    enable_ansi()
    streak = best = rounds = 0
    while True:
        won = play_round()
        rounds += 1
        streak = streak + 1 if won else 0
        best = max(best, streak)
        print(f"  {C.CYAN}Streak:{C.RESET} {streak}  "
              f"{C.CYAN}Best:{C.RESET} {best}  "
              f"{C.CYAN}Rounds:{C.RESET} {rounds}\n")
        again = input(f"  {C.YELLOW}Play again? (y/n):{C.RESET} ").lower().strip()
        if again != "y":
            clear()
            print(f"\n{C.CYAN}Thanks for playing, astronaut!{C.RESET}")
            print(f"{C.DIM}Rounds: {rounds} | Best streak: {best}{C.RESET}\n")
            break


if __name__ == "__main__":
    main()