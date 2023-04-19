import cv2
import numpy as np
from time import perf_counter

# Capture screenshots of the images to compare
print("loading")
img1 = cv2.imread('1.png')
img2 = cv2.imread('3.png')


# Convert the images to grayscale
print("starting match")
start = perf_counter()
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)


# Apply template matching
result = cv2.matchTemplate(gray1, gray2, cv2.TM_CCOEFF_NORMED)


# Get the similarity percentage
similarity = np.max(result)
delta = perf_counter() - start

print(f"took {delta:.2f} seconds")


# Print the similarity percentage
print(f"The images are {similarity * 100:.2f}% similar")
