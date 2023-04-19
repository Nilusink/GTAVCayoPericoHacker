import cv2

# Load the input and template images
input_img = cv2.imread('finger1.png')
template_img = cv2.imread('cayo1.png')

# Initialize the ORB feature detector and descriptor extractor
orb = cv2.ORB_create()

# Detect and compute the features and descriptors for the input and template images
input_kp, input_desc = orb.detectAndCompute(input_img, None)
template_kp, template_desc = orb.detectAndCompute(template_img, None)

# Create a BFMatcher object with the Hamming distance as the distance measure
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Match the descriptors of the input and template images using the BFMatcher
matches = bf.match(input_desc, template_desc)

# Sort the matches by their distance (lower distances indicate better matches)
matches = sorted(matches, key=lambda x: x.distance)

# Extract the matched keypoints from the input and template images
input_matched_kp = [input_kp[match.queryIdx] for match in matches]
template_matched_kp = [template_kp[match.trainIdx] for match in matches]

# Estimate an affine transformation that maps the template image onto the input image
M, _ = cv2.estimateAffinePartial2D(
    srcPoints=[kp.pt for kp in template_matched_kp],
    dstPoints=[kp.pt for kp in input_matched_kp],
    method=cv2.RANSAC,
    ransacReprojThreshold=3.0,
    maxIters=2000,
    confidence=0.99,
)

# Get the coordinates of the corners of the template image in the input image
rows, cols = template_img.shape[:2]
corners = [[0, 0], [0, rows], [cols, rows], [cols, 0]]
corners = cv2.transform(np.array([corners]), M)[0]

# Draw a rectangle around the region in the input image that matches the template image
cv2.polylines(input_img, [corners.astype(np.int32)], True, (0, 255, 0), thickness=2)

# Display the result
cv2.imshow('Input Image', input_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
