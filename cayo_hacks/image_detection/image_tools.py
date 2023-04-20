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
        template: np.ndarray,
        large_image: np.ndarray
) -> tuple[float, tuple[tuple[int, int], tuple[int, int]]]:
    """
    match two similar sized images

    :return: similarity between 0 and 1, position (start xy, end xy)
    """
    gray1 = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(large_image, cv2.COLOR_BGR2GRAY)

    # Apply template matching
    result = cv2.matchTemplate(gray1, gray2, cv2.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Get the coordinates of the region in the input image
    # that matches the template image
    top_left = max_loc
    bottom_right = (
        top_left[0] + template.shape[1],
        top_left[1] + template.shape[0]
    )

    # Get the similarity percentage
    return abs(np.max(result)), (top_left, bottom_right)


def match_images2(
        template: np.ndarray,
        large_image: np.ndarray
) -> tuple[float, tuple[tuple[int, int], tuple[int, int]]]:
    """
    match two similar sized images

    :return: similarity between 0 and 1
    """
    gray1 = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(large_image, cv2.COLOR_BGR2GRAY)

    # Create a feature detector and descriptor extractor
    detector = cv2.ORB_create()

    # Detect keypoints and descriptors for both images
    keypoints1, descriptors1 = detector.detectAndCompute(gray1, None)
    keypoints2, descriptors2 = detector.detectAndCompute(gray2, None)

    # Create a brute-force matcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match the keypoints and descriptors of the two images
    matches = bf.match(descriptors1, descriptors2)

    matches = sorted(matches, key=lambda x: x.distance)

    # Extract the matched keypoints from the input and template images
    input_matched_kp = [keypoints1[match.queryIdx] for match in matches]
    template_matched_kp = [keypoints2[match.trainIdx] for match in matches]

    # Estimate an affine transformation that maps the template image onto the input image
    M, _ = cv2.estimateAffinePartial2D(
        srcPoints=[kp.pt for kp in template_matched_kp],
        dstPoints=[kp.pt for kp in input_matched_kp], method=cv2.RANSAC,
        ransacReprojThreshold=3.0, maxIters=2000, confidence=0.99, )

    # Get the coordinates of the corners of the template image in the input image
    rows, cols = template.shape[:2]
    corners = [[0, 0], [0, rows], [cols, rows], [cols, 0]]
    corners = cv2.transform(np.array([corners]), M)[0]

    tmp_img = large_image.copy()
    # Draw a rectangle around the region in the input image that matches the template image
    cv2.polylines(
        tmp_img, [corners.astype(np.int32)], True, (0, 255, 0), thickness=2
        )

    cv2.imshow("found", tmp_img)
    cv2.waitKey(0)

    if len(keypoints1) > 0 and len(keypoints2) > 0:
        # Calculate the similarity score based on the number and quality of the matched keypoints
        return (
            len(matches) / max(len(keypoints1),
            len(keypoints2)), ((0, 0), (0, 0))
        )

    return 0, ((-1, -1), (-1, -1))


def sharpen_image(image: np.ndarray) -> np.ndarray:
    """
    sharpen an image (in form of a np.ndarray)

    :param image: input image
    :return: processed image
    """
    # Define the kernel for sharpening
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

    # Apply the kernel to the input image
    sharpened_image = cv2.filter2D(image, -1, kernel)

    return sharpened_image
