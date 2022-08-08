#!/usr/bin/env python3

import subprocess

def stop():
    subprocess.run(['rostopic pub /move_base/cancel actionlib_msgs/GoalID -- {}'], shell=True, timeout=3)
