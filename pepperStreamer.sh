echo streaming to $1

 gst-launch-0.10 -v \
 v4l2src always-copy=false queue-size=5 device=/dev/video0 ! 'video/x-raw-yuv,width=640,height=480,framerate=30/1' ! \
 jpegenc quality=70 ! rtpjpegpay ! udpsink host=$1 port=9000  sync=false -v
 alsasrc ! audioconvert ! audioresample ! alawenc ! rtppcmapay ! udpsink host=$1 port=12345 sync=false \
 udpsrc port=9001 ! application/x-rtp,media=audio,clock-rate=48000,encoding-name=VORBIS,payload=96 ! \
                   rtpvorbisdepay ! vorbisdec ! volume volume=1 ! autoaudiosink sync=false

