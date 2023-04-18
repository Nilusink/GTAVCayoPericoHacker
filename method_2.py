import cv2
import numpy as np
from time import perf_counter

# Capture screenshots of the images to compare
print("loading")
img1 = cv2.imread('finger1.png')
img2 = cv2.imread('finger2.png')

# Convert the images to grayscale
print("starting match")
start = perf_counter()
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

gray1 = cv2.resize(gray1, (4000, 400))
gray2 = cv2.resize(gray2, (4000, 400))

# Create a feature detector and descriptor extractor
detector = cv2.ORB_create()

# Detect keypoints and descriptors for both images
keypoints1, descriptors1 = detector.detectAndCompute(gray1, None)
keypoints2, descriptors2 = detector.detectAndCompute(gray2, None)

# Create a brute-force matcher
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Match the keypoints and descriptors of the two images
matches = bf.match(descriptors1, descriptors2)

# Calculate the similarity score based on the number and quality of the matched keypoints
similarity = len(matches) / max(len(keypoints1), len(keypoints2))

delta = perf_counter() - start

print(f"took {delta:.2f} seconds")


# Print the similarity percentage
print(f"The images are {similarity * 100:.2f}% similar")
