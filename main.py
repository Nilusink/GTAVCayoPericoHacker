"""
main.py
19. April 2023

implements keyboard movement

Author:
Nilusinkc
"""
from finger_detection import Matcher
from time import sleep
import keyboard as kb


# settings
KEYBOARD_DELAY: float = .01


# global matcher instance
m = Matcher()


def keyboard_move_ticks(ticks: int, delay: float = KEYBOARD_DELAY) -> None:
    """
    move n ticks with the keyboard (left - right arrow keys)
    """
    for _ in range(-ticks):
        kb.press("d")
        sleep(KEYBOARD_DELAY)
        kb.release("d")

        sleep(delay)

    for _ in range(ticks):
        kb.press("a")
        sleep(KEYBOARD_DELAY)
        kb.release("a")
        sleep(delay)


def make_procedure():
    """
    take a screenshot and find all offsets, then move the cursor with the arrow keys
    """
    m.make_screenshot()
    offsets = m.get_all_off()
    print(f"{offsets=}")
    for offset in offsets:
        keyboard_move_ticks(offset)
        kb.press_and_release("s")
        sleep(KEYBOARD_DELAY)


def main():
    while True:
        if kb.is_pressed("ctrl"):
            if kb.is_pressed("t"):
                exit(0)
        
            elif kb.is_pressed("r"):
                print("proc")
                make_procedure()

        sleep(.01)


if __name__ == "__main__":
    main()
