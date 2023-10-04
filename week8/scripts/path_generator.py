#!/usr/bin/env python
import rospy
import tf_conversions
from geometry_msgs.msg import Twist, Pose
import numpy as np
from week8.msg import instructions


points = [(2.0, 0.0), (2.0, -2.0), (0.0, -2.0), (0.0, 0.0)]
times = [10,10, 10,10, 10,10]

message = instructions()

# Make points
def calculate_points(points):

    print("POINTS")
    print(points)
    vectorL = 1
    robot_angle = 0.0
    commands = []

    # --- Follow a set of points ---
    for i in range(len(points)-1):
        # Distance
        distx = points[i+1][0] - points[i][0]
        disty = points[i+1][1] - points[i][1]
        b = np.sqrt(distx*distx+disty*disty)

        robotx = points[i][0]
        roboty = points[i][1]

        newpointx = vectorL*np.cos(robot_angle) + robotx
        newpointy = vectorL*np.sin(robot_angle) + roboty

        print("New point: x(" + str(newpointx) + "), y(" + str(newpointy)+ ")")

        distx2 = newpointx-points[i+1][0]
        disty2 = newpointy-points[i+1][1]
        a = np.sqrt(distx2*distx2 + disty2*disty2)

        print("a: "+str(a))
        c = vectorL
        print("c: " + str(c))
        print("b: " + str(b))

        op = (b*b+c*c-a*a)/(2*b*c)
        print("op: " + str(round(op,14)))
        op = round(op,14)
        
        angle = np.arccos(op)
        print("angle: "+ str(angle))
        print("robotangle: "+str(robot_angle))

        # Check which side to choose
        """
        testPointX = b*np.cos(robot_angle)*np.cos(angle) - b*vectorL*np.sin(robot_angle)*np.sin(angle) + robotx
        testPointY = b*np.cos(robot_angle)*np.sin(angle) + b*vectorL*np.sin(robot_angle)*np.cos(angle) + roboty

        print("Test point: x(" + str(testPointX) + "), y(" + str(testPointY)+ ")")

        if (testPointX < points[i+1][0]+1 and testPointX > points[i+1][0]-1 )and (testPointY < points[i+1][1]+1 and testPointY > points[i+1][1]-1):
            print("First try :)")      
        else:
            print("Not right one")
            angle = 2.0*np.pi-angle
        """
            
        commands.append((0.0,((angle))))
        commands.append((b, 0.0))
        print("Sent Angle: " + str(angle))
        print("Sent Distance: " + str(b))
        print("")
        robot_angle += angle

        print(commands)

    return commands

def calculate_velocities(command, times):
    final_commands = []
    for x in range(0, len(command)):
        distance = command[x][0]
        time = times[x]
        linearVel = distance/time

        angle = command[x][1]
        angularVel = angle/time

        final_commands.append([linearVel,angularVel,time])

    return final_commands
        


if __name__ == '__main__':
    pub = rospy.Publisher("/pose", instructions, queue_size=1)
    rospy.init_node("path_generator")
    rate = rospy.Rate(100)

    commands = calculate_points(points)

    messages = calculate_velocities(commands, times)
    print(messages)

    count = 0
    lastTime = 0.0
    done = False

    initialTime = rospy.get_time()
    while not rospy.is_shutdown():
        currentTime = rospy.get_time()

        if (currentTime-initialTime > lastTime) and not(done):
            print("SENDING...")
            initialTime = currentTime
            currentTime += lastTime
            message.linearVel = messages[count][0]
            message.angularVel = messages[count][1]
            lastTime = messages[count][2]
            message.time = lastTime

            pub.publish(message)
            count += 1

        if count >= len(messages):
            message.linearVel = 0.0
            message.angularVel = 0.0
            message.time = 0.0
            done = True

            pub.publish(message)


        rate.sleep()
