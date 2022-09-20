#!/usr/bin/env python3

import subprocess

def stop():
    #subprocess.run(['rostopic pub -1 /move_base/cancel actionlib_msgs/GoalID -- {}'], shell=True, timeout=3)
    subprocess.run(['rostopic pub -1 /move_base/cancel actionlib_msgs/GoalID -- {}'], shell=True)
