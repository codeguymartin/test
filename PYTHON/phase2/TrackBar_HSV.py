import cv2,os
import numpy as np
#optional argument
def nothing(x):
    pass

dir_pathIN = '/home/martin/Documents/PYTHON/Golf_Card_Reader/images/phase2'

#file = 'Birds_subset1.tif'
file = 'golf_scores_N2_marked.jpg'
#file='MacleodsMorass_20171204_map.tif'

filepath = os.path.join(dir_pathIN, file)
filename, file_extension = os.path.splitext(filepath)
im = cv2.imread(filepath)
im = cv2.resize(im, (0,0), fx=0.5, fy=0.5)
        #easy assigments
hh='Hue High'
hl='Hue Low'
sh='Saturation High'
sl='Saturation Low'
vh='Value High'
vl='Value Low'

cv2.namedWindow('image')

# create trackbars for color change
# cv2.createTrackbar('R','image',0,255,nothing)
# cv2.createTrackbar('G','image',0,255,nothing)
# cv2.createTrackbar('B','image',0,255,nothing)

cv2.createTrackbar(hl, 'image',0,179,nothing)
cv2.createTrackbar(hh, 'image',0,179,nothing)
cv2.createTrackbar(sl, 'image',0,255,nothing)
cv2.createTrackbar(sh, 'image',0,255,nothing)
cv2.createTrackbar(vl, 'image',0,255,nothing)
cv2.createTrackbar(vh, 'image',0,255,nothing)

# create switch for ON/OFF functionality
# switch = '0 : OFF \n1 : ON'
# cv2.createTrackbar(switch, 'image',0,1,nothing)

# while(1):
#     cv2.imshow('image',im)
#     k = cv2.waitKey(1) & 0xFF
#     if k == 27:
#         break
#
#     # get current positions of four trackbars
#     r_h = cv2.getTrackbarPos('R','image')
#     g_s = cv2.getTrackbarPos('G','image')
#     b_v = cv2.getTrackbarPos('B','image')
#     s11 = cv2.getTrackbarPos(switch,'image')
#
#     if s11 == 0:
#         im[:] = 0
#     else:
#         im[:] = [b_v,g_s,r_h]
#
# ######hsv one

while(1):
    #_,frame=cap.read()
    #im=cv2.GaussianBlur(im,(5,5),0)
    #convert to HSV from BGR
    hsv=cv2.cvtColor(im, cv2.COLOR_BGR2HSV)


    #read trackbar positions for all
    hul=cv2.getTrackbarPos(hl, 'image')
    huh=cv2.getTrackbarPos(hh, 'image')
    sal=cv2.getTrackbarPos(sl, 'image')
    sah=cv2.getTrackbarPos(sh, 'image')
    val=cv2.getTrackbarPos(vl, 'image')
    vah=cv2.getTrackbarPos(vh, 'image')
    #make array for final values
    HSVLOW=np.array([hul,sal,val])
    HSVHIGH=np.array([huh,sah,vah])

    #apply the range on a mask
    mask = cv2.inRange(hsv,HSVLOW, HSVHIGH)
    res = cv2.bitwise_and(im,im, mask =mask)

    cv2.imshow('image', res)
    cv2.imshow('yay', im)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break


cv2.destroyAllWindows()
