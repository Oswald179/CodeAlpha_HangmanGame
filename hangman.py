"""
TASK 1: Hangman Game — CodeAlpha Python Internship
Intern: Nyamedor Oswald Ayiku | ID: CA/DF1/322006

Default     : python hangman.py            → console version (spec-compliant)
Graphical   : python hangman.py --gui      → tkinter window (bonus demo)
"""

import sys

if __name__ == "__main__":
    if "--gui" in sys.argv:
        try:
            from hangman_gui import main as gui_main
            gui_main()
        except ImportError:
            print("tkinter is not available. Install python3-tk.")
            sys.exit(1)
    else:
        from hangman_console import main as console_main
        console_main()