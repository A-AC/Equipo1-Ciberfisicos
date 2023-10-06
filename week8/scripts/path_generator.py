#!/usr/bin/env python
import rospy
import tf_conversions
from geometry_msgs.msg import Twist, Pose
import numpy as np
from week8.msg import instructions


points = rospy.get_param("/points")
times = rospy.get_param("/times")
LinearSpeedLimit = rospy.get_param("/LinearSpeedLimit")
AngularSpeedLimit = rospy.get_param("/AngularSpeedLimit")

print(points)
print(times)

message = instructions()

def calculate_points_new(points):
    vectorL = 1
    robot_angle = 0.0
    commands = []
    robot = [0.0, 0.0]
    robotV = [1.0, 0.0]
    point = [0.0, 0.0]

     # --- Follow a set of points ---
    for i in range(len(points)-1):

        # We calculate distance
        distx = points[i+1][0] - points[i][0]
        disty = points[i+1][1] - points[i][1]
        d = np.sqrt(distx*distx+disty*disty)

        point[0] = distx
        point[1] = disty

        robot[0] = points[i][0]
        robot[1] = points[i][1]

        robotV[0] = vectorL*np.cos(robot_angle) 
        robotV[1] = vectorL*np.sin(robot_angle)

        print(point)
        print(robot)
        print(robotV)
        

        angle = np.arccos(np.dot(robotV, point)/(np.sqrt((point[0]*point[0]) + (point[1]*point[1]))))

        cross = np.cross(robotV, point)
        print(cross)
        if cross < 0:
            angle = angle * -1.0

        elif cross > 0:
            angle = angle

        else:
            angle = 0.0

        robot_angle += angle 
        
        commands.append((0.0,((angle))))
        commands.append((d, 0.0))

        print("Sent Angle: " + str(angle))
        print("Sent Distance: " + str(d))
        print("")

    print(commands)
    return commands

        

def calculate_velocities(command, times):
    final_commands = []
    linearVel = 0.0
    angularVel = 0.0
    print(len(command))
    for x in range(0, len(command)):
        distance = command[x][0]
        time = times[x]
        linearVel = distance/time

        angle = command[x][1]
        angularVel = angle/time

        if angularVel > AngularSpeedLimit or angularVel < -1.0*AngularSpeedLimit or linearVel > LinearSpeedLimit or linearVel < -1.0*LinearSpeedLimit:
            print("ERROR ANGULAR OR LINEAR SPEED TOO FAST")
            return [[0.0, 0.0, -1.0]]

        final_commands.append([linearVel,angularVel,time])

    return final_commands
        


if __name__ == '__main__':
    pub = rospy.Publisher("/pose", instructions, queue_size=1)
    rospy.init_node("path_generator")
    rate = rospy.Rate(100)

    commands = calculate_points_new(points)
    print(commands)

    messages = calculate_velocities(commands, times)
    print(messages)

    count = 0
    lastTime = 0.0
    done = 1

    initialTime = rospy.get_time()
    while not rospy.is_shutdown():
        currentTime = rospy.get_time()

        if messages[0][2] < 0.0:
            print("ERROR LINEAR OR ANGULAR SPEED IS TO HIGH")
        else:

            if (currentTime-initialTime >= lastTime) and done == 1:
                print(count)
                print("SENDING...")
                message.linearVel = messages[count][0]
                message.angularVel = messages[count][1]
                lastTime = messages[count][2]
                message.time = lastTime
                initialTime = currentTime

                pub.publish(message)
                count += 1

            if count >= len(messages):
                done = 0

                if (currentTime-initialTime >= lastTime):
                    print("DONE")
                    message.linearVel = 0.0
                    message.angularVel = 0.0
                    message.time = 0.0

                    pub.publish(message)
                    print(message)


        rate.sleep()
