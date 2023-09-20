#!/usr/bin/env python3

import rospy
from visualization_msgs.msg import Marker

sun = Marker()

def init_sun():
    sun.header.frame_id = "sun"
    sun.header.stamp = rospy.Time.now()
    sun.id = 0
    sun.type = 2
    sun.action = 0
    sun.pose.position.x = 0   
    sun.pose.position.y = 0
    sun.pose.position.z = 0
    sun.pose.orientation.x = 0
    sun.pose.orientation.y = 0
    sun.pose.orientation.z = 0
    sun.pose.orientation.w = 1
    sun.scale.x = 2
    sun.scale.y = 2
    sun.scale.z = 2
    sun.color.r = 1.0
    sun.color.g = 1.0
    sun.color.b = 0.0
    sun.color.a = 1.0
    sun.lifetime = rospy.Duration(0)

def stop():
    rospy.loginfo("Stopping the sun")
    sun.action = 2

if __name__=='__main__':
    rospy.init_node("sun_marker")
    loop_rate = rospy.Rate(10)
    rospy.on_shutdown(stop)
    rospy.loginfo("Configuring the sun")

    init_sun()

    pub_sun = rospy.Publisher("/sun", Marker, queue_size=10)

    try:
        while not rospy.is_shutdown():
            sun.header.stamp = rospy.Time.now()
            pub_sun.publish(sun)
            loop_rate.sleep()
    except:
        pass