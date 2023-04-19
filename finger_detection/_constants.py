"""
_constants.py
18. April 2023

Fingerprint positions on screen

Author:
Nilusink
"""
LEFT_SIZE: tuple[int, int] = (410, 55)
RIGHT_SIZE: tuple[int, int] = (415, 44)

LEFT_ORIGIN: tuple[int, int] = (410, 360)
RIGHT_ORIGIN: tuple[int, int] = (1025, 363 + RIGHT_SIZE[1] // 2)

SCREEN_SIZE: tuple[int, int] = (1920, 1080)

LEFT_Y_OFF: float = 76
RIGHT_Y_OFF: float = 76.9

N_FINGERPRINTS: int = 8
