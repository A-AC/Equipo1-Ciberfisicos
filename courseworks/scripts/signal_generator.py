#!/usr/bin/env python
import rospy
import numpy as np
from std_msgs.msg import Float32

if __name__ == '__main__':
    timePub = rospy.Publisher("time", Float32, queue_size=10)
    signalPub = rospy.Publisher("signal", Float32, queue_size=10)
    rospy.init_node("signal_generator")
    rate = rospy.Rate(10)


    while not rospy.is_shutdown():
        signal = np.sin(rospy.get_time())

        signalPub.publish(signal)
        timePub.publish(rospy.get_time())
        #message = "Time:  %s" % rospy.get_time()
        #message2 = "Signal:  %s" % signal
        #rospy.loginfo(message)
        #rospy.loginfo(message2)

        rate.sleep()