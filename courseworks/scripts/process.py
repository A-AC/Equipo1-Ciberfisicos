#!/usr/bin/env python
import rospy
import numpy as np
from std_msgs.msg import Float32

currentTime = 0.0
newSignal = 0.0
offset = np.pi


def callbackTime(msg):
    global currentTime
    currentTime = msg.data
    rospy.loginfo("Time %s", msg.data)

def callbackSignal(msg):
    if currentTime > 0.0:
        global newSignal
        newSignal = ((msg.data*np.cos(np.pi) + np.cos(currentTime)*np.sin(np.pi)) + 1)*0.5

        rospy.loginfo("Signal %s", msg.data)

def callbackProc(msg):
    rospy.loginfo("New Signal %s", msg.data)

if __name__ == '__main__':

    pub = rospy.Publisher("proc_signal", Float32, queue_size=10)
    rospy.init_node('process')


    rospy.Subscriber("time", Float32, callbackTime)
    rospy.Subscriber("signal", Float32, callbackSignal)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        pub.publish(newSignal)
        rospy.loginfo("New Signal %s", newSignal)
        rate.sleep()

    rospy.spin()
    
       