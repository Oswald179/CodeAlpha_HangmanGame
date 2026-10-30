"""
TASK 1: Hangman Game (GUI) — CodeAlpha Python Internship
Intern: Nyamedor Oswald Ayiku | ID: CA/DF1/322006
"""

import random
import time
import tkinter as tk
from tkinter import font as tkfont

try:
    import winsound
    HAS_SOUND = True
except ImportError:
    HAS_SOUND = False

WORDS = ["planet", "rocket", "galaxy", "meteor", "cosmos"]
MAX_WRONG = 6

# ── Palette ──
BG        = "#0a0e14"
PANEL     = "#11161d"
PANEL2    = "#1a2029"
ACCENT    = "#58a6ff"
GREEN     = "#3fb950"
RED       = "#f85149"
YELLOW    = "#e3b341"
TEXT      = "#e6edf3"
DIM       = "#30363d"
WHITE     = "#ffffff"
SUIT      = "#c9d1d9"
HELMET    = "#58a6ff"


def beep(freq=400, dur=120):
    if HAS_SOUND:
        try:
            winsound.Beep(freq, dur)
        except Exception:
            pass


class HangmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman — Space Rescue")
        self.root.configure(bg=BG)
        self.root.geometry("1000x720")
        self.root.minsize(1000, 680)

        self.f_title = tkfont.Font(family="Consolas", size=22, weight="bold")
        self.f_word  = tkfont.Font(family="Consolas", size=30, weight="bold")
        self.f_btn   = tkfont.Font(family="Consolas", size=14, weight="bold")
        self.f_stat  = tkfont.Font(family="Consolas", size=12)

        self.streak = 0
        self.best = 0
        self.round_start = time.time()
        self.shake_job = None
        self.stars = [(random.randint(20, 440), random.randint(20, 460))
                      for _ in range(60)]

        self._build_ui()
        self.new_game()

    # ── UI ──
    def _build_ui(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", pady=(14, 0))
        tk.Label(header, text="🚀  HANGMAN — SPACE RESCUE",
                 font=self.f_title, fg=ACCENT, bg=BG).pack()
        tk.Label(header,
                 text="Save the astronaut. Guess the word.  6 wrong = lost in space.",
                 font=("Consolas", 11), fg=DIM, bg=BG).pack(pady=(2, 0))

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=20, pady=10)

        # LEFT — canvas
        left = tk.Frame(body, bg=PANEL, highlightbackground="#21262d",
                        highlightthickness=1)
        left.pack(side="left", fill="both", padx=(0, 12))

        self.canvas = tk.Canvas(left, width=460, height=480,
                                bg=PANEL, highlightthickness=0)
        self.canvas.pack(padx=12, pady=12)

        # RIGHT — word, hearts, keyboard
        right = tk.Frame(body, bg=BG)
        right.pack_propagate(True)  
        right.pack(side="left", fill="both", expand=True)

        self.word_label = tk.Label(right, text="", font=self.f_word,
                                   fg=WHITE, bg=BG)
        self.word_label.pack(pady=(6, 4))

        self.hearts_label = tk.Label(right, text="", font=("Consolas", 24),
                                     fg=RED, bg=BG)
        self.hearts_label.pack(pady=(0, 6))

        self.status_label = tk.Label(right, text="", font=self.f_stat,
                                     fg=TEXT, bg=BG)
        self.status_label.pack(pady=(0, 12))

        kb = tk.Frame(right, bg=BG)
        kb.pack(pady=4)
        self.letter_buttons = {}
        for row in ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]:
            rf = tk.Frame(kb, bg=BG)
            rf.pack(pady=3)
            for letter in row:
                b = tk.Button(
                    rf, text=letter, width=3, height=1, font=self.f_btn,
                    bg=PANEL2, fg=TEXT, bd=0, relief="flat",
                    activebackground=ACCENT, activeforeground=WHITE,
                    command=lambda l=letter.lower(): self.guess(l),
                )
                b.pack(side="left", padx=2)
                b.bind("<Enter>", lambda e, btn=b: self._hover(btn, True))
                b.bind("<Leave>", lambda e, btn=b: self._hover(btn, False))
                self.letter_buttons[letter.lower()] = b

        footer = tk.Frame(self.root, bg=BG)
        footer.pack(fill="x", padx=20, pady=(0, 14))
        self.stats_label = tk.Label(footer, text="", font=self.f_stat,
                                    fg=DIM, bg=BG)
        self.stats_label.pack(side="left")
        tk.Button(footer, text="🔄  New Game", font=self.f_btn,
                  bg=ACCENT, fg=WHITE, bd=0, relief="flat",
                  activebackground="#1f6feb", activeforeground=WHITE,
                  padx=16, pady=6, command=self.new_game).pack(side="right")


    def _hover(self, btn, on):
        if btn["state"] == "normal":
            btn.config(bg="#30363d" if on else PANEL2)
            


    # ── State ──
    def new_game(self):
        self.word = random.choice(WORDS)
        self.guessed = set()
        self.wrong = 0
        self.finished = False
        self.round_start = time.time()
        for b in self.letter_buttons.values():
            b.config(state="normal", bg=PANEL2, fg=TEXT)
        self.status_label.config(text="Click a letter to begin!", fg=TEXT)
        self.update_display()

    def guess(self, letter):
        if self.finished or letter in self.guessed:
            return
        self.guessed.add(letter)
        btn = self.letter_buttons[letter]
        btn.config(state="disabled")

        if letter in self.word:
            btn.config(bg=GREEN, fg=WHITE)
            self.status_label.config(
                text=f"✅  '{letter.upper()}' is in the word!", fg=GREEN)
            beep(880, 90)
        else:
            self.wrong += 1
            btn.config(bg=RED, fg=WHITE)
            self.status_label.config(
                text=f"❌  '{letter.upper()}' is not there. "
                     f"{MAX_WRONG - self.wrong} lives left.", fg=RED)
            beep(220, 150)
            self._shake()

        self.update_display()
        if all(c in self.guessed for c in self.word):
            self.finish(True)
        elif self.wrong >= MAX_WRONG:
            self.finish(False)

    def _shake(self):
        if self.shake_job:
            self.root.after_cancel(self.shake_job)
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        offsets = [(-6, 0), (6, 0), (-4, 2), (4, -2), (0, 0)]
        def step(i=0):
            if i < len(offsets):
                dx, dy = offsets[i]
                self.root.geometry(f"+{x+dx}+{y+dy}")
                self.shake_job = self.root.after(30, step, i + 1)
        step()

    def finish(self, win):
        self.finished = True
        for b in self.letter_buttons.values():
            b.config(state="disabled")
        elapsed = time.time() - self.round_start

        if win:
            self.streak += 1
            self.best = max(self.best, self.streak)
            self.status_label.config(
                text=f"🚀  MISSION SUCCESS! '{self.word.upper()}'  "
                     f"({elapsed:.1f}s)", fg=GREEN)
            beep(660, 90); self.root.after(120, lambda: beep(880, 90))
            self.root.after(240, lambda: beep(1100, 160))
            self._confetti()
            self._rocket_launch()
        else:
            self.streak = 0
            self.status_label.config(
                text=f"💀  LOST IN SPACE. The word was '{self.word.upper()}'",
                fg=RED)
            beep(180, 300)
        self.update_stats()

    # ── Render ──
    def update_display(self):
        self.word_label.config(text="  ".join(
            c.upper() if c in self.guessed else "_" for c in self.word))
        remaining = MAX_WRONG - self.wrong
        self.hearts_label.config(text="❤ " * remaining + "♡ " * self.wrong)
        self.draw_scene()
        self.update_stats()

    def update_stats(self):
        self.stats_label.config(
            text=f"Streak: {self.streak}   |   Best: {self.best}   |   "
                 f"Wrong: {self.wrong}/{MAX_WRONG}")

    def draw_scene(self):
        c = self.canvas
        c.delete("all")
        # Starfield + moon
        for x, y in self.stars:
            c.create_oval(x, y, x+1.5, y+1.5, fill="#3b4252", outline="")
        c.create_oval(370, 30, 410, 70, fill="#c9d1d9", outline="")
        c.create_oval(378, 32, 400, 52, fill=PANEL, outline="")

        # Gallows
        c.create_line(40, 440, 200, 440, fill=TEXT, width=4)
        c.create_line(90, 440, 90, 60, fill=TEXT, width=5)
        c.create_line(90, 60, 300, 60, fill=TEXT, width=5)
        c.create_line(300, 60, 300, 110, fill=TEXT, width=3)
        c.create_line(90, 440, 50, 440, fill=TEXT, width=3)

        if self.wrong == 0:
            # Safe astronaut standing by
            self._draw_astronaut(260, 260, dead=False)
            return

        # Helmet + head
        if self.wrong >= 1:
            c.create_oval(265, 115, 335, 185, outline=HELMET, width=3)
            c.create_oval(280, 130, 320, 170, outline=ACCENT, width=1)
            if self.wrong >= MAX_WRONG:
                for x1, y1, x2, y2 in [(292, 140, 302, 150), (302, 140, 292, 150),
                                       (308, 140, 318, 150), (318, 140, 308, 150)]:
                    c.create_line(x1, y1, x2, y2, fill=RED, width=2)
                c.create_arc(292, 152, 308, 168, start=0, extent=180,
                             style="arc", outline=RED, width=2)
            else:
                c.create_oval(292, 142, 300, 150, fill=ACCENT)
                c.create_oval(310, 142, 318, 150, fill=ACCENT)
                c.create_line(295, 160, 305, 160, fill=ACCENT, width=2)

        # Suit body
        if self.wrong >= 2:
            c.create_rectangle(268, 185, 332, 300, fill=SUIT,
                               outline=ACCENT, width=2)
            c.create_rectangle(290, 200, 310, 240, fill=PANEL2,
                               outline=DIM, width=1)

        # Arms
        if self.wrong >= 3:
            c.create_line(268, 210, 220, 250, fill=SUIT, width=8)
            c.create_line(220, 250, 210, 260, fill=ACCENT, width=8)
        if self.wrong >= 4:
            c.create_line(332, 210, 380, 250, fill=SUIT, width=8)
            c.create_line(380, 250, 390, 260, fill=ACCENT, width=8)

        # Legs
        if self.wrong >= 5:
            c.create_line(285, 300, 260, 370, fill=SUIT, width=9)
            c.create_line(260, 370, 255, 385, fill=ACCENT, width=9)
        if self.wrong >= 6:
            c.create_line(315, 300, 340, 370, fill=SUIT, width=9)
            c.create_line(340, 370, 345, 385, fill=ACCENT, width=9)

    def _draw_astronaut(self, cx, cy, dead=False):
        c = self.canvas
        c.create_oval(cx-35, cy-70, cx+35, cy, outline=HELMET, width=3)
        c.create_oval(cx-25, cy-60, cx+25, cy-10, outline=ACCENT, width=1)
        c.create_oval(cx-14, cy-45, cx-6, cy-37, fill=ACCENT)
        c.create_oval(cx+6, cy-45, cx+14, cy-37, fill=ACCENT)
        c.create_arc(cx-14, cy-30, cx+14, cy-10, start=200, extent=140,
                     style="arc", outline=ACCENT, width=2)
        c.create_rectangle(cx-30, cy+5, cx+30, cy+80, fill=SUIT,
                           outline=ACCENT, width=2)
        c.create_rectangle(cx-12, cy+20, cx+12, cy+55, fill=PANEL2,
                           outline=DIM)

    def _confetti(self):
        colors = [ACCENT, GREEN, YELLOW, RED, WHITE, "#d2a8ff"]
        pieces = []
        for _ in range(80):
            x = random.randint(20, 440)
            y = random.randint(-40, 20)
            oid = self.canvas.create_oval(x, y, x+5, y+5,
                                          fill=random.choice(colors),
                                          outline="")
            pieces.append([oid, random.uniform(2, 6)])
        def fall():
            alive = False
            for p in pieces:
                self.canvas.move(p[0], 0, p[1])
                pos = self.canvas.coords(p[0])
                if pos and pos[3] < 480:
                    alive = True
            if alive:
                self.canvas.after(30, fall)
        fall()

    def _rocket_launch(self):
        c = self.canvas
        r = c.create_text(80, 400, text="🚀", font=("Consolas", 34))
        def up():
            c.move(r, 1, -6)
            pos = c.coords(r)
            if pos and pos[1] > 20:
                c.after(40, up)
        up()


def main():
    root = tk.Tk()
    HangmanGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()