"""
_constants.py
18. April 2023

Fingerprint positions on screen

Author:
Nilusink
"""
from pyautogui import size


# variable constants
SCREEN_SIZE: tuple[int, int] = size()

LEFT_SIZE: tuple[int, int] = (
    int(.2135416 * SCREEN_SIZE[0]),
    int(.0509259 * SCREEN_SIZE[1])
)
RIGHT_SIZE: tuple[int, int] = (
    int(.21614583 * SCREEN_SIZE[0]),
    int(.022916 * SCREEN_SIZE[1])
)

LEFT_ORIGIN: tuple[int, int] = (
    int(.2135416 * SCREEN_SIZE[0]),
    int(.33333 * SCREEN_SIZE[1])
)
RIGHT_ORIGIN: tuple[int, int] = (
    int(.53385416 * SCREEN_SIZE[0]),
    int(.356481 * SCREEN_SIZE[1])
)

LEFT_Y_OFF: float = .07037037 * SCREEN_SIZE[1]
RIGHT_Y_OFF: float = .0712037037 * SCREEN_SIZE[1]


# constants
N_FINGERPRINTS: int = 8

CLR_RESET="\033[1;0m"
STL_BOLD="\033[1;1m"
CLR_RED="\033[0;31m"
CLR_GREEN="\033[0;32m"
CLR_BLUE="\033[0;34m"