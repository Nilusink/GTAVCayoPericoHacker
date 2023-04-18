"""
image_tools.py
18. April 2023

tools for slicing / getting one specific image

Author:
Nilusink
"""
from ._constants import *
import numpy as np
import cv2


def get_fingerprint_image(
        screenshot: np.ndarray,
        left_right: bool,
        n_fingerprint: int
) -> np.ndarray:
    """
    get the image of a fingerprint on screen

    :param screenshot: input image
    :param left_right: false: left, true: right
    :param n_fingerprint: starting with 0, the nth fingerprint
    :return: cv2 image
    """
    if left_right:
        finger = screenshot[
                 RIGHT_ORIGIN[1] + int(n_fingerprint * RIGHT_Y_OFF)
                 :RIGHT_ORIGIN[1] + RIGHT_SIZE[1]
                 + int(n_fingerprint * RIGHT_Y_OFF),
                 RIGHT_ORIGIN[0]:RIGHT_ORIGIN[0] + RIGHT_SIZE[0]
        ]

        # return finger
        return cv2.resize(finger, LEFT_SIZE)

    else:
        return screenshot[
                      LEFT_ORIGIN[1] + int(n_fingerprint * LEFT_Y_OFF)
                      :LEFT_ORIGIN[1] + LEFT_SIZE[1]
                      + int(n_fingerprint * LEFT_Y_OFF), LEFT_ORIGIN[0]
                      :LEFT_ORIGIN[0] + LEFT_SIZE[0]
        ]


def draw_fingerprint_rectangle(
        screenshot: np.ndarray,
        left_right: bool,
        n_fingerprint: int
) -> None:
    """
    draw a rectangle around the selected fingerprint

    :param screenshot: input image
    :param left_right: false: left, true: right
    :param n_fingerprint: starting with 0, the nth fingerprint
    """
    if left_right:
        cv2.rectangle(
            screenshot,
            (
                RIGHT_ORIGIN[0],
                RIGHT_ORIGIN[1] + int(n_fingerprint * RIGHT_Y_OFF)
            ),
            (
                RIGHT_ORIGIN[0] + RIGHT_SIZE[0],
                RIGHT_ORIGIN[1] + RIGHT_SIZE[1] + int(n_fingerprint * RIGHT_Y_OFF)
            ),
            (0, 0, 255), 2
        )

    else:
        cv2.rectangle(
            screenshot,
            (
                LEFT_ORIGIN[0],
                LEFT_ORIGIN[1] + int(n_fingerprint * LEFT_Y_OFF)
            ),
            (
                LEFT_ORIGIN[0] + LEFT_SIZE[0],
                LEFT_ORIGIN[1] + LEFT_SIZE[1] + int(n_fingerprint * LEFT_Y_OFF)
            ),
            (0, 0, 255), 2
        )


def match_images(
        image1: np.ndarray,
        image2: np.ndarray
) -> float:
    """
    match two similar sized images

    :return: similarity between 0 and 1
    """
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Apply template matching
    result = cv2.matchTemplate(gray1, gray2, cv2.TM_CCOEFF_NORMED)

    # Get the similarity percentage
    return abs(np.max(result))


def match_images2(
        image1: np.ndarray,
        image2: np.ndarray
) -> float:
    """
    match two similar sized images

    :return: similarity between 0 and 1
    """
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Create a feature detector and descriptor extractor
    detector = cv2.ORB_create()

    # Detect keypoints and descriptors for both images
    keypoints1, descriptors1 = detector.detectAndCompute(gray1, None)
    keypoints2, descriptors2 = detector.detectAndCompute(gray2, None)

    # Create a brute-force matcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match the keypoints and descriptors of the two images
    matches = bf.match(descriptors1, descriptors2)

    if len(keypoints1) > 0 and len(keypoints2) > 0:
        # Calculate the similarity score based on the number and quality of the matched keypoints
        return len(matches) / max(len(keypoints1), len(keypoints2))

    return 0
