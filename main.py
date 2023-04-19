"""
main.py
19. April 2023

<description>

Author:
Nilusinkc
"""
from finger_detection import Matcher
from time import sleep
# import keyboard as kb


m = Matcher()

ACTIVATION_KEYBIND: str = "ctrl+e"
KEYBOARD_DELAY: float = .1


# def keyboard_move_ticks(ticks: int, delay: float = KEYBOARD_DELAY) -> None:
#     """
#     move n ticks with the keyboard (left - right arrow keys)
#     """
#     for _ in range(ticks):
#         kb.press("d")
#         sleep(.1)
#         kb.release("d")
#
#         sleep(delay)
#
#     for _ in range(-ticks):
#         kb.press("a")
#         sleep(.1)
#         kb.release("a")
#         sleep(delay)


def make_procedure():
    """
    take a screenshot and find all offsets, then move the cursor with the arrow keys
    """
    # m.make_screenshot()
    offsets = m.get_all_off()

    # for offset in offsets:
    #     keyboard_move_ticks(offset)
    #     kb.press_and_release("s")
    #     sleep(KEYBOARD_DELAY * 2)


def main():
    while True:
        # if kb.is_pressed("ctrl"):
        #     if kb.is_pressed("t"):
        #         exit(0)
        #
        #     elif kb.is_pressed("r"):
        #         print("proc")
        make_procedure()
        exit(0)

        sleep(.05)

#        make_procedure()


if __name__ == "__main__":
    main()
