
import sys
import time
import os
import subprocess
import headController
import armController
import thread

from naoqi import ALProxy
from subprocess import call

robotIP="127.0.0.1"

def HeadProcessing():
   headController.main(robotIP,9559)

def BodyProcessing():
   armController.main(robotIP,9559)

def PepperStreamer(targetIP):
   os.system("./pepperStreamer.sh "+targetIP)

def main(targetIP):
  # Create proxy to ALBehaviorManager

  #  detection=ALProxy("ALFaceDetection",robotIP,9559)
  #  detection.setRecognitionEnabled(False)
  #  perception=ALProxy("ALPeoplePerception",robotIP,9559)
  #  auton=ALProxy("ALAutonomousMoves",robotIP,9559)
  #  auton.setExpressiveListeningEnabled(False)
   # auton.setBackgroundStrategy("none")
  #  vision=ALProxy("ALVideoDevice",robotIP,9559)
  #  vision.stopCamera(0)
    auton=ALProxy("ALAutonomousLife",robotIP,9559)
    print auton.getState()
    if auton.getState()!='disabled':
        auton.setState("disabled")
        auton.stopAll()
    motion=ALProxy("ALMotion",robotIP,9559)
    motion.wakeUp()
    awareness=ALProxy("ALBasicAwareness",robotIP,9559)
    awareness.stopAwareness()
    audio=ALProxy("ALAudioDevice",robotIP,9559)
    audio.setOutputVolume(100)

#    time.sleep(5)
#    subprocess.Popen(["python","headController.py"])
    thread.start_new_thread(HeadProcessing,())
    thread.start_new_thread(PepperStreamer,(targetIP,))
    thread.start_new_thread(BodyProcessing,())
#    call("#!/bin/bash pepperStreamer.sh "+targetIP,shell=True)
 #   os.system("pepperStreamer.sh "+ targetIP)
    while 1:
      pass
	  
if __name__ == "__main__":

  if (len(sys.argv) < 2):
    print "Usage python albehaviormanager_example.py targetIP"
    sys.exit(1)

  main(sys.argv[1])
