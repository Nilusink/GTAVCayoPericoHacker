import cv2
import numpy as np
from time import perf_counter
from finger_detection.image_tools import *
from finger_detection import *


# Capture screenshots of the images to compare
print("loading")
cayo = cv2.imread('cayo.jpg')

N_LEFT: int = 6
N_RIGHT: int = 7


# image matching
left_finger = get_fingerprint_image(cayo, False, 6)
right_finger = get_fingerprint_image(cayo, True, 7)

draw_fingerprint_rectangle(cayo, False, 6)
draw_fingerprint_rectangle(cayo, True, 0)
draw_fingerprint_rectangle(cayo, True, 7)

cv2.imshow("rects", cayo)
cv2.imshow("Left Finger", left_finger)
cv2.imshow("Right Finger", right_finger)

cv2.waitKey(0)

# Convert the images to grayscale
print("starting match")
start = perf_counter()
gray1 = cv2.cvtColor(left_finger, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(right_finger, cv2.COLOR_BGR2GRAY)


# Apply template matching
result = cv2.matchTemplate(gray1, gray2, cv2.TM_CCOEFF_NORMED)


# Get the similarity percentage
similarity = np.max(result)
delta = perf_counter() - start

print(f"took {delta:.2f} seconds")


# Print the similarity percentage
print(f"The images are {similarity * 100:.2f}% similar")
