#!/usr/bin/env python
# Author: Martin Leahy
# Date: 2018-01-01

## Aim:



## Import libraries: GDAL is critical for lat long and geotiff
import numpy as np
import os, time
import cv2, math

t0 = time.time()  # timing how long it takes
###______________________________________ PRELIM SETUP _________________________
##Paramaters:

#HSV thresholds
channel1MinRED = 160
channel1MaxRED = 255
channel2MinRED = 0
channel2MaxRED = 255
channel3MinRED = 0
channel3MaxRED =132

channel1MinPEN = 0
channel1MaxPEN = 40
channel2MinPEN = 0
channel2MaxPEN = 40
channel3MinPEN = 0
channel3MaxPEN = 40

AreaMinRED=50000 #pixel area is (width x length of pixels). This is min area of blobs that are kept, and considered Objects
AreaMaxRED=120000 #pixel area is (width x length of pixels). This is max area of blobs that are kept, and considered Objects

AreaMin=10 #pixel area is (width x length of pixels). This is min area of blobs that are kept, and considered Objects
AreaMax=60 #pixel area is (width x length of pixels). This is max area of blobs that are kept, and considered Objects

aspect_ratio_rot_box_MAX=1
aspect_ratio_rot_box_MIN=0.6

aspect_ratio_rot_box_RED_MIN=0.5
aspect_ratio_rot_box_RED_MAX=1.5
#RGB_threshold_forBinary=60 #The RGB level (0 to 255) that defines where the tree starts. ie like a contour of the blob. Depends how many bits 8 versus 1. Sometimes the input levels can vary ie 36-255 or 0-255.

dir_pathIN = '/home/martin/Documents/PYTHON/Golf_Card_Reader/images/phase2/'
dir_pathOUT = dir_pathIN


###_______________________________________END PRELIM SETUP ________________________

###______________________________________ START TIF FILE MAIN  LOOP_________________________
data_class_Object=[]
data_area = []
data_perimeter = []
data_extent = []
data_circularity = []
data_solidity = []
data_aspect_ratio_rot_box = []

FILES=os.listdir(dir_pathOUT)
TotObjects=0
print(dir_pathIN)
FILES=os.listdir(dir_pathIN)
for file in FILES: #MAIN FOR LOOP
    t = time.time()  # timing how long it takes. single image around 2mins for just the thresholding and writing ot _raster
    if file.endswith('golf_scores_N2_marked.jpg'):   #  THESE ARE THE RAW IMAGES..... for binary then it would be if file.endswith('_binary.tif'):
        print file

        filepath=os.path.join(dir_pathOUT, file)
        filename, file_extension = os.path.splitext(filepath)
        ## Read the tiled tif file and convert to 3 channels 3rd dim 1 ie R, G, B
        # Read image
        im = cv2.imread(os.path.join(dir_pathIN, file)) #could use , cv2.IMREAD_UNCHANGED to see of that affects the trnsparency  white background
        im_copy=im

        AY = len(im)
        AX = len(im[0])
        Object_Array=np.zeros((AY, AX))

        # hsv = cv2.cvtColor(im_denoise, cv2.COLOR_BGR2HSV)         # Convert BGR to HSV
        rgb= cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        #px = rgb[500, 2200]
        #print rgb
        #ball = rgb[280:340, 330:390]
        # define range of blue color in HSV
        lower_RED = np.array([channel1MinRED, channel2MinRED, channel3MinRED])
        upper_RED = np.array([channel1MaxRED, channel2MaxRED, channel3MaxRED])
        lower_PEN = np.array([channel1MinPEN, channel2MinPEN, channel3MinPEN])
        upper_PEN = np.array([channel1MaxPEN, channel2MaxPEN, channel3MaxPEN])

        # Threshold the HSV image to get only blue colors
        maskRED = cv2.inRange(rgb, lower_RED, upper_RED)
        maskPEN = cv2.inRange(rgb, lower_PEN, upper_PEN)
        # Bitwise-AND mask and original image
        resRED = cv2.bitwise_and(im, im, mask=maskRED)
        resPEN = cv2.bitwise_and(im, im, mask=maskPEN)



