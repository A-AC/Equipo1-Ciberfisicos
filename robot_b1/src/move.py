#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import math

def move():
    rospy.init_node('robotB1', anonymous=True)
    velocity_pub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=1)
    vel_msg = Twist()
    print("Moviendo el robot B1")

    vel_x = int(input("Ingresa la velocidad en x: "))
    vel_y = int(input("Ingresa la velocidad en y: "))
    dist = int(input("Ingresa la distancia: "))
    reverse = int(input("Hacia atrás? "))

    if reverse == 1:
        vel_msg.linear.x = -abs(vel_x)
        vel_msg.linear.y = -abs(vel_y)
    else:
        vel_msg.linear.x = abs(vel_x)
        vel_msg.linear.y = abs(vel_y)

    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0

    while not rospy.is_shutdown():
        t0 = rospy.Time.now().to_sec()
        actual_dist = 0

        while actual_dist < dist:
            velocity_pub.publish(vel_msg)
            t1 = rospy.Time.now().to_sec()
            dist_x = vel_x*(t1-t0)
            dist_y = vel_y*(t1-t0)
            actual_dist = math.sqrt((dist_x*dist_x) + (dist_y*dist_y))
        
        vel_msg.linear.x = 0
        vel_msg.linear.y = 0
        velocity_pub.publish(vel_msg)

if __name__=='__main__':
    try:
        move()
    except rospy.ROSInterruptException: pass