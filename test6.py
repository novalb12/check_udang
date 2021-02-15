# import numpy as np
# import cv2
# import Cars
# import time


# def nothing(x):
#     pass


# cv2.namedWindow("Trackbars")
# cv2.createTrackbar("Bawah", "Trackbars", 0, 500, nothing)
# cv2.createTrackbar("Atas", "Trackbars", 0, 500, nothing)

# # mendefinisikan input dan output
# cnt_up = 0
# cnt_down = 0
# # Membuka video
# cap = cv2.VideoCapture('udang.mp4')
# # Dimensi (properti) video
# # cap.set(3,160) #Width
# # cap.set(4,120) #Height
# # Meletakkan properti video ke setiap frame di video
# for i in range(19):
#     print(i), cap.get(i)
# w = cap.get(3)
# h = cap.get(4)
# frameArea = h*w
# areaTH = 10
# print('Area Threshold'), areaTH
# # Garis masuk dan keluar
# line_up = 300
# line_down = 400
# up_limit = 250
# down_limit = 450
# print("Red line y:"), str(line_down)
# print("Blue line y:"), str(line_up)
# line_down_color = (255, 0, 0)
# line_up_color = (0, 0, 255)
# pt1 = [0, line_down]
# pt2 = [w, line_down]
# pts_L1 = np.array([pt1, pt2], np.int32)
# pts_L1 = pts_L1.reshape((-1, 1, 2))
# pt3 = [0, line_up]
# pt4 = [w, line_up]
# pts_L2 = np.array([pt3, pt4], np.int32)
# pts_L2 = pts_L2.reshape((-1, 1, 2))
# pt5 = [0, up_limit]
# pt6 = [w, up_limit]
# pts_L3 = np.array([pt5, pt6], np.int32)
# pts_L3 = pts_L3.reshape((-1, 1, 2))
# pt7 = [0, down_limit]
# pt8 = [w, down_limit]
# pts_L4 = np.array([pt7, pt8], np.int32)
# pts_L4 = pts_L4.reshape((-1, 1, 2))
# # Background subtractor
# fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=True)
# # Elemen struktural untuk filter morfologi
# kernelOp = np.ones((3, 3), np.uint8)
# kernelOp2 = np.ones((5, 5), np.uint8)
# kernelCl = np.ones((11, 11), np.uint8)
# # Variabel-variabel
# font = cv2.FONT_HERSHEY_SIMPLEX
# cars = []
# max_p_age = 5
# pid = 1
# while (cap.isOpened()):
#     b = cv2.getTrackbarPos("Bawah", "Trackbars")
#     a = cv2.getTrackbarPos("Atas", "Trackbars")
#     # Membaca gambar dari aliran video
#     ret, frame = cap.read()
#     for i in cars:
#         i.age_one()  # tandai setiap mobil sebagai satu object
#     # Tahap Pra-pengolahan
#     # Penerapan background subtractor
#     fgmask = fgbg.apply(frame)
#     fgmask2 = fgbg.apply(frame)
# # Menggunakan metode binarisasi untuk menghilangkan bayangan (color ke grey)
#     try:
#         ret, imBin = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
#         ret, imBin2 = cv2.threshold(fgmask2, 200, 255, cv2.THRESH_BINARY)

#         # Proses Opening (erosi->dilasi) untuk menghilangkan noise
#         mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernelOp)
#         mask2 = cv2.morphologyEx(imBin2, cv2.MORPH_OPEN, kernelOp)

#         # Proses Closing (dilasi -> erosi) untuk menghilangkan pixel ke putih
#         mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernelCl)
#         mask2 = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, kernelCl)
#     except:
#         print('EOF')
#         print('UP:'), cnt_up
#         print('DOWN:'), cnt_down
#         break

# # Pembuatan Kontur

#     contours, hierarchy = cv2.findContours(
#         mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     for cnt in contours:
#         area = cv2.contourArea(cnt)
#         if (area > b) & (area < a):

#             #   TRACKING
#             # Pengaturan untuk kondisi mobil yang jamak

#             M = cv2.moments(cnt)
#             cx = int(M['m10']/M['m00'])
#             cy = int(M['m01']/M['m00'])
#             x, y, w, h = cv2.boundingRect(cnt)
#             new = True
#             if cy in range(up_limit, down_limit):
#                 for i in cars:
#                     if abs(cx-i.getX()) <= w and abs(cy-i.getY()) <= h:

#                       # object dekat dengan object yang telah terdeteksi sebelumnya
#                         new = False
#                         i.updateCoords(cx, cy)
#       # perbaharui koordinat dalam object dalam atur ulang usia (awal penandaan)
#                         if i.going_UP(line_down, line_up) == True:
#                             cnt_up += 1
#                             print("ID:",
#                                   i.getId(), 'crossed going up at', time.strftime("%c"))
#                         elif i.going_DOWN(line_down, line_up) == True:
#                             cnt_down += 1
#                             print("ID:",
#                                   i.getId(), 'crossed going down at', time.strftime("%c"))
#                         break
#                     if i.getState() == '1':
#                         if i.getDir() == 'down' and i.getY() > down_limit:
#                             i.setDone()
#                         elif i.getDir() == 'up' and i.getY() < up_limit:
#                             i.setDone()
#                     if i.timedOut():
#                       # hapus object (mobil) dari daftar
#                         index = cars.index(i)
#                         cars.pop(index)
#                         del i  # hapus dari memori
#                 if new == True:
#                     p = Cars.MyCars(pid, cx, cy, max_p_age)
#                     cars.append(p)
#                     pid += 1

