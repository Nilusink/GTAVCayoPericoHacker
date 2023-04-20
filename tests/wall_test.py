"""
wall_test.py
19. April 2023

tests for wall-safe hack

Author:
Nilusink
"""
from time import perf_counter
import numpy as np
import cv2


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


# constants
N_ROWS: int = 8
N_COLUMNS: int = 10


N_SET_NUMBERS: int = 4

SET_NUMBERS_START: tuple[int, int] = (537, 176)
SET_NUMBERS_OFFSET: float = 65

SET_DIGIT_SIZE: tuple[int, int] = (56, 38)
SET_DIGIT_SIZE_2: tuple[int, int] = (
    int(SET_DIGIT_SIZE[0] / 2), int(SET_DIGIT_SIZE[1] / 2)
)


FIRST_NUM: tuple[int, int] = (330, 288)
ROW_OFFSET: float = 40.5
COLUMN_OFFSET: float = 64

DIGIT_SIZE: tuple[int, int] = (48, 32)
DIGIT_SIZE_2: tuple[int, int] = (
    int(DIGIT_SIZE[0] / 2),
    int(DIGIT_SIZE[1] / 2)
)

# load image
input_img = sharpen_image(cv2.imread("../images/numbers2.jpg"))
draw_img = input_img.copy()

start_time = perf_counter()
# set numbers
SET_NUM_IMAGES: list[np.ndarray] = [...] * N_SET_NUMBERS
for number in range(N_SET_NUMBERS):
    coords = (
        SET_NUMBERS_START[0] + int(SET_NUMBERS_OFFSET * number),
        SET_NUMBERS_START[1]
    )

    start = (coords[0] - SET_DIGIT_SIZE_2[0], coords[1] - SET_DIGIT_SIZE_2[1])
    end = (coords[0] + SET_DIGIT_SIZE_2[0], coords[1] + SET_DIGIT_SIZE_2[1])

    cv2.rectangle(draw_img, start, end, (0, 155, 0), 1)

    num_img = input_img[start[1]:end[1], start[0]:end[0]]

    SET_NUM_IMAGES[number] = num_img


def check_match(image: np.ndarray, thresh: float = .1) -> int:
    """
    :param image:
    :return: -1: noting found, 0 - N_SET_DIGITS: similar to
    """
    match_values: list[float] = [0] * N_SET_NUMBERS

    for i, num_image in enumerate(SET_NUM_IMAGES):
        match, _ = match_images(image, num_image)
        match_values[i] = match

        # if match > thresh:
        #     cv2.imshow("num", image)
        #     cv2.imshow("template", num_image)
        #     cv2.waitKey(0)

    max_val = max(match_values)

    if max_val > thresh:
        return match_values.index(max_val)

    return -1


# lower stuff
# create list with all 0
fields: list[list[int]] = [[-1] * N_COLUMNS for _ in range(N_ROWS)]

for row in range(N_ROWS):
    for column in range(N_COLUMNS):
        coords = (
            FIRST_NUM[0] + int(COLUMN_OFFSET * column),
            FIRST_NUM[1] + int(ROW_OFFSET * row)
        )

        start = (
            coords[0] - DIGIT_SIZE_2[0],
            coords[1] - DIGIT_SIZE_2[1]
        )

        end = (
            coords[0] + DIGIT_SIZE_2[0],
            coords[1] + DIGIT_SIZE_2[1]
        )

        # cut out number
        num_img = input_img[start[1]:end[1], start[0]:end[0]]
        # num_img = sharpen_image(cv2.resize(num_img, SET_DIGIT_SIZE))
        num_img = cv2.resize(num_img, SET_DIGIT_SIZE)

        average_color = np.mean(num_img)
        # print(average_color)
        # cv2.imshow("", num_img)
        # cv2.waitKey(0)

        is_selected = average_color < 50

        if is_selected:
            # draw rectangle around number
            cv2.rectangle(draw_img, start, end, (0, 155, 0), 1)

        # check for match
        m = check_match(num_img)

        if m != -1:
            cv2.circle(
                draw_img, coords, 4,
                (0, 0, 255), 7
            )

        fields[row][column] = m


# check for results
n_results: int = 0
target_xy: tuple[int, int] = (-1, -1)


for r, row in enumerate(fields):
    for c, column in enumerate(row):
        if c < N_COLUMNS - 4 and column == 0:
            if all([row[c+n] == n for n in range(1, 4)]):
                start = (
                    FIRST_NUM[0] + int(c * COLUMN_OFFSET) - DIGIT_SIZE_2[0],
                    FIRST_NUM[1] + int(r * ROW_OFFSET) - DIGIT_SIZE_2[1],
                )

                end = (
                    FIRST_NUM[0] + int((c + 3) * COLUMN_OFFSET) +
                    DIGIT_SIZE_2[0],
                    FIRST_NUM[1] + int(r * ROW_OFFSET) + DIGIT_SIZE_2[1],
                )

                cv2.rectangle(draw_img, start, end, (255, 255, 0))
                target_xy = r, c
                n_results += 1


if n_results > 1:
    print("MULTIPLE SOLUTIONS DETECTED!")


delta = perf_counter() - start_time

cv2.imshow(f"took {delta * 1000:.3f} ms", draw_img)
cv2.waitKey(0)
