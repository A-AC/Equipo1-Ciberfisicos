#!/usr/bin/env python
import rospy
import tf_conversions
from geometry_msgs.msg import Twist, Pose
import numpy as np
from week8.msg import instructions

command = Twist()
timeToFinish = 0.0

def instruction_callback(msg):
    global linearVel
    global angularVel
    global timeToFinish
    linearVel = msg.linearVel
    angularVel = msg.angularVel
    timeToFinish = msg.time
    

def init_command():
    command.linear.x = 0.0
    command.linear.y = 0.0
    command.linear.z = 0.0
    command.angular.x = 0.0
    command.angular.y = 0.0
    command.angular.z = 0.0

if __name__ == '__main__':
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    rospy.Subscriber("/pose", instructions, instruction_callback)
    rospy.init_node("open_loop_controller")
    rate = rospy.Rate(100)

    init_command()

    initialTime = rospy.get_time()
    while not rospy.is_shutdown():
        currentTime = rospy.get_time()
        if currentTime-initialTime <= timeToFinish:
            command.linear.x = linearVel
            command.angular.z = angularVel
        else:
            command.linear.x = 0.0
            command.linear.z = 0.0
            initialTime = currentTime

        print("LinearVel", command.linear.x)
        print("AngularVel", command.angular.z)
        pub.publish(command)


        rate.sleep()
