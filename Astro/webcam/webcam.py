import cv2
import time
import matplotlib.pyplot as plt
import numpy as np
import math

from lib.star import imageAvg, boxToWeightPosition, findStarNewBox, boxToPosition, findStars

saveVideo = False
simulation = True
framecount = 0
state = 0

#Capture video from webcam
#vid_capture = cv2.VideoCapture(2) # Astro camera
#vid_capture = cv2.VideoCapture(0) # labtop camera

if saveVideo:
    vid_cod = cv2.VideoWriter_fourcc(*'XVID')
    output = cv2.VideoWriter("videos/cam_video.mp4", vid_cod, 20.0, (640,480))

# Graphs
y = []
for i in range(100):
    y.append(0)
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(y)
plt.ylim((-10,10))

stars = []
targetbox = (0, 0, 0, 0)

while(True):
    # Capture each frame of webcam video
    if not simulation:
        ret,frameold = vid_capture.read()
        frame = cv2.cvtColor(frameold, cv2.COLOR_BGR2GRAY)
        imgh = len(frame)
        imgw = len(frame[0])
    else:
        imgh = 500
        imgw = 500
        frame = np.zeros((imgh,imgw,1), np.uint8)
        cv2.circle(frame, (int(100 + 3*math.sin(framecount/10)), int(101 + 2*math.sin(framecount/17))), 2, (154), -1)
        cv2.circle(frame, (100, 201), 4, (203), -1)
        cv2.circle(frame, (200, 101), 3, (173), -1)

    # debug frame we can annotate
    debugimg = np.zeros((imgh,imgw,3), np.uint8)

    # Detect star
    diffx = 0
    diffy = 0
    if state == 0:
        avg = imageAvg(frame)
        if avg < 10:
            avg = 10
        stars = findStars(frame, avg, debugimg)
        
        if len(stars) > 0:
            targetbox = stars[1]
        elif len(stars) == 1:
            targetbox = stars[0]
        else:
            targetbox = (0, 0, 0, 0)
    else:
        newbox = findStarNewBox(targetbox, frame, avg, debugimg, 42)
        oldpos = boxToPosition(targetbox)
        newpos = boxToPosition(newbox)
        cv2.putText(debugimg, "x: "+str(newpos[0])+" y: "+str(newpos[1]), (50,20+4*30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
        diffx = newpos[0] - oldpos[0]
        diffy = newpos[1] - oldpos[1]

    cv2.putText(debugimg, "Threshold", (50,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
    cv2.putText(debugimg, "Star", (50,20+30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
    cv2.putText(debugimg, "Center", (50,20+2*30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

    #print("Pixel at (50, 50) - {}".format(v))
    #print(str(time.time_ns())+',' +str(v),  file=open('file.csv','a')) 

    # Plot datas:
    y.insert(0, math.sqrt(diffx**2+diffy**2))
    y.pop()
    line1.set_ydata(y)
    fig.canvas.draw()

    cv2.imshow("Video stream", frame)
    cv2.imshow('Debug', debugimg)
    if saveVideo:
        output.write(frame)
    # Close and break the loop after pressing "q" key
    val = cv2.waitKey(1)
    if val &0XFF == ord('q'):
        break
    elif val &0XFF == ord('n'):
        state += 1
    framecount += 1

# close the already opened camera
if not simulation:
    vid_capture.release()
if saveVideo:
    # close the already opened file
    output.release()
# close the window and de-allocate any associated memory usage
cv2.destroyAllWindows()