######################### RED - START

        inv_openingRED = cv2.bitwise_not(maskRED)
        retRED, threshRED = cv2.threshold(maskRED, 125, 255, 0)
        _, contoursRED, _ = cv2.findContours(threshRED, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        ##################START DEFINE CONTOURS ########################################
        contours_areaRED = []
        contours_NOT_ObjectsRED = []  # These are the contours which are either too big or too small to be Objects
        contours_ObjectsRED = []
        for con in contoursRED:  # calculate area and filter into new array
            area = cv2.contourArea(con)
            if AreaMinRED < area < AreaMaxRED:
                contours_areaRED.append(con)
            else:
                contours_NOT_ObjectsRED.append(con)

        for con in contours_areaRED:  # check the rotated box aspect ratio
            rect = cv2.minAreaRect(con)
            # box = cv2.boxPoints(rect)
            # box = np.int0(box)
            center = rect[0]
            size = rect[1]
            angle = rect[2]
            w = size[0]
            h = size[1]
            if h == 0:
                break
            aspect_ratio_rot_box = float(w) / h
            # print 'aspect_ratio =', aspect_ratio_rot_box
            if aspect_ratio_rot_box > aspect_ratio_rot_box_RED_MIN or aspect_ratio_rot_box < aspect_ratio_rot_box_RED_MAX:
                contours_ObjectsRED.append(con)

            else:
                contours_NOT_ObjectsRED.append(con)  # add the Objects contours which are in OK area range, but not circular enough
        # print contours_ObjectsPEN
        # cv2.drawContours(im_copy, contours_ObjectsPEN, -1, (0, 255, 0), 3)
            cv2.drawContours(im, contours_ObjectsRED, -1, (0, 255, 0), 1)
        cv2.imshow('maskRED', maskRED)
        cv2.imshow('im contours', im)
        cv2.waitKey()
        NoObjectsRED = len(contours_ObjectsRED)

        ######### fit rectnage

        for con in contours_ObjectsRED:
            rect = cv2.boundingRect(con)
            cv2.rectangle(im_copy, (rect[0], rect[1]), (rect[2] + rect[0], rect[3] + rect[1]), (0, 255, 0), 2)
            print rect[0],rect[1],rect[2] + rect[0],rect[3] + rect[1]
        cv2.imshow('im  rect ', im_copy)
        cv2.waitKey()

        ######################### RED - END

        #kernel = np.ones((5, 5), np.uint8)
        #erosion = cv2.erode(mask, kernel, iterations=1)
        #opening = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel)
        #closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        #cv2.imshow('resRED', rgb)

        #cv2.imshow('resPEN', resPEN)
        #cv2.imshow('im', im)
        #cv2.imshow('maskRED', maskRED)
        #cv2.imshow('maskPEN', maskPEN)
        #cv2.waitKey()

        #These need to be calculated in this version
        shift_Y=9
        shift_X=10
        Pix_X=726
        Pix_Y=136
        len_X=30
        len_Y=20
        top = Pix_Y-len_Y-shift_Y
        left = Pix_X-len_X-shift_X

        hole=0
        TotScore9holes=0
        for i in range(9): #Loop over holes 1 to 9 - and find scores from 1 to 9 plus W for Wipe
            score=0
            #left = left + (len_Y + shift_Y)
            #right = left + len_Y

            top= top+ (len_Y + shift_Y)
            bottom = top+ len_Y

            left = Pix_X - len_X - shift_X

            #top = Pix_X - len_X - shift_X
            hole = i + 1

            for j in range(10): # Loop over possible scores for each hole
                score=score+1
                #print 'hole, score',hole, score
                left=left+(len_X+shift_X)
                #bottom=top+len_X
                right = left + len_X
                #print left, right, top, bottom,hole, score
                subset_rgb=rgb[top:bottom,left:right]
                subset_im= im[top:bottom,left:right]
                AY_subset = len(subset_rgb)
                AX_subset = len(subset_rgb[0])
                maskPEN_subset_rgb = cv2.inRange(subset_rgb, lower_PEN, upper_PEN)
                resPEN_subset_rgb = cv2.bitwise_and(subset_im, subset_im, mask=maskPEN_subset_rgb) # dont really need this`

                #inv_openingRED = cv2.bitwise_not(maskRED)
                #retRED, threshRED = cv2.threshold(inv_openingRED, 125, 255, 0)
                #_, contoursRED, _ = cv2.findContours(threshRED, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                #inv_openingPEN = cv2.bitwise_not(maskPEN_subset_rgb)
                retPEN, threshPEN = cv2.threshold(maskPEN_subset_rgb, 125, 255, 0)
                _, contoursPEN, _ = cv2.findContours(threshPEN, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                ##################START DEFINE CONTOURS ########################################
                contours_areaPEN = []
                contours_NOT_ObjectsPEN = []  # These are the contours which are either too big or too small to be Objects
                contours_ObjectsPEN = []
                for con in contoursPEN:  # calculate area and filter into new array
                    area = cv2.contourArea(con)
                    if AreaMin < area < AreaMax:
                        contours_areaPEN.append(con)
                    else:
                        contours_NOT_ObjectsPEN.append(con)


                for con in contours_areaPEN:  # check the rotated box aspect ratio
                    rect = cv2.minAreaRect(con)
                    # box = cv2.boxPoints(rect)
                    # box = np.int0(box)
                    center = rect[0]
                    size = rect[1]
                    angle = rect[2]
                    w = size[0]
                    h = size[1]
                    if h == 0:
                        break
                    aspect_ratio_rot_box = float(w) / h
                    # print 'aspect_ratio =', aspect_ratio_rot_box
                    if aspect_ratio_rot_box < aspect_ratio_rot_box_MIN or aspect_ratio_rot_box > aspect_ratio_rot_box_MAX:
                        offset=[]
                        offset=[left, top]
                        contours_ObjectsPEN.append(con)
                        AY_cont = len(contours_ObjectsPEN[0])

                        if(j==9):
                            scoreText='Wipe'
                        else:
                            scoreText = "%2.0f" % score
                            TotScore9holes +=score

                        print 'Score on hole ', hole, 'is ', scoreText
                        #print left, right, top, bottom,hole, score
                        #cv2.imshow('maskPEN_subset_rgb', maskPEN_subset_rgb)
                        #cv2.waitKey()

                        # just loop and add the offset
                        for i in range(0,AY_cont):

                            contours_ObjectsPEN[0][i][0][0]  =  contours_ObjectsPEN[0][i][0][0] + left
                            contours_ObjectsPEN[0][i][0][1]  =  contours_ObjectsPEN[0][i][0][1] + top
                    else:
                        contours_NOT_ObjectsPEN.append(con)  # add the Objects contours which are in OK area range, but not circular enough
                #print contours_ObjectsPEN
                #cv2.drawContours(im_copy, contours_ObjectsPEN, -1, (0, 255, 0), 3)

                NoObjects = len(contours_ObjectsPEN)
                TotObjects+=NoObjects

                #print NoObjects
                #cv2.imshow('image_Contours', im_copy)
                #cv2.waitKey()
print 'Total No objects=',TotObjects
print 'Total Score 9 holes =',TotScore9holes
elapsed = time.time() - t0
print 'time taken (TOTAL): (seconds)',elapsed
