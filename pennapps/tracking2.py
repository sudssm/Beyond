import cv2 
import numpy as np 


from time import sleep
frame=cv2.imread('led_crop.jpeg')
img=cv2.GaussianBlur(frame, (5,5), 0)

img=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

orange = np.uint8([[[186, 109, 199]]])
hsv_orange = cv2.cvtColor(orange, cv2.COLOR_BGR2HSV)[0][0]
lower_pink = np.array([hsv_orange[0]-20, 100, 100])
upper_pink = np.array([hsv_orange[0] + 80, 255, 255])

lw = np.array([0,0,0], dtype=np.uint8)
uw = np.array([10,20,255], dtype=np.uint8)

# lower=np.array([0, 0, 0],np.uint8)
# upper=np.array([10, 20, 255],np.uint8)

black=np.uint8([[[10,10,10]]])
hsv_black = cv2.cvtColor(black, cv2.COLOR_BGR2HSV)[0][0]


lower = np.array([0,0,0], dtype=np.uint8)
upper = np.array([255,255,40], dtype=np.uint8)

separated=cv2.inRange(img,lower,upper)

def findCenter(mask): 
    centres = []
    contours, hierarchy = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(contours)):
        if cv2.contourArea(contours[i]) < 500:
            continue
        moments = cv2.moments(contours[i])
        if moments['m00'] > 0:
            centres.append((int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00'])))
            cv2.circle(mask, centres[-1], 3, (255, 255, 255), -1)
            print centres[-1]

#this bit draws a red rectangle around the detected region
contours,hierarchy=cv2.findContours(separated,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
max_area = 0
largest_contour = None
for idx, contour in enumerate(contours):
    area = cv2.contourArea(contour)
    if area > max_area:
        max_area = area
        largest_contour=contour
if not largest_contour==None:
    moment = cv2.moments(largest_contour)
    if moment["m00"] > 500:
        rect = cv2.minAreaRect(largest_contour)
        rect_perim = ((rect[0][0], rect[0][1]), (rect[1][0], rect[1][1]), rect[2])
        box = cv2.cv.BoxPoints(rect_perim)
        box = np.int0(box)
        cv2.drawContours(frame,[box], 0, (0, 0, 255), 2)
        crop = img[box[0][0]:box[0][1], box[1][0]:box[1][1]]
        pink = cv2.inRange(crop, lower_pink, upper_pink)
        findCenter(pink)



res = cv2.bitwise_and(frame,frame, mask= separated)
while (1):
    cv2.imshow('img',frame)
    # cv2.imshow('res', res)
    cv2.imshow('pink', pink)
