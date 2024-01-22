import cv2
import numpy as np
import matplotlib.pyplot as plt

def find_histogram(labels):
    """
    create a histogram with k clusters
    :param: labels
    :return: hist
    """
    num_labels = np.arange(0, len(np.unique(labels)) + 1)
    (hist, _) = np.histogram(labels, bins=num_labels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist

def plot_colors(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    start_x = 0

    # Convert centroids to RGB color space to be displayed
    centroids_rgb = cv2.cvtColor(np.uint8([centroids]), cv2.COLOR_BGR2RGB)[0]

    for (percent, color) in zip(hist, centroids_rgb):
        end_x = start_x + (percent * 300)
        cv2.rectangle(bar, (int(start_x), 0), (int(end_x), 50), tuple(map(int, color)), -1)
        start_x = end_x

    return bar

# Open a video capture object
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video feed
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get the center part of the frame
    center_x, center_y = frame.shape[1] // 2, frame.shape[0] // 2
    size = 100  # Size of the region in the center to analyze
    center_crop = frame[center_y - size // 2:center_y + size // 2, center_x - size // 2:center_x + size // 2]

    # Reshape for clustering
    # -1 tells NumPy to automatically determine the number of pixels in the frame (rows)
    # 3 is telling us that we want three columns for the RGB values of that pixel
    pixels = center_crop.reshape((-1, 3))
    pixels = np.float32(pixels)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    # termination criteria for the KMeans algorithm.
        # cv2.TERM_CRITERIA_EPS: Terminate the algorithm when the specified accuracy (epsilon) is reached.
        # cv2.TERM_CRITERIA_MAX_ITER: Terminate the algorithm after a specified number of iterations.
        # 100: Maximum number of iterations (in this case, 100 iterations).
        # 0.2: Epsilon value, specifying the required accuracy.
        # k = 3: This line sets the number of clusters (k) for KMeans. In this case, it's set to 3, meaning 
        # the algorithm will try to group the pixels into three clusters based on color similarity.
        
    k = 3
    
    # Begin the kmeans with CV2 function .kmeans()
    _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    #labels: The cluster assignment for each pixel.
    # centers: The average color of each cluster.
    
    # Note that lables and centers are both arrays. 
        # labels is an N-numbered array for the N-pixels we analyze
        # centers is an k x 3 array for the k clusters. The 3 columns is for the average RGB in that cluster

    # Get dominant color (center of the largest cluster)
    dominant_color = centers[np.argmax(find_histogram(labels))][::-1]

    hist = find_histogram(labels)
    bar = plot_colors(hist, centers)

# Draw rectangle around the center crop
    cv2.rectangle(frame, (center_x - size // 2, center_y - size // 2), 
                  (center_x + size // 2, center_y + size // 2), (255, 0, 0), 2)

    # Display the original frame and the color bar
    cv2.imshow('Frame with Dominant Color', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    cv2.imshow('Dominant Color', bar)
    
    # Print and write out dominant color
    print("Dominant Color:", dominant_color)
    with open("dominant_color.txt", "w") as file:
        file.write("Dominant Color: {}".format(dominant_color))

    # Introduce a delay and check for the 'q' key press
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
