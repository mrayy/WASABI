

import almath
import time
import argparse
import socket
import math
import thread

from contextlib import closing
from naoqi import ALProxy


bufsize = 2048
PORT_CONST_HEAD_Action = 41000
AVG_WINDOW_SIZE=10
yaw=0
pitch=0

def clamp(n, smallest, largest): return max(smallest, min(n, largest))

class MovingAverage:
        def __init__(self,count):
                self.data=[]
                self.average=0
                self.count=count

        def add(self,v):
                self.data.append(v)
                if(len(self.data)>self.count):
                        del self.data[0]
                self.average=0
                for i in range(len(self.data)):
                        self.average=self.average+self.data[i]
                self.average=self.average/len(self.data)
                return self.average

				
def DataReceiver():
    global yaw
    global pitch
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    with closing(sock):
         sock.bind(("", PORT_CONST_HEAD_Action))
         while True:
             msg = sock.recv(bufsize)
#             print msg
             pitch1=-math.radians(float(msg.split(",")[1]))
             yaw1  =math.radians(float(msg.split(",")[0]))
             yaw  =clamp(yaw1,-math.pi,math.pi)
             pitch=clamp(pitch1,-math.pi,math.pi)
#            print(str(yaw)+","+str(pitch))



def main(robotIP, PORT = 9559):
    global yaw
    global pitch
    thread.start_new_thread(DataReceiver,())
    motion = ALProxy("ALMotion", robotIP, PORT)
    motion.setStiffnesses("Head", 1.0)
    #motion.setAngles(["HeadYaw"],1.0,1.0);
    avgYaw=MovingAverage(AVG_WINDOW_SIZE)
    avgPitch=MovingAverage(AVG_WINDOW_SIZE)
    while True:
        #print("************************* Head:"+msg)
        yaw2=avgYaw.add(yaw)
        pitch2=avgPitch.add(pitch)
#        print(str(pitch2) + " .. " + str(yaw2))
        motion.setAngles(["HeadYaw", "HeadPitch"], [yaw2,pitch2], 0.5)
        time.sleep(0.01)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")

    args = parser.parse_args()
    main(args.ip, args.port)

