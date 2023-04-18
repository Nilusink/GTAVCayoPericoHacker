"""
_matcher.py
19. April 2023

Main attraction - tells you how many clicks off the hack is

Author:
Nilusink
"""
from .image_tools import *
from ._constants import *
import pyautogui as pag
import numpy as np


class Matcher:
    _current_screenshot: np.ndarray = None

    def __init__(self):
        # load image (instead of screenshot)
        self._current_screenshot = cv2.imread('cayo2.png')

    def find_n_off(self, n_fingerprint: int) -> tuple[int, float]:
        """
        tells you how many clicks off one specific image is

        :param n_fingerprint: the nth fingerprint in the row
        :return: n clicks off, certainty
        """
        n_finger_image = get_fingerprint_image(
            self._current_screenshot,
            False,
            n_fingerprint
        )

        match_percentages: list[float] = [0] * N_FINGERPRINTS
        for n_position in range(N_FINGERPRINTS):
            curr_img = get_fingerprint_image(
                self._current_screenshot,
                True,
                n_position
            )

            match_percentages[n_position] = match_images(
                n_finger_image,
                curr_img
            )

        max_match = max(match_percentages)
        actual_n_finger = match_percentages.index(max_match)

        return actual_n_finger - n_fingerprint, max_match

    def get_all_off(self) -> list[int]:
        """
        get all offsets
        """
        out: list[int] = []
        print("offsets: ")

        for i_finger in range(N_FINGERPRINTS):
            ticks, certainty = self.find_n_off(i_finger)

            # # show a visualization of the matching
            n_matched = i_finger + ticks
            tmp_img = self._current_screenshot.copy()
            draw_fingerprint_rectangle(tmp_img, False, i_finger)
            draw_fingerprint_rectangle(tmp_img, True, n_matched)
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
        screenshot = pag.screenshot()
        screenshot.save("cayo2.png")
        self._current_screenshot = np.array(screenshot)