#             # Gambar

#             cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
#             img = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
#             # cv2.drawContours(frame, cnt, -1, (0,255,0), 3)

#     # Akhir cnt dalam kontur

#     # Trayektori Gambar

#     for i in cars:
#         cv2.putText(frame, str(i.getId()), (i.getX(), i.getY()),
#                     font, 0.7, i.getRGB(), 1, cv2.LINE_AA)
#     str_up = 'Naik: ' + str(cnt_up)
#     str_down = 'Turun: ' + str(cnt_down)
#     frame = cv2.polylines(frame, [pts_L1], False, line_down_color, thickness=2)
#     frame = cv2.polylines(frame, [pts_L2], False, line_up_color, thickness=2)
#     frame = cv2.polylines(frame, [pts_L3], False, (255, 255, 255), thickness=1)
#     frame = cv2.polylines(frame, [pts_L4], False, (255, 255, 255), thickness=1)
#     cv2.putText(frame, str_up, (15, 40), font, 0.5,
#                 (200, 200, 200), 2, cv2.LINE_AA)
#     cv2.putText(frame, str_up, (15, 40), font,
#                 0.5, (0, 200, 0), 1, cv2.LINE_AA)
#     cv2.putText(frame, str_down, (15, 60), font,
#                 0.5, (200, 200, 200), 2, cv2.LINE_AA)
#     cv2.putText(frame, str_down, (15, 60), font,
#                 0.5, (0, 0, 200), 1, cv2.LINE_AA)
#     cv2.imshow('Frame', frame)
#     # cv2.imshow('Mask',mask)

#     # klik ESC untuk keluar
#     k = cv2.waitKey(30) & 0xff
#     if k == 27:
#         break
# # Akhir untuk while(cap.isOpened())

# # bersihkan layar
# cap.release()
# cv2.destroyAllWindows()

import datetime
import math
import cv2
import numpy as np

# global variables
width = 0
height = 0
EntranceCounter = 0
ExitCounter = 0
MinCountourArea = 800  # Adjust ths value according to your usage
BinarizationThreshold = 70  # Adjust ths value according to your usage
OffsetRefLines = 150  # Adjust ths value according to your usage

# Check if an object in entering in monitored zone


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


camera = cv2.VideoCapture('udang.mp4')

# force 640x480 webcam resolution
camera.set(3, 640)
camera.set(4, 480)

ReferenceFrame = None

# The webcam maybe get some time / captured frames to adapt to ambience lighting. For this reason, some frames are grabbed and discarted.
for i in range(0, 20):
    (grabbed, Frame) = camera.read()

while True:
    (grabbed, Frame) = camera.read()
    height = np.size(Frame, 0)
    width = np.size(Frame, 1)

    # if cannot grab a frame, this program ends here.
    if not grabbed:
        break

    # gray-scale convertion and Gaussian blur filter applying
    GrayFrame = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY)
    GrayFrame = cv2.GaussianBlur(GrayFrame, (21, 21), 0)

    if ReferenceFrame is None:
        ReferenceFrame = GrayFrame
        continue

    # Background subtraction and image binarization
    FrameDelta = cv2.absdiff(ReferenceFrame, GrayFrame)
    FrameThresh = cv2.threshold(
        FrameDelta, BinarizationThreshold, 255, cv2.THRESH_BINARY)[1]

    # Dilate image and find all the contours
    FrameThresh = cv2.dilate(FrameThresh, None, iterations=2)
    cnts = cv2.findContours(
        FrameThresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    QttyOfContours = 0

    # plot reference lines (entrance and exit lines)
    CoorYEntranceLine = (height // 2)-OffsetRefLines
    CoorYExitLine = (height // 2)+OffsetRefLines
    # cv2.line(Frame, (0, CoorYEntranceLine),
    #          (width, CoorYEntranceLine),
    #          (255, 0, 0), 1)
    # cv2.line(Frame, (0, CoorYExitLine), (width, CoorYExitLine), (0, 0, 255), 2)

    # check all found countours
    for c in cnts:
        # if a contour has small area, it'll be ignored
        if (cv2.contourArea(c) > 800) or (cv2.contourArea(c) < 110):
            continue

        QttyOfContours = QttyOfContours+1

        # draw an rectangle "around" the object
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(Frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # find object's centroid
        CoordXCentroid = (x + x + w) // 2
        CoordYCentroid = (y + y + h) // 2
        ObjectCentroid = (CoordXCentroid, CoordYCentroid)
        cv2.circle(Frame, ObjectCentroid, 1, (0, 0, 0), 5)

        if (CheckEntranceLineCrossing(CoordYCentroid, CoorYEntranceLine, CoorYExitLine)):
            EntranceCounter += 1

        if (CheckExitLineCrossing(CoordYCentroid, CoorYEntranceLine, CoorYExitLine)):
            ExitCounter += 1

    print("Total countours found: "+str(QttyOfContours))

    # Write entrance and exit counter values on frame and shows it
    cv2.putText(Frame, "Entrances: {}".format(str(EntranceCounter)), (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250, 0, 1), 2)
    cv2.putText(Frame, "Exits: {}".format(str(ExitCounter)), (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow("Original Frame", Frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break


# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
