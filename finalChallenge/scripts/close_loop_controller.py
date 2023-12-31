#!/usr/bin/env python
import rospy
import tf_conversions
from geometry_msgs.msg import Twist, Pose
from std_msgs.msg import Int16, Float32
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import numpy as np
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu

command = Twist()
#imu_rec = Imu()
poseRobot = Pose()
points = rospy.get_param("/points")
linear_vel_max = rospy.get_param("/linear_vel_max")
angular_vel_max = rospy.get_param("/angular_vel_max")
linear_vel_min = rospy.get_param("/linear_vel_min")
angular_vel_min = rospy.get_param("/angular_vel_min")
points_poses = []
print(points)
superError1 = 0.0
superError2 = 0.0
currentTime = 0.0
prevTime = 0.0
arm_status = 0
prevAngle = 0.0

def get_arm_status(msg):
    global arm_status
    arm_status = msg.data

def generate_poses():
    global points
    pointsPoses = []

    for x in points:
        poseA = Pose()
        poseA.position.x = x[0]
        poseA.position.y = x[1]
        if x[2] == "N":
            poseA.orientation.z = "N"
        else:
            poseA.orientation.z = x[2][0]*(np.pi/180.0)
            poseA.orientation.x = x[2][1]

        print(poseA.orientation.z)
        pointsPoses.append(poseA)

    
    return pointsPoses

def get_angle_robot_and_point(robot_orientation,robot_position, points_poses, current_point):
    vectorL = 1
    robotV = [0.0, 0.0]
    point = [0.0,0.0]
    working_point = points_poses[current_point]

    robotV[0] = vectorL*np.cos(robot_orientation)
    robotV[1] = vectorL*np.sin(robot_orientation)

    point[0] = working_point.position.x - robot_position.position.x
    point[1] = working_point.position.y - robot_position.position.y

    print(robotV)
    print(point)

    angle = np.arccos(np.dot(robotV, point)/(np.sqrt((point[0]*point[0]) + (point[1]*point[1]))))

    cross = np.cross(robotV, point)
    if cross < 0:
        angle = angle * -1.0

    elif cross > 0:
        angle = angle

    else:
        angle = 0.0

    return angle

def wrap_to_system(angle, prevAngle):
    if angle > np.pi/2 and prevAngle < -np.pi/2:
        return angle-2*np.pi
    elif angle < -np.pi/2 and prevAngle > np.pi/2:
        return angle + 2*np.pi
    else:
        return angle

def get_angle_robot_and_orientation(robot_orientation, points_poses, current_point):
    vectorL = 1
    robotV = [0.0, 0.0]
    point = [0.0,0.0]
    working_point = points_poses[current_point]

    robotV[0] = vectorL*np.cos(robot_orientation)
    robotV[1] = vectorL*np.sin(robot_orientation)

    point[0] = vectorL*np.cos(working_point.orientation.z)
    point[1] = vectorL*np.sin(working_point.orientation.z)

    print(robotV)
    print(point)

    angle = np.arccos(np.dot(robotV, point)/(np.sqrt((point[0]*point[0]) + (point[1]*point[1]))))

    cross = np.cross(robotV, point)
    if cross < 0:
        angle = angle * -1.0

    elif cross > 0:
        angle = angle

    else:
        angle = 0.0

    return angle

def dist_poses(pose1, pose2):

    dist = np.sqrt((np.power((pose2.position.x - pose1.position.x), 2) + np.power((pose2.position.y - pose1.position.y), 2)))
    return dist

def get_odometry(msg):
    global poseRobot
    poseRobot = msg.pose.pose
    
def PID_Position(error):
    global currentTime
    global prevTime
    global superError1

    dt = currentTime-prevTime
    
    # P
    #Kp = rospy.get_param("Kp_Position", "No param found")
    #P = Kp*error
    P = 0.7*error

    # I
    superError1 += error * dt
    Ki = rospy.get_param("Ki_Position", "NO param found")
    I = superError1*0.0065

    # D
    #Kd = rospy.get_param("Kd_Position", "NO param found")
    #D = Kd*((error-prevError)/dt)
    D = 0.0

    #prevError = error

    return (P + I + D)

