# How to launch camera

ls -al /dev/video*
gst-launch-1.0 v4l2src device=/dev/video4 ! video/x-raw,format=YUY2,width=1280,height=720 ! videoconvert ! xvimagesink sync=false
