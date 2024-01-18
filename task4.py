import cv2
import numpy as np

# Define the HSV threshold range for blue color
H_LOW, S_LOW, V_LOW = 100, 100, 100
H_HIGH, S_HIGH, V_HIGH = 130, 255, 255

# Open the camera
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Convert the frame from BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the color range for blue
    lower_color = np.array([H_LOW, S_LOW, V_LOW])
    upper_color = np.array([H_HIGH, S_HIGH, V_HIGH])

    # Threshold the HSV image to get only the blue color
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding boxes around the detected contours
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the frame with bounding boxes
    cv2.imshow('Blue Object Tracking', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
