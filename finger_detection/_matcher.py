"""
_matcher.py
19. April 2023

Main attraction - tells you how many clicks off the hack is

Author:
Nilusink
"""
import cv2

from .image_tools import *
from ._constants import *
# import pyautogui as pag
import numpy as np


class Matcher:
    _current_screenshot: np.ndarray = None
    _current_screenshot_fingerprint_only: np.ndarray = None

    def __init__(self):
        # load image (instead of screenshot)
        self._current_screenshot = sharpen_image(cv2.imread('cayo3.png'))
        self._current_screenshot_fingerprint_only = \
            self._current_screenshot[0:-1, SCREEN_SIZE[0] // 2:-1]

    def find_n_off(self, n_fingerprint: int):  # -> tuple[int, float]:
        """
        tells you how many clicks off one specific image is

        :param n_fingerprint: the nth fingerprint in the row
        :return: n clicks off, certainty, position found
        """
        n_finger_image = get_fingerprint_image(
            self._current_screenshot,
            False,
            n_fingerprint
        )

        n_finger_image = cv2.resize(
            n_finger_image,
            (int(LEFT_SIZE[0] * 1.09), int(LEFT_SIZE[1] * 1.1))
        )

        n_finger_image = sharpen_image(n_finger_image)

        match, position = match_images(
            n_finger_image,
            self._current_screenshot_fingerprint_only
        )

        start = list(position[0])
        end = list(position[1])

        start[0] += SCREEN_SIZE[0] // 2
        end[0] += SCREEN_SIZE[0] // 2

        center_y = (end[1] - start[1]) / 2 + start[1]

        pos = round((center_y - RIGHT_ORIGIN[1]) / RIGHT_Y_OFF)

        off = pos - n_fingerprint

        return off, match, (start, end)

    def get_all_off(self) -> list[int]:
        """
        get all offsets
        """
        out: list[int] = []
        print("offsets: ")

        for i_finger in range(N_FINGERPRINTS):
            # ticks, certainty = self.find_n_off(i_finger)

            ticks, certainty, position = self.find_n_off(i_finger)

            # # show a visualization of the matching
            n_matched = i_finger + ticks
            tmp_img = self._current_screenshot.copy()
            draw_fingerprint_rectangle(tmp_img, False, i_finger)
            # draw_fingerprint_rectangle(tmp_img, True, n_matched)

            cv2.rectangle(tmp_img, position[0], position[1], (0, 0, 255))
            cv2.imshow("match: ", tmp_img)
            cv2.waitKey(0)

            out.append(ticks)
            print(f" {i_finger}: {out[-1]} ticks ({100 * certainty:.2f}% "
                  f"certain)")

        return out

    def make_screenshot(self) -> None:
        """
        make a new screenshot
        """
        # screenshot = pag.screenshot()
        # screenshot.save("cayo2.png")
        # self._current_screenshot = sharpen_image(np.array(screenshot))
        self._current_screenshot_fingerprint_only = \
            self._current_screenshot[0:-1, SCREEN_SIZE[0] // 2:-1]

