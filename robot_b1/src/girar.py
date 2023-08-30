#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist

PI = 3.1416

def rotate():
    rospy.init_node('robotB1', anonymous=True)
    velocity_pub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=1)
    vel_msg = Twist()
    print("Girando el robot B1")

    vel = int(input("Ingresa la velocidad: "))
    ang = int(input("Ingresa el angulo: "))
    dir = int(input("Ingrea la dirección: "))

    ang_vel = vel*2*PI/360
    real_ang = ang*2*PI/360

    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0

    if dir == 1:
        vel_msg.angular.z = -abs(ang_vel)
    else:
        vel_msg.angular.z = abs(ang_vel)

    while not rospy.is_shutdown():
        t0 = rospy.Time.now().to_sec()
        actual_ang = 0

        while actual_ang < real_ang:
            velocity_pub.publish(vel_msg)
            t1 = rospy.Time.now().to_sec()

            actual_ang = ang_vel*(t1-t0)
        
        vel_msg.angular.z = 0
        velocity_pub.publish(vel_msg)

if __name__=='__main__':
    try:
        rotate()
    except rospy.ROSInterruptException: pass