# coding=utf-8
import glob, os
import numpy as np
import cv2

# Create ORB detector with 1000 keypoints with a scaling pyramid factor of 1.2
orb = cv2.ORB_create(1000, 1.2) # feature extration object
# Create Brute Force Matcher
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)


def drawMatches(img1, kp1, img2, kp2, matches):
    # Create a new output image that concatenates the two images together
    # (a.k.a) a montage
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')

    # Place the first image to the left
    out[:rows1,:cols1] = np.dstack([img1, img1, img1])

    # Place the next image to the right of it
    out[:rows2,cols1:] = np.dstack([img2, img2, img2])

    # For each pair of points we have between both images
    # draw circles, then connect a line between them
    for mat in matches:

        # Get the matching keypoints for each of the images
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        # x - columns
        # y - rows
        (x1,y1) = kp1[img1_idx].pt
        (x2,y2) = kp2[img2_idx].pt

        # Draw a small circle at both co-ordinates
        # radius 4
        # colour blue
        # thickness = 1
        cv2.circle(out, (int(x1),int(y1)), 4, (255, 0, 0), 1)   
        cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (255, 0, 0), 1)

        # Draw a line in between the two points
        # thickness = 1
        # colour blue
        cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255, 0, 0), 1)


    # Show the image
    cv2.imshow('Matched Features', out)
    cv2.waitKey(0)
    cv2.destroyWindow('Matched Features')

    # Also return the image if you'd like a copy
    return out

def calcMatchesPosition(img1, kp1, img2, kp2, matches):
    error_total_x = 0
    error_total_y = 0

    # para calcular a proporção da imagem
    pos1 = 0
    img1_idx = matches[pos1].queryIdx
    img2_idx = matches[pos1].trainIdx

    (pt1x1, pt1y1) = kp1[img1_idx].pt
    (pt1x2, pt1y2) = kp2[img2_idx].pt

    ratio_x = 0
    ratio_y = 0

    count_x = 0
    count_y = 0
    min_ratio = 0.1
    max_ratio = 10.0
    for pos2 in range(pos1 + 1, len(matches)):
        img1_idx2 = matches[pos2].queryIdx
        img2_idx2 = matches[pos2].trainIdx

        (pt2x1, pt2y1) = kp1[img1_idx2].pt
        (pt2x2, pt2y2) = kp2[img2_idx2].pt

        if (pt1x2 - pt2x2) != 0:
            ratio = (pt1x1 - pt2x1) / (pt1x2 - pt2x2)
            if ratio > min_ratio and ratio < max_ratio:
                ratio_x += ratio
                count_x += 1
        if (pt1y2 - pt2y2) != 0:
            ratio = (pt1y1 - pt2y1) / (pt1y2 - pt2y2)
            if ratio > min_ratio and ratio < max_ratio:
                ratio_y += ratio
                count_y += 1

    if count_x > 0:
        ratio_x /= count_x
    if count_y > 0:
        ratio_y /= count_y
    print('ratiox: ' + str(ratio_x))
    print('ratioy: ' + str(ratio_y))

    # para calcular o erro de posicionamento de cada ponto
    for pos1 in range(len(matches)-1):

        # Get the matching keypoints for each of the images
        img1_idx = matches[pos1].queryIdx
        img2_idx = matches[pos1].trainIdx

        (pt1x1,pt1y1) = kp1[img1_idx].pt
        (pt1x2,pt1y2) = kp2[img2_idx].pt

        error_x = 0
        error_y = 0
        for pos2 in range(pos1+1, len(matches)):
            img1_idx2 = matches[pos2].queryIdx
            img2_idx2 = matches[pos2].trainIdx

            (pt2x1, pt2y1) = kp1[img1_idx2].pt
            (pt2x2, pt2y2) = kp2[img2_idx2].pt

            error_x += np.fabs((pt1x1 - pt2x1) - ((pt1x2 - pt2x2) * ratio_x))
            error_y += np.fabs((pt1y1 - pt2y1) - ((pt1y2 - pt2y2) * ratio_y))

        error_x /= (len(matches)- (pos1+1))
        error_y /= (len(matches)- (pos1+1))

        error_total_x += error_x
        error_total_y += error_y
    return (error_total_x/ratio_x + error_total_y/ratio_y) / 2

clicks = []
def click_event(event, x, y, flags, params):
 
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
 
        # displaying the coordinates
        # on the Shell
        clicks.append((x,y))
        print(x, ' ', y)

def findMatchByFiles(img_filename1, img_filename2):
    img1 = cv2.imread(img_filename1, 0)
    img2 = cv2.imread(img_filename2, 0)
    return findMatch(img1, img2)

def findMatch(img1, img2):
    clicks.clear()
    print("RESULT2")
    print(img1.shape)
    #cv2.imshow('image',img)
    #cv2.waitKey(10000)
    img1 = cv2.resize(img1, (1920,1080))
    img2 = cv2.resize(img2, (1920,1080))
    #print(img.shape)
    
    #cv2.imshow('image',img1)
    #cv2.setMouseCallback('image', click_event)
    #cv2.waitKey(0)
    
    #mask = np.zeros(img1.shape[:2], dtype="uint8")
    #for i in range(0,len(clicks),2):
    #    cv2.rectangle(mask, clicks[i], clicks[i+1], 255, -1)

    print("LOG1")
    # Detect keypoints of original image
    #(kp1,des1) = orb.detectAndCompute(img1, mask)
    (kp1,des1) = orb.detectAndCompute(img1, None)
    (kp2,des2) = orb.detectAndCompute(img2, None)
    print("LOG2")

    # Do matching
    matches = bf.match(des1,des2)

    # Sort the matches based on distance.  Least distance
    # is better
    matches = sorted(matches, key=lambda val: val.distance, reverse=False)
    sum = 0
    total = len(matches)
    for num in range(0, total):
        print('matches: ' + str(matches[num].distance))
        sum += matches[num].distance
    if total > 0:
        sum /= total
    print('media: ' + str(sum))
    # Show only the top 10 matches - also save a copy for use later

    error = 0
    if total > 0:
        error = calcMatchesPosition(img1, kp1, img2, kp2, matches[0:total])
        print("ERROR: " + str(error))
        #drawMatches(img1, kp1, img2, kp2, matches[0:total])
    
    return error