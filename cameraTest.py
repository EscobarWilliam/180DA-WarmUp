import cv2 as cv
import numpy as np

# Read the image in color (not grayscale)
img = cv.imread('/Users/williamescobar/Downloads/Cat.jpeg')
assert img is not None, "file could not be read, check with os.path.exists()"

# Convert the image to grayscale
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# Apply a threshold to the grayscale image
ret, thresh = cv.threshold(gray, 145, 255, 0)

#note that thresh is now the altered image where we converted pixesl
#to either 255 or 0 depending on if they were above or below the threshold
#value of 145

# Find contours in the thresholded image
contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.RETR_CCOMP)

#contours: A list where each element is a numpy array representing a contour. The numpy array 
# contains the (x, y) coordinates of the points that make up the contour.

#These parameters control how contours are detected and represented. By using cv.RETR_EXTERNAL, 
#you are asking the function to find only the outer contours of the connected components in the
# binary image. The cv.CHAIN_APPROX_SIMPLE method simplifies the contours by removing redundant 
# points and compressing the contour representation.

# Iterate over contours and draw rectangles
for cnt in contours:
    x, y, w, h = cv.boundingRect(cnt)
    cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Display the image with rectangles
cv.imshow('Bounding Boxes', img)
cv.waitKey(0)
cv.destroyAllWindows()
