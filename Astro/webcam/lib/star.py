def getStarBoundary(interx, intery, image, threshold):
    """
    interx, intery: position of a point of interest ie, a point inside a star
    image: a grayscale image
    threshold: while the pixel value is above the threshold we are inside the star
    return the xmin, xmax, ymin, ymax containing the star
    """
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
            y += 1
        elif image [y-1][x+1] > threshold:
            y -= 1
            x += 1
        elif image [y+1][x+1] > threshold:
            y += 1
            x += 1
        else:
            break
    xmax = x

    print("Star xmin ", xmin, "xmax", xmax)
    print("Star ymin ", ymin, "ymax", ymax)

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

def findStars(image, threshold):
    """
    image: black and white image
    threshold: minimum pixel value to consider it as a star, you can use imageAvg(image)
    """
    imgw = len(image[0])
    imgh = len(image)
    count = 0
    posstar = (0, 0)
    for x in range(imgw):
        for y in range(imgh):
            if image[y][x] > 10*threshold:
                count += 1
                #helpwin[y][x] = (255, 0, 0) # we could anotate an image for debugging purpose
                posstar = (x, y)
    print('Number of pixels the 10x average value: ', count, " / ", imgw*imgh)