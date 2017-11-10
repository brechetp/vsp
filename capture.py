import numpy as np
import cv2
import myfeatures, config
import pdb
cap = cv2.VideoCapture(0)

config = config.Config() # config object
hog_obj = myfeatures.HOG(config) # init the hog object
cntFrame = 0
refreshHOG = 30

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if (cntFrame == 0): # every refreshHOG frames
        _, hog_image = hog_obj.compute(gray, visualise=True)
    # pdb.set_trace()

    # Display the resulting frame
    cv2.namedWindow("Channels") # we create the frame for displaying multiple windows with opencv
    cv2.imshow("HOG", hog_image) # display the channel image

    cv2.namedWindow("Main")
    cv2.imshow("Main", frame)
    # hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 0.02))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cntFrame += 1
    cntFrame %= refreshHOG # we loop the counter every refresh HOG frame

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
