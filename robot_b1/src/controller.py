#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import math
from std_msgs.msg import UInt16

kp = 0.005
dist_x = 0

def PID(error):
    return kp*error

def callback(msg):
    global dist_x
    dist_x = msg.data
    

def move():
    rospy.init_node('robotB1', anonymous=True)
    velocity_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    encoder = rospy.Subscriber('/Lencoder', UInt16, callback)
    vel_msg = Twist()
    print("Moviendo el robot B1")

    dist = int(input("Ingresa la distancia: "))

    entrada = 0

    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0

    while not rospy.is_shutdown():

        while dist_x < dist:
            error = dist-dist_x
            entrada = PID(error)
                
            vel_msg.linear.x = entrada
            print(vel_msg.linear.x)
            velocity_pub.publish(vel_msg)

        vel_msg.linear.x = 0
        velocity_pub.publish(vel_msg)

if __name__=='__main__':
    try:
        move()
    except rospy.ROSInterruptException: pass