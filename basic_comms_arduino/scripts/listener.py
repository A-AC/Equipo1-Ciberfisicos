#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

message = ""

def callback(msg):
    global message
    message = msg.data

if __name__ == '__main__':
    rospy.init_node('listener')
    rospy.Subscriber("distance", String, callback)

    rate = rospy.Rate(100)

    while not rospy.is_shutdown():
        # Tank filling logic. the sensor is placed facing the water to calculate its lever, when the sensor reads a height of 5 cm: its full and needs
        # to stop, on the other hand if the sensor reads more than 28 cm: the tank is empty and needs to be filled. Anything between the values is fine.
        if int(message) > 28:
            rospy.loginfo("El tanque esta vacio, se debe llenar. Lectura: " + message + " cm")
        
        elif int(message) < 5:
            rospy.loginfo("El tanque esta lleno, se debe parar de llenar. Lectura: " + message + " cm")

        else:
            rospy.loginfo("El tanque esta adecuado, no hacer nada. Lectura: " + message + " cm")

        rate.sleep()