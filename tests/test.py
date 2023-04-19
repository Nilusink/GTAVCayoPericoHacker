import cv2
import numpy as np
from time import perf_counter
from finger_detection.image_tools import *
from finger_detection import *


# Capture screenshots of the images to compare
print("loading")
cayo = cv2.imread('cayo1.png')

N_LEFT: int = 6
N_RIGHT: int = 7


# image matching
left_finger = get_fingerprint_image(cayo, False, 0)
right_finger = get_fingerprint_image(cayo, True, 0)

left_finger = cv2.resize(left_finger, (1000, 100))
right_finger = cv2.resize(right_finger, (1000, 100))

cv2.imwrite("finger1.png", left_finger)
cv2.imwrite("finger2.png", right_finger)

draw_fingerprint_rectangle(cayo, False, 0)
draw_fingerprint_rectangle(cayo, False, 7)
draw_fingerprint_rectangle(cayo, True, 0)
draw_fingerprint_rectangle(cayo, True, 7)

cv2.imshow("rects", cayo)
cv2.imshow("Left Finger", left_finger)
cv2.imshow("Right Finger", right_finger)

cv2.waitKey(0)

# Convert the images to grayscale
print("starting match")
start = perf_counter()

# Get the similarity percentage
similarity = match_images(left_finger, right_finger)
delta = perf_counter() - start

print(f"took {delta:.2f} seconds")


# Print the similarity percentage
print(f"The images are {similarity * 100:.2f}% similar")
