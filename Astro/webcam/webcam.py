import cv2
import time
import matplotlib.pyplot as plt
import numpy as np

from lib.star import findStars
from lib.star import imageAvg

saveVideo = False
simulation = True

#Capture video from webcam
#vid_capture = cv2.VideoCapture(2) # Astro camera
vid_capture = cv2.VideoCapture(0) # labtop camera

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
plt.ylim((0,255))

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
        cv2.circle(frame, (100, 101), 2, (154), -1)
        cv2.circle(frame, (100, 201), 4, (203), -1)
        cv2.circle(frame, (200, 101), 3, (173), -1)

    # debug frame we can annotate
    debugimg = np.zeros((imgh,imgw,3), np.uint8)

    # Detect star
    avg = imageAvg(frame)
    findStars(frame, avg, debugimg)

    cv2.putText(debugimg, "Threshold", (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)

    #print("Pixel at (50, 50) - {}".format(v))
    #print(str(time.time_ns())+',' +str(v),  file=open('file.csv','a')) 

    # Plot datas:
    y.insert(0, frame[50, 50])
    y.pop()
    line1.set_ydata(y)
    fig.canvas.draw()

    cv2.imshow("Video stream", frame)
    cv2.imshow('Debug', debugimg)
    if saveVideo:
        output.write(frame)
    # Close and break the loop after pressing "q" key
    if cv2.waitKey(1) &0XFF == ord('q'):
        break
# close the already opened camera
vid_capture.release()
if saveVideo:
    # close the already opened file
    output.release()
# close the window and de-allocate any associated memory usage
cv2.destroyAllWindows()