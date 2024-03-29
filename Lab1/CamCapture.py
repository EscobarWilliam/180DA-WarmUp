import numpy as np
import cv2

#To capture a video, you need to create a VideoCapture object. Its 
# argument can be either the device index or the name of a video file. 
# Device index is just the number to specify which camera. Normally one 
# camera will be connected (as in my case). So I simply pass 0 (or -1). 
cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()