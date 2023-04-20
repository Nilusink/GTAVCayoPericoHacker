"""
main.py
19. April 2023

implements keyboard movement

Author:
Nilusink
"""
from cayo_hacks.elevator_hack import Matcher
from cayo_hacks.image_detection import *
from time import sleep
import keyboard as kb


# for colors to work
import os
os.system('color')


def main():
    """
    main program loop
    """
    # dramatic startup sequence
    print(f"{CLR_BLUE}::{CLR_RESET} Initiating hack ..", end="", flush=True)

    # create instances
    finger_matcher = Matcher(keyboard_delay=.01)

    print(f"\r{CLR_BLUE}::{CLR_RESET} Initiating hack {CLR_GREEN}done{CLR_RESET}", end="")
    sleep(.2)

    print(f"""
{CLR_BLUE}::{CLR_RESET}
{CLR_BLUE}::{CLR_RED}{STL_BOLD}\tControls{CLR_RESET}
{CLR_BLUE}::{CLR_RESET}\t  • {CLR_GREEN}CTRL{CLR_RESET} + {CLR_GREEN}R{CLR_RESET}  ->  Start Hack
{CLR_BLUE}::{CLR_RESET}\t  • {CLR_GREEN}CTRL{CLR_RESET} + {CLR_GREEN}T{CLR_RESET}  ->  Stop Program
{CLR_BLUE}::{CLR_RESET}
""")

    # actual program
    while True:
        if kb.is_pressed("ctrl"):
            if kb.is_pressed("t"):
                exit(0)
        
            elif kb.is_pressed("r"):
                # elevator fingerprint hack
                if finger_matcher.debug:
                    print("proc")
    
                finger_matcher.start_procedure()

            elif kb.is_pressed("e"):
                # wall safe number hack
                ...

        sleep(.01)


if __name__ == "__main__":
    main()
