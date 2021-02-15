import cv2
import numpy as np
import dlib


def nothing(x):
    pass


def CheckEntranceLineCrossing(y, CoorYEntranceLine, CoorYExitLine):
    AbsDistance = abs(y - CoorYEntranceLine)

    if ((AbsDistance <= 2) and (y < CoorYExitLine)):
        return 1
    else:
        return 0

# Check if an object in exitting from monitored zone


def CheckExitLineCrossing(y, CoorYEntranceLine, CoorYExitLine):
    AbsDistance = abs(y - CoorYExitLine)
    if ((AbsDistance <= 2) and (y > CoorYEntranceLine)):
        return 1
    else:
        return 0


FIRST_FRAME = None
OffsetRefLines = 50
EntranceCounter = 0
ExitCounter = 0
SKIP_FRAME = 10
COUNT_FRAME = 1
trackers = []
cap = cv2.VideoCapture('udang.mp4')

# cv2.namedWindow("Trackbars")
# cv2.createTrackbar("up", "Trackbars", 0, 1000, nothing)
# cv2.createTrackbar("down", "Trackbars", 0, 1000, nothing)
while (cap.isOpened()):
    ret, frame = cap.read()
    height = np.size(frame, 0)
    width = np.size(frame, 1)
    # simbol // untuk definisi integer
    CoorYEntranceLine = (height // 2)-OffsetRefLines
    CoorYExitLine = (height // 2)+OffsetRefLines
    cv2.line(frame, (0, CoorYEntranceLine),
             (width, CoorYEntranceLine),
             (255, 0, 0), 1)
    cv2.line(frame, (0, CoorYExitLine), (width, CoorYExitLine), (0, 0, 255), 2)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if FIRST_FRAME is None:
        FIRST_FRAME = gray
        continue

    frameDelta = cv2.absdiff(FIRST_FRAME, gray)

    # up = cv2.getTrackbarPos("up", "Trackbars")
    # down = cv2.getTrackbarPos("down", "Trackbars")
    thresh = cv2.threshold(frameDelta, 20, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=5)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[0]
    if COUNT_FRAME % SKIP_FRAME == 0:
        trackers = []
        for i, c in enumerate(cnts):
            # if (cv2.contourArea(c) < 110) or (cv2.contourArea(c) > 800):
            #     continue
            (x, y, w, h) = cv2.boundingRect(c)
            if (w < 10) or (w > 62):
                continue
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            t = dlib.correlation_tracker()
            rect = dlib.rectangle(x, y, (x+w), (y+h))
            t.start_track(gray, rect)
            trackers.append([t, False])
    else:
        for (i, tracker) in enumerate(trackers):
            if (tracker[1]):
                continue
            tracker[0].update(gray)
            pos = tracker[0].get_position()
            # unpack the position object
            startX = int(pos.left())
            startY = int(pos.top())
            endX = int(pos.right())
            endY = int(pos.bottom())
            # draw the bounding box from the correlation object tracker
            cv2.rectangle(frame, (startX, startY), (endX, endY),
                          (0, 255, 0), 2)
            cv2.putText(frame, str(i), (startX, startY - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
            CoordXCentroid = (startX+endX) // 2
            CoordYCentroid = (startY+endY) // 2
            ObjectCentroid = (CoordXCentroid, CoordYCentroid)
            if (CheckEntranceLineCrossing(CoordYCentroid, CoorYEntranceLine, CoorYExitLine)):
                print("id" + str(i) + " up")
                tracker[1] = True
                EntranceCounter += 1

            if (CheckExitLineCrossing(CoordYCentroid, CoorYEntranceLine, CoorYExitLine)):
                print("id" + str(i) + " down")
                tracker[1] = True
                ExitCounter += 1
    # for i, c in enumerate(cnts):
    #     if (cv2.contourArea(c) < 110) or (cv2.contourArea(c) > 700):
    #         continue
    #     (x, y, w, h) = cv2.boundingRect(c)
    #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #     CoordXCentroid = (x + x + w) // 2
    #     CoordYCentroid = (y + y + h) // 2
    #     ObjectCentroid = (CoordXCentroid, CoordYCentroid)

    #     cv2.circle(frame, ObjectCentroid, 1, (0, 0, 0), 5)
    #     cv2.putText(frame, str(i), (x, y),
    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250, 0, 1), 2)
    #     if (CheckEntranceLineCrossing(CoordYCentroid, CoorYEntranceLine, CoorYExitLine)):
    #         print("id"+str(i)+" up")
    #         EntranceCounter += 1

    #     if (CheckExitLineCrossing(CoordYCentroid, CoorYEntranceLine, CoorYExitLine)):
    #         print("id"+str(i)+" down")
    #         ExitCounter += 1

    cv2.putText(frame, "Entrances: {}".format(str(EntranceCounter)), (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250, 0, 1), 2)
    cv2.putText(frame, "Exits: {}".format(str(ExitCounter)), (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow('frame', frame)
    COUNT_FRAME += 1
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
