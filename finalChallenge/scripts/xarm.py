#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int16
import os
import time
import sys

dir = os. getcwd()
print(dir)
os.chdir(os.getcwd() + '/src/finalChallenge/scripts')
print(os.getcwd())
from xarm.wrapper import XArmAPI

os.chdir(dir)
print(dir)

status = 0

def callback(msg):
    global status
    status = msg.data

if __name__ == '__main__':
    rospy.init_node("xarm_routine")
    rospy.Subscriber("/start_arm", Int16, callback)
    pub = rospy.Publisher("/done_arm", Int16, queue_size=10)
    rate = rospy.Rate(10)

    try:
        ip = "192.168.31.198"
        arm = XArmAPI(ip)
    except:
        ip = input('Please input the xArm ip address:')
        arm = XArmAPI(ip)
        if not ip:
            print('input error, exit')
        
    
    arm.motion_enable(enable=True)
    arm.set_mode(0)
    arm.set_state(state=0)
    speed = 50


    while not rospy.is_shutdown():

        # Get object
        if status == 1:
            print("PICKUP")
            arm.set_servo_angle(angle=[-90.0, 21.8, -137.7, 115.8, -90], speed=speed, wait=True)
            print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
            arm.set_servo_angle(angle=[-90.0, 8.6, -103.5, 94.9, -90], speed=speed, wait=True)
            print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))

            rospy.sleep(2)
            arm.set_tgpio_digital(0, 1)
            time.sleep(0.5)
            rospy.sleep(2)

            arm.set_servo_angle(angle=[-90.0, 21.8, -137.7, 115.8, -90], speed=speed, wait=True)
            print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
            arm.set_servo_angle(angle=[-90.0, -51.6, -69.8, 121.4, -90], speed=speed, wait=True)
            print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))

            pub.publish(2)

        # Relase Objetc
        elif status == 2:
            print("RLEASE")

            arm.set_servo_angle(angle=[-90.0, 21.8, -137.7, 115.8, -90], speed=speed, wait=True)
            print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
            arm.set_servo_angle(angle=[-90.0, 8.6, -103.5, 94.9, -90], speed=speed, wait=True)
            print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))

            rospy.sleep(2)
            arm.set_tgpio_digital(0, 0)
            time.sleep(0.5)
            rospy.sleep(2)

            arm.set_servo_angle(angle=[-90.0, 21.8, -137.7, 115.8, -90], speed=speed, wait=True)
            print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
            arm.set_servo_angle(angle=[-90.0, -51.6, -69.8, 121.4, -90], speed=speed, wait=True)
            print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))

            pub.publish(2)
            

        # HOME
        elif status == 3:
            print("HOME")

            arm.set_servo_angle(angle=[-90.0, -51.6, -69.8, 121.4, -90], speed=speed, wait=True)
            print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))

            rospy.sleep(2)
            #arm.set_tgpio_digital(0, 0)
            #time.sleep(0.5)
            #rospy.sleep(2)

            pub.publish(2)

        status = 0
            

        rate.sleep()
