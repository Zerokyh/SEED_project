#!/usr/bin/python3

import rospy
import random
import actionlib

from geometry_msgs.msg import PoseStamped

from mag_common_py_libs.geometry import quaternion_from_yaw, pose2str

from mbf_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseResult


def nav_goal_cb(msg):
    goal = mbf_msgs.MoveBaseGoal(target_pose=msg)
    move_base_ac.send_goal(goal)
    rospy.loginfo("Calling MBF's move_base action with target pose %f %f", msg.pose.position.x, msg.pose.position.y)
    rospy.sleep(0.010)
    rospy.loginfo("CANCEL!!!")
    move_base_ac.cancel_goal()