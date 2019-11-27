# Raspberry Pi 0W

## Configuration

I use a Raspberry Pi 0W bought on 2018, with a debian based operating system on a 4Go Sandisk micro SD card.


The Raspberry is connected on the Mobile Host-Point (from my Android Phone).

## Stream video

### On the Raspberry pi
```
ffmpeg -f video4linux2 -r 15 -re -i /dev/video0 -preset ultrafast -vcodec libx264 -tune zerolatency -b 900k -f mpegts udp://<IP address>:1234
```

### On the Laptop
```
mpv udp://<IP address>:1234 --no-cache --untimed --no-demuxer-thread --video-sync=audio --vd-lavc-threads=1
```
Or
```
mplayer -demuxer mpegts udp://<IP address>:1234
```
