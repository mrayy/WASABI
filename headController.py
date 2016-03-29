
import almath
import time
import argparse
import socket
import math
from contextlib import closing
from naoqi import ALProxy


bufsize = 2048
PORT_CONST_HEAD_Action = 41000
AVG_WINDOW_SIZE=10

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

def main(robotIP, PORT = 9559):
    motion = ALProxy("ALMotion", robotIP, PORT)
    motion.setStiffnesses("Head", 1.0)
    #motion.setAngles(["HeadYaw"],1.0,1.0);
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    avgYaw=MovingAverage(AVG_WINDOW_SIZE)
    avgPitch=MovingAverage(AVG_WINDOW_SIZE)
    with closing(sock):
         sock.bind(("", PORT_CONST_HEAD_Action))
         while True:
             msg = sock.recv(bufsize)
             #print("************************* Head:"+msg)
             pitch=-math.radians(float(msg.split(",")[1]))
             yaw  =math.radians(float(msg.split(",")[0]))
             pitch=clamp(pitch,-math.pi,math.pi)
             yaw  =clamp(yaw,-math.pi,math.pi)
#            yaw=avgYaw.add(yaw)
#            pitch=avgPitch.add(pitch)
#             print(str(pitch) + " .. " + str(yaw))
             motion.setAngles(["HeadYaw", "HeadPitch"], [yaw,pitch], 0.3)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")

    args = parser.parse_args()
    main(args.ip, args.port)

