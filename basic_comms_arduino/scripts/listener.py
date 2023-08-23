#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

message = ""

def callback(msg):
    global message
    message = msg.data

if __name__ == '__main__':
    rospy.init_node('listener')
    rospy.Subscriber("chatter", String, callback)

    rate = rospy.Rate(100)

    while not rospy.is_shutdown():
        if int(message) > 28:
            rospy.loginfo("Estas lejos a: " + message + " cm")
        
        elif int(message) < 5:
            rospy.loginfo("Estas muy cerca a: " + message + " cm")

        else:
            rospy.loginfo("Distancia adecuada: " + message + " cm")

        rate.sleep()