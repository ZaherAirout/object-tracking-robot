import cv2
import numpy as np

cap = cv2.VideoCapture(0)  # -- webcam


# cap = cv2.VideoCapture('/home/stephen/Desktop/source clips/3.avi')

def nothing(arg): pass


# takes an image, and a lower and upper bound
# returns only the parts of the image in bounds
def only_color(frame, xxx_todo_changeme):
    # Convert BGR to HSV
    (b, r, g, b1, r1, g1) = xxx_todo_changeme
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower = np.array([b, r, g])
    upper = np.array([b1, r1, g1])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower, upper)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)
    return res, mask


# setup trackbars
cv2.namedWindow('image')
cv2.createTrackbar('h', 'image', 0, 255, nothing)
cv2.createTrackbar('h1', 'image', 255, 255, nothing)

# main loop of the program
while True:
    # read image from the video
    _, img = cap.read()
    # get trackbar values
    h = cv2.getTrackbarPos('h', 'image')
    h1 = cv2.getTrackbarPos('h1', 'image')
    # extract only the colors between h,s,v and h1,s1,v1
    img, mask = only_color(img, (h, 0, 0, h1, 255, 255))
    # show the image and wait
    cv2.imshow('img', img)
    k = cv2.waitKey(150)
    if k == 27:
        break
# release the video to avoid memory leaks, and close the window
cap.release()
cv2.destroyAllWindows()