def PID_Orientation(error):
    global currentTime
    global prevTime
    global superError2

    dt = currentTime-prevTime
    
    # P
    #Kp = rospy.get_param("Kp_Orientation", "No param found")
    #P = Kp*error
    P = 0.0005*error

    # I
    superError2 += error * dt
    Ki = rospy.get_param("Ki_Orientation", "NO param found")
    I = superError2*0.006

    # D
    #Kd = rospy.get_param("Kd_Orientation", "NO param found")
    #D = Kd*((error-prevError)/dt)
    D = 0.0

    #prevError = error

    return (P + I + D) 


def init_command():
    global command
    command.linear.x = 0.0
    command.linear.y = 0.0
    command.linear.z = 0.0
    command.angular.x = 0.0
    command.angular.y = 0.0
    command.angular.z = 0.0

if __name__ == '__main__':
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    pub_smoother = rospy.Publisher("/smoother_cmd_vel", Twist, queue_size=10)
    arm_pub = rospy.Publisher("/start_arm", Int16, queue_size=1)
    # For Debug
    position_error_pub = rospy.Publisher("/controller/posError", Float32, queue_size=10)
    position_goal_pub = rospy.Publisher("/controller/posGoal", Float32, queue_size=10)
    position_real_pub = rospy.Publisher("/controller/posReal", Float32, queue_size=10)
    orientation_error_pub = rospy.Publisher("/controller/orientError", Float32, queue_size=10)
    orientation_goal_pub = rospy.Publisher("/controller/orientGoal", Float32, queue_size=10)
    orientation_real_pub = rospy.Publisher("/controller/orientReal", Float32, queue_size=10)

    rospy.Subscriber("/odom", Odometry, get_odometry)
    rospy.Subscriber("/done_arm", Int16, get_arm_status)
    rospy.init_node("close_loop_controller")
    rate = rospy.Rate(100)

    init_command()
    points_poses = generate_poses()
    current_point = 0
    current_state = 0
    new_robot_orientation = 0.0
    prev_position = Pose()
    angular_vel = 0.0
    prevTime = 0.0
    arm_status = 0
    dist_error =0.0
    dist_goal=0.0
    angle_goal =0.0
    angle_error =0.0
    dist_real =0.0

    while not rospy.is_shutdown():
        
        robot_position = poseRobot
        #(x, y, robot_orientation) = euler_from_quaternion([imu_rec.orientation.x, imu_rec.orientation.y, imu_rec.orientation.z, imu_rec.orientation.w])
        (x, y, robot_orientation) = euler_from_quaternion([poseRobot.orientation.x, poseRobot.orientation.y, poseRobot.orientation.z, poseRobot.orientation.w])
        robot_orientation = wrap_to_system(robot_orientation, prevAngle)

        currentTime = rospy.get_time()
        print("Current Point: ", current_point)

        # publish errors and goals to see graphs
        position_error_pub.publish(dist_error)
        position_goal_pub.publish(dist_goal)
        position_real_pub.publish(dist_real)
        orientation_error_pub.publish(angle_error)
        orientation_goal_pub.publish(angle_goal)
        orientation_real_pub.publish(robot_orientation)

        if current_state == 0:
            print("NEXT POINT")
            if current_state >= len(points_poses):
                print("DONE")
            else:
                current_point += 1
                arm_status = 0
                current_state = 1
                superError1 = 0.0
                superError2 = 0.0
            prevAngle = robot_orientation
            new_robot_orientation = robot_orientation
            
        
        elif current_state == 1:
            print("GETTING ANGLE")

            angle_indp = get_angle_robot_and_point(robot_orientation, robot_position, points_poses, current_point)
            angle_goal = new_robot_orientation + angle_indp

            current_state = 2
            

        elif current_state == 2:
            print("SETTING ANGLE")
            angle_error = angle_goal - robot_orientation
            angular_vel = PID_Orientation(angle_error)

            if np.abs(angular_vel) > angular_vel_max:
                if angular_vel > 0:
                    angular_vel = angular_vel_max
                else:
                    angular_vel = -1.0*angular_vel_max

            if np.abs(angular_vel) < angular_vel_min:
                if angular_vel > 0:
                    angular_vel = angular_vel_min
                else:
                    angular_vel = -1.0*angular_vel_min

            print("robot angle: ", robot_orientation)
            print("angle Goal: ", angle_goal)
            print("angle Error: ", angle_error)
            print("angular vel: ", angular_vel)

            if np.abs(angle_error) < 0.018:
                print("DONE")
                current_state = 3
                command.linear.x = 0.0
                command.angular.z = 0.0
                prev_position = robot_position
            else:

                command.linear.x = 0.0
                command.angular.z = angular_vel

        elif current_state == 3:
            print("GETTING DISTANCE")
            dist_goal = dist_poses(robot_position, points_poses[current_point])
            current_state = 4

        elif current_state == 4:
            print("MOVING")
            dist_real = dist_poses(robot_position, prev_position)

            dist_error = dist_goal - dist_real
            linear_vel = PID_Position(dist_error)*0.5

            if np.abs(linear_vel) > linear_vel_max:
                if linear_vel > 0:
                    linear_vel = linear_vel_max
                else:
                    linear_vel = -1.0* linear_vel_max

            if np.abs(linear_vel) < linear_vel_min:
                if linear_vel > 0:
                    linear_vel = linear_vel_min
                else:
                    linear_vel = -1.0* linear_vel_min

            print("robot dist: ", dist_real)
            print("dist Goal: ", dist_goal)
            print("dist Error: ", dist_error)
            print("linear vel: ", linear_vel)

            if np.abs(dist_error) < 0.02:
                print("DONE")
                if points_poses[current_point].orientation.z == "N":
                    current_state = 0
                else:
                    current_state = 5
                    superError2 = 0.0
                    new_robot_orientation = robot_orientation

                command.linear.x = 0.0
                command.angular.z = 0.0
            else:
                command.linear.x = linear_vel
                command.angular.z = 0.0


        elif current_state == 5:
            print("ADJUSTING GETTING ANGLE")

            angle_indp_adj = get_angle_robot_and_orientation(robot_orientation, points_poses, current_point)
            angle_goal_adj = new_robot_orientation + angle_indp_adj

            current_state = 6

        elif current_state == 6:
            print("ADJUSTING SETTING ANGLE")
            angle_error_adj = angle_goal_adj - robot_orientation
            angular_vel_adj = PID_Orientation(angle_error_adj)

            if np.abs(angular_vel_adj) > angular_vel_max:
                if angular_vel_adj > 0:
                    angular_vel_adj = angular_vel_max
                else:
                    angular_vel_adj = -1.0*angular_vel_max

            if np.abs(angular_vel_adj) < angular_vel_min:
                if angular_vel_adj > 0:
                    angular_vel_adj = angular_vel_min
                else:
                    angular_vel_adj = -1.0*angular_vel_min

            print("robot angle: ", robot_orientation)
            print("angle Goal: ", angle_goal_adj)
            print("angle Error: ", angle_error_adj)
            print("angular vel: ", angular_vel_adj)

            if np.abs(angle_error_adj) < 0.018:
                print("DONE")
                if points_poses[current_point].orientation.x == 0:
                   current_state = 0
                else:
                    current_state = 7
                command.linear.x = 0.0
                command.angular.z = 0.0
                prev_position = robot_position
                arm_pub.publish(points_poses[current_point].orientation.x)
                #pub.publish(command) #DELETE AFTER TESTING
                #x = input("NOW WHAT?") # DELETE AFTER TESTING
            else:

                command.linear.x = 0.0
                command.angular.z = angular_vel_adj

        elif current_state == 7:

            print("ARM ROUTINE")
            if arm_status == 1:
                print("WAITING")

            elif arm_status == 2:
                print("DONE ARM ROUTINE")
                current_state = 0


        prevTime = currentTime
        prevAngle = robot_orientation

        pub.publish(command)


        rate.sleep()
