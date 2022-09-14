#!/usr/bin/python3

import rospy
import math
import traceback
import sys
import navi_goal_test1
import subprocess
import os
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseResult

rospy.init_node("Working_MODE")
rospy.loginfo("SimpleNavigationGoals Initialization")
rospy.loginfo("Initializations done")
nav_goals = navi_goal_test1.SimpleNavigationGoals()

def GO(x, y, theta):
    rospy.loginfo("Go to %0.1f, %0.1f, %0.1f", x, y, theta)

    if (nav_goals.go_to(x, y, theta)):
        print("Goal reached!")
        

def STOP():
    subprocess.run(['roslaunch mini_model emergency_stop.launch'], shell=True)
# def STOP():
#     os.system("rostopic pub -1 /move_base/cancel actionlib_msgs/GoalID -- {}")
    
def RESET():
    x = -0.5
    y = -5.2
    theta = 0
    rospy.loginfo("Go to %d, %d, %d", x, y, theta)
    if (nav_goals.go_to(x, y, theta)):
        print("Goal reached!")   
         
def movebase_client():
    global strings
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x =  float(strings[0])
    goal.target_pose.pose.position.y =  float(strings[1])
    goal.target_pose.pose.orientation.w = 1

    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!") 
    else:
        return client.get_result()


if __name__ == "__main__":
   
    try:
    # What to do if shut down (e.g. ctrl + C or failure)
        rospy.on_shutdown(nav_goals._shutdown)

    except rospy.ROSInterruptException:
        rospy.logerr(traceback.format_exc())
    rospy.loginfo("test terminated.")