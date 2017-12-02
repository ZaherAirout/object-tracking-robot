import cv2
import numpy as np

# Initialize the list of reference points and boolean indicating whether cropping is being performed or not.
refPt = []
cropping = False
image = None
window_main = "Camera feed"
window_cropping = "Select ROI"
window_result = "Result"


def click_and_crop(event, x, y, flags, param):
    # Grab references to the global variables.
    global refPt, cropping
    global frame, target_frame, window_main, window_cropping, window_result

    # If the left mouse button was clicked, record the starting (x, y) coordinates and indicate that cropping is being
    # performed.
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True
    # Check to see if the left mouse button was released.
    elif event == cv2.EVENT_LBUTTONUP:
        # Record the ending (x, y) coordinates and indicate that the cropping operation is finished.
        refPt.append((x, y))
        cropping = False
        # Draw a rectangle around the region of interest.
        cv2.rectangle(target_frame, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow(window_cropping, target_frame)
    else:
        pass


def show_webcam(detector='orb', matching='bf', mirror=False):
    global frame, target_frame, window_main, window_cropping, window_result

    # Initialize detector.
    if detector == 'orb':
        detector = cv2.ORB_create()
    else:
        print('Unrecognized detector.')
        quit()
    MIN_MATCH_COUNT = 10
    cam = cv2.VideoCapture()
    cam.open('http://192.168.1.18:8080/stream/video.h264')
    # Press 'Esc' to quit.
    while cv2.waitKey(1) != 27:
        ret_val, frame = cam.read()
        if ret_val == False:
            print("Frame is empty")
        if mirror:
            frame = cv2.flip(frame, 1)
        cv2.imshow(window_main, frame)
        key = cv2.waitKey(1) & 0xFF

        # Press 's' to freeze capture and crop target.
        if key == ord('s'):
            target_frame = frame.copy()
            # Create window for the frozen frame.
            cv2.imshow(window_cropping, target_frame)
            cv2.moveWindow(window_cropping, 200, 200)
            cv2.setMouseCallback(window_cropping, click_and_crop)

        # If ROI has been selected, proceed with matching.
        if len(refPt) == 2:
            roi = target_frame[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]

            # Find the keypoints and descriptors with ORB.
            kp1, des1 = detector.detectAndCompute(roi, None)
            kp2, des2 = detector.detectAndCompute(frame, None)

            # Match the descriptors.
            matcher = None
            matches = None
            if matching == 'flann':
                FLANN_INDEX_KDTREE = 0
                index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
                search_params = dict(checks=50, crossCheck=False)
                matcher = cv2.FlannBasedMatcher(index_params, search_params)
            elif matching == 'bf':
                matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
            else:
                print('Unrecognized matching method.')
                quit()
            if matcher:
                matches = matcher.knnMatch(np.asarray(des1, np.float32), np.asarray(des2, np.float32), k=2)
            else:
                print('Unrecognized matching method.')
                quit()

            # Store all the good matches as per Lowe's ratio test.
            good = []
            for m, n in matches:
                if m.distance < 0.7 * n.distance:
                    good.append(m)
            if len(good) > MIN_MATCH_COUNT:
                src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
                dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

                M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
                if mask is not None:
                    matchesMask = mask.ravel().tolist()

                    h, w, c = roi.shape
                    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
                    dst = cv2.perspectiveTransform(pts, M)

                    frame = cv2.polylines(frame, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

                    draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                                       singlePointColor=None,
                                       matchesMask=matchesMask,  # draw only inliers
                                       flags=2)

                    result = cv2.drawMatches(roi, kp1, frame, kp2, good, None, **draw_params)
                    cv2.imshow(window_result, result)
            else:
                print("Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT))
                matchesMask = None
    cv2.destroyAllWindows()


def main():
    show_webcam(detector='orb', matching='flann', mirror=True)


if __name__ == '__main__':
    main()
