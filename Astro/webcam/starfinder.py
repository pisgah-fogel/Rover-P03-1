import cv2
import numpy as np

def getStarCenter(interx, intery, image):
    x = interx
    y = intery
    # find top (y small)
    for i in range(20):
        if image[y-1][x][0] == 255:
            y -= 1
        elif image [y-1][x-1][0] == 255:
            y -= 1
            x -= 1
        elif image [y-1][x+1][0] == 255:
            y -= 1
            x += 1
        else:
            break
    ymin = y # top of the star = y min

    x = interx
    y = intery
    # find bottom (y big)
    for i in range(20):
        if image[y+1][x][0] == 255:
            y += 1
        elif image [y+1][x-1][0] == 255:
            y += 1
            x -= 1
        elif image [y+1][x+1][0] == 255:
            y += 1
            x += 1
        else:
            break
    ymax = y # top of the star = y min

    x = interx
    y = intery
    # find left (x small)
    for i in range(20):
        if image[y][x-1][0] == 255:
            x -= 1
        elif image [y-1][x-1][0] == 255:
            y -= 1
            x -= 1
        elif image [y+1][x-1][0] == 255:
            y += 1
            x -= 1
        else:
            break
    xmin = x

    x = interx
    y = intery
    # find right (x big)
    for i in range(20):
        if image[y][x+1][0] == 255:
            y += 1
        elif image [y-1][x+1][0] == 255:
            y -= 1
            x += 1
        elif image [y+1][x+1][0] == 255:
            y += 1
            x += 1
        else:
            break
    xmax = x

    print("Star xmin ", xmin, "xmax", xmax)
    print("Star ymin ", ymin, "ymax", ymax)

    return (xmin + (xmax-xmin)/2, ymin + (ymax-ymin)/2)

image = cv2.imread('/home/phileas/Pictures/stacking/IMG_1154.JPG')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  
imgx = 1100
imgy = 0
imgw = 400
imgh = 400

crop = gray[imgy:imgy+imgh, imgx:imgx+imgw]
helpwin = np.zeros((imgh,imgw,3), np.uint8)

#cv2.rectangle(image, (imgx, imgy), (imgx+imgw, imgy+imgh), (255, 255, 255))
#cv2.imshow('Original image',image)
cv2.rectangle(gray, (imgx-1, imgy-1), (imgx+imgw, imgy+imgh), (255, 255, 255))
cv2.imshow('Original image',gray)

print(len(crop))
print(len(crop[0]))

sum = 0
for x in range(imgw):
    for y in range(imgh):
        sum += crop[y][x]
avg = sum/(imgw*imgh)
print('Average value is: ', avg)

count = 0
posstar = (0, 0)
for x in range(imgw):
    for y in range(imgh):
        if crop[y][x] > 10*avg:
            count += 1
            helpwin[y][x] = (255, 0, 0)
            posstar = (x, y)
print('Number of pixels the 10x average value: ', count, " / ", imgw*imgh)

print("Region of interrest at x:",posstar[0]," y:",posstar[1])
center = getStarCenter(posstar[0], posstar[1], helpwin)
cv2.circle(helpwin, (posstar[0], posstar[1]), 2, (0,0,255), -1)
cv2.circle(helpwin, (int(center[0]), int(center[1])), 2, (0,255,0), -1)

cv2.imshow('Gray image', crop)
cv2.imshow('Detected stars', helpwin)

cv2.waitKey(0)
cv2.destroyAllWindows()

