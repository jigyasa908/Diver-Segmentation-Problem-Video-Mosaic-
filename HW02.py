'''
Author - Jigyasa Singh
This program performs video segmentation combined with region segmentation, and foreground integration.
The steps involved in the above-mentioned process are - 
1. Creating a background model using MOG2 function
2. The first 5 frames I added in the mosaic directly because as per my observation during background subtraction, the first few frames didn’t show significant change.
3. Performed morphological operations EROSION and CLOSING in order to detected the diver clearly
4. By keeping the track of the previous mask, I checked if it overlaps with the newly created mask.
5. If the overlapping is less than 0.005 I add the particular frame to the mosaic using the copyTo() function

'''


import numpy as np
import cv2

#Taking video as an input
cap = cv2.VideoCapture('/Users/jigyasasingh/Desktop/assign 2/IMG_1804__2175.m4v')

#Creating Kernels to perform morphological operations
kernel3 = np.ones([3,3], dtype=np.uint8)
kernel5 = np.ones([5,5], dtype=np.uint8)
kernel7 = np.ones([7,7], dtype=np.uint8)

# Get the Default resolutions
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

#Creating Background Subtraction for the video using MOG2
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
changemap = np.zeros([1280,720], dtype=np.uint8)

#out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

for i in range(6):
    if(cap.isOpened()):
        ret, frame = cap.read()
        fgmask = fgbg.apply(frame)
        mosaic = frame
#cv2.imshow('bg', mosaic)

while(cap.isOpened()):
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)

    #Performing Morphological operation - EROSION and CLOSING
    #fgmask = cv2.GaussianBlur(fgmask,(3,3),cv2.BORDER_DEFAULT)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_ERODE, kernel3)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel7)
    fgmask = cv2.medianBlur(fgmask, 3)
    if ret==True:
        tot = 1280 * 720

        #Calculating the overlap value using the binary operation - BITWISE AND
        overlap = float(np.count_nonzero(np.bitwise_and(changemap,fgmask))) / float(tot)
        #print(overlap)
        #The if loop below checks the overlapping value and adds it to the mosaic if the value is below 0.05
        if overlap < 0.002:
            changemap = np.bitwise_or(changemap, fgmask)
            mosaic = cv2.copyTo(frame, fgmask, mosaic)
        
        #va = cv2.copyTo(frame,fgmask)
        #cv2.imshow('nnn', va)
        cv2.imshow('frame',fgmask)
        #cv2.imshow('changemap',changemap)
        cv2.imshow('mosaic',mosaic)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
    else:
        break
#print(type(fgmask))    
# Release everything if job is finished
cap.release()
#out.release()
cv2.destroyAllWindows()