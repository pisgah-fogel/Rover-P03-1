import cv2

def getStarBoundary(interx, intery, image, threshold, debugimg):
    """
    interx, intery: position of a point of interest ie, a point inside a star
    image: a grayscale image
    threshold: while the pixel value is above the threshold we are inside the star
    return the xmin, xmax, ymin, ymax containing the star
    """
    if interx + 20 >= len(image[0]) or intery + 20 >= len(image):
        return (interx, interx, intery, intery)

    x = interx
    y = intery
    # find top (y small)
    for i in range(20):
        if image[y-1][x] > threshold:
            y -= 1
        elif image [y-1][x-1] > threshold:
            y -= 1
            x -= 1
        elif image [y-1][x+1] > threshold:
            y -= 1
            x += 1
        else:
            break
    ymin = y # top of the star = y min

    x = interx
    y = intery
    # find bottom (y big)
    for i in range(20):
        if image[y+1][x] > threshold:
            y += 1
        elif image [y+1][x-1] > threshold:
            y += 1
            x -= 1
        elif image [y+1][x+1] > threshold:
            y += 1
            x += 1
        else:
            break
    ymax = y # top of the star = y min

    x = interx
    y = intery
    # find left (x small)
    for i in range(20):
        if image[y][x-1] > threshold:
            x -= 1
        elif image [y-1][x-1] > threshold:
            y -= 1
            x -= 1
        elif image [y+1][x-1] > threshold:
            y += 1
            x -= 1
        else:
            break
    xmin = x

    x = interx
    y = intery
    # find right (x big)
    for i in range(20):
        if image[y][x+1] > threshold:
            x += 1
        elif image [y-1][x+1] > threshold:
            y -= 1
            x += 1
        elif image [y+1][x+1] > threshold:
            y += 1
            x += 1
        else:
            break
    xmax = x

    #print("Star xmin ", xmin, "xmax", xmax)
    #print("Star ymin ", ymin, "ymax", ymax)
    cv2.rectangle(debugimg, (xmin, ymin), (xmax, ymax), (0, 255, 0))

    #starcenter = (xmin + (xmax-xmin)/2, ymin + (ymax-ymin)/2)

    return (xmin, xmax, ymin, ymax)

def imageAvg(image):
    """
    image: a black and white image
    return the average pixel value of the image
    """
    sum = 0
    imgw = len(image[0])
    imgh = len(image)
    for x in range(imgw):
        for y in range(imgh):
            sum += image[y][x]
    avg = sum/(imgw*imgh)
    print('Average pixel value is: ', avg)
    return avg

def pointAlreadyRegistered(register, x, y):
    for boundary in register:
        if x + 1 >= boundary[0] and x - 1 <= boundary[1] and y + 1 >= boundary[2] and y - 1 <= boundary[3]:
            return boundary[3] - boundary[2]
    return -1

def findStars(image, threshold, debugimg):
    """
    image: black and white image
    threshold: minimum pixel value to consider it as a star, you can use imageAvg(image)
    """
    imgw = len(image[0])-1
    imgh = len(image)-1
    count = 0
    stars = []

    # For debug purpose only
    for x in range(imgw):
        for y in range(imgh):
            if image[y][x] > 10*threshold:
                debugimg[y, x] = (0, 0, 255) # B G R

    # Real stuff
    for x in range(imgw):
        for y in range(imgh):
            if image[y][x] > 10*threshold:
                count += 1
                reg = pointAlreadyRegistered(stars, x, y)
                if reg == -1:
                    tmp = getStarBoundary(x, y, image, threshold, debugimg)
                    stars.append(tmp)
                    y += tmp[3] - tmp[2] # Jump over the star
                    starcenter = boxToPosition(tmp)
                    print("Star center at ", starcenter[0], " ", starcenter[1])
                    debugimg[int(starcenter[1]), int(starcenter[0])] = (255, 255, 255)
                else:
                    y += reg + 1  # jump over the already registered star

    print('Number of pixels the 10x average value: ', count, " / ", imgw*imgh)
    print('Number of stars: ', len(stars))
    return stars

def boxToPosition(box):
    """
    box[0] min x
    box[1] max x
    box[2] min y
    box[3] max y
    return star middle position (x, y)
    """
    return (box[0] + (box[1]-box[0])/2, box[2] + (box[3]-box[2])/2)

def boxToWeightPosition(box, image):
    pass # TODO

def findStarNewBox(oldbox, image, threshold, debugimg, distance):
    xmin = oldbox[0]
    xmax = oldbox[1]
    ymin = oldbox[2]
    ymax = oldbox[3]
    for x in range(xmin-distance, xmax+distance):
        for y in range(ymin-distance, ymax+distance):
            if image[y][x] > 10*threshold:
                tmp = getStarBoundary(x, y, image, threshold, debugimg)
                starcenter = boxToPosition(tmp)
                debugimg[int(starcenter[1]), int(starcenter[0])] = (255, 255, 255)
                return tmp
    return (0,0,0,0)