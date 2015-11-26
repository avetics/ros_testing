#!/usr/bin/env python

import rospy
import csv
from std_msgs.msg import String
from sensor_msgs.msg import Joy
from mavros_msgs.msg import RCIn
from geometry_msgs.msg import Quaternion

pub = rospy.Publisher('joytester', Joy, queue_size=50)
csv_data = []
k = 0

#offset for greater frequncey . default 1
frequency_offset = 1

testing_pub = rospy.Publisher('testing_diff', Quaternion, queue_size = 50)

def convert_ppm(ppm_val):
    result = 0
    if ppm_val < 0:
        result = (ppm_val - 1500)/500.0        
    elif ppm_val > 0:
        result = ((ppm_val - 1500)/500.0)*-1
    return result

def callback(data):
    global k 
    
    last_row = csv_data[k-frequency_offset]
    diff = Quaternion()
   
    diff.x = round(float(last_row[1])-convert_ppm(data.channels[3]),4)
    diff.y = round(float(last_row[2])-convert_ppm(data.channels[1]),4)
    diff.z = round(float(last_row[4])-convert_ppm(data.channels[0]),4)
    diff.w = round(float(last_row[5])+convert_ppm(data.channels[2]),4)
    testing_pub.publish(diff)

    if (k < len(csv_data)):
        row = csv_data[k]
        #print(data.channels[0])
        #print(convert_ppm(data.channels[3]));
        msg = Joy()
	msg.axes = (float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]),float(row[7]))
        msg.buttons = (0,0,0,0,0,0,0,0,0,0,0)
	k = k + 1
        pub.publish(msg)       
    else:
        k = 0
    
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/mavros/rc/in", RCIn, callback)
    rospy.spin()

def load_data():
    global csv_data
    #TODO change to relative Path
    with open('/home/jinahadam/catkin_ws/src/joy_logger/joy.csv', 'rb') as f:
    	   reader = csv.reader(f)
           csv_data = list(reader)

if __name__ == '__main__':
    
    try:
        load_data() #load test data from CSV
        listener()       
    except rospy.ROSInterruptException:
        pass
