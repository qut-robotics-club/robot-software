import cv2 as cv
import numpy as np
from picamera2 import Picamera2

picam2 = Picamera2()
# picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()
print("Camera opened")

imgOld = picam2.capture_array()

lastKey = " "
while True:
    img = picam2.capture_array()

    img[0, 0, 0]
    imgSlice = img[:, 300:500, :]

    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    target_value = 140
    target_sat = 90
    target_hue = 52

    value_range = 50
    sat_range = 50
    hue_range = 8
    mask = cv.inRange(
        img_hsv,
        (target_hue - hue_range, target_sat - sat_range, target_value - value_range),
        (target_hue + hue_range, target_sat + sat_range, target_value + value_range),
    )

    dilate_kernel = cv.getStructuringElement(cv.MORPH_RECT, (9, 9))
    processed_mask = cv.dilate(mask, dilate_kernel)

    erode_kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
    processed_mask = cv.erode(processed_mask, erode_kernel)

    contours, _ = cv.findContours(processed_mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    cv.drawContours(img, contours, -1, (255, 255, 255), 2, cv.LINE_AA)

    # print("foobar")

    if lastKey == ord("a"):
        cv.imshow("Debug Image", mask)
    elif lastKey == ord("s"):
        cv.imshow("Debug Image", img_hsv)
    elif lastKey == ord("d"):
        cv.imshow("Debug Image", processed_mask)
    else:
        cv.imshow("Debug Image", img)
    read_key = cv.waitKey(1)
    if read_key != -1:
        lastKey = read_key
