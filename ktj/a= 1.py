#!/usr/bin/env python3
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
from time import sleep
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import sys

def movebase_client():
    
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x =  float(a[1:5])
    goal.target_pose.pose.position.y =  float(a[6:9])
    goal.target_pose.pose.orientation.w = 1

    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

def asdf():
    print(a[2:6])
    print(a[11:15])
    
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN

while True:
    _, frame = cap.read()

    decodedObjects = pyzbar.decode(frame)
    for obj in decodedObjects:
        a=obj.data.decode()
        # b=obj.data.decode()
        cv2.putText(frame, str(obj.data.decode()), (50, 50), font, 2,
                    (255, 0, 0), 3)
        asdf()
        rospy.init_node('movebase_client_py')
        result = movebase_client()
        if result:
            rospy.loginfo("Goal execution done!")
            print((sys.version))
        else: 
            rospy.loginfo("Navigation test finished.")        
    cv2.imshow("Frame", frame)
    
    # print(frame)
    # if print("Data", obj.data):
    #     break
    
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()

# if __name__ == '__main__':
#     try:
        # while True:
        #     _, frame = cap.read()
        
        #     decodedObjects = pyzbar.decode(frame)
        #     for obj in decodedObjects:
        #         a=obj.data.decode()
        #         # b=obj.data.decode()
        #         cv2.putText(frame, str(obj.data.decode()), (50, 50), font, 2,
        #                     (255, 0, 0), 3)
        #         asdf()    
        #     cv2.imshow("Frame", frame)
            
        #     # print(frame)
        #     # if print("Data", obj.data):
        #     #     break
            
        #     key = cv2.waitKey(1)
        #     if key == 27:
        #         break
        # cap.release()
        # cv2.destroyAllWindows()
    #     rospy.init_node('movebase_client_py')
    #     result = movebase_client()
    #     if result:
    #         rospy.loginfo("Goal execution done!")
    #         print((sys.version))
    # except rospy.ROSInterruptException:
    #     rospy.loginfo("Navigation test finished.")
        
