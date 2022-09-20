#!/usr/bin/python3

import rospy
import math
import traceback
import sys
import navi_goal_test1
import subprocess

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
    
def RESET():
    x = -0.5
    y = -5.2
    theta = 0
    rospy.loginfo("Go to %0.1f, %0.1f, %0.1f", x, y, theta)
    if (nav_goals.go_to(x, y, theta)):
        print("Goal reached!")    

if __name__ == "__main__":
   
    try:
    # What to do if shut down (e.g. ctrl + C or failure)
        rospy.on_shutdown(nav_goals._shutdown)

    except rospy.ROSInterruptException:
        rospy.logerr(traceback.format_exc())
    rospy.loginfo("test terminated.")