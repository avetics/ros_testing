#!/usr/bin/env python

import rospy
import csv
from std_msgs.msg import String
from sensor_msgs.msg import Joy
from mavros_msgs.msg import RCIn
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Pose2D

pub = rospy.Publisher('joy', Joy, queue_size=50)
testing_pub = rospy.Publisher('testing_diff', Quaternion, queue_size = 50)
latency_ch = rospy.Publisher('latency_ch', Pose2D, queue_size = 50)

csv_data = []
k = 0

#offset for greater frequncey . default 1
frequency_offset = 1



def convert_ppm(ppm_val):
    result = 0
    if ppm_val < 0:
        result = (ppm_val - 1500)/500.0        
    elif ppm_val > 0:
        result = ((ppm_val - 1500)/500.0)*-1
    return result

def callback(data):
    diff(data)
    #compare_all(data)
    #comapre_single_channel(data)
    
    
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/mavros/rc/in", RCIn, callback)
    rospy.spin()

def load_data():
    print("Load Data")
    global csv_data
    with open('/home/jinahadam/catkin_ws/src/joy_logger/joy_data.csv', 'rb') as f:
    	   reader = csv.reader(f)
           csv_data = list(reader)


def comapre_single_channel(data):
    global k 
    
    last_row = csv_data[k-frequency_offset]

    lat = Pose2D()
    lat.x = float(last_row[1])
    lat.y = convert_ppm(data.channels[3])
    lat.theta = 0
    
    latency_ch.publish(lat)

    if (k < len(csv_data)):
        row = csv_data[k]
        msg = Joy()
        msg.axes = (float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]),float(row[7]))
        msg.buttons = (0,0,0,0,0,0,0,0,0,0,0)
        k = k + 1
        pub.publish(msg)       
    else:
        k = 0

def diff(data):
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
        msg = Joy()
     	msg.axes = (float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]),float(row[7]))
        msg.buttons = (0,0,0,0,0,0,0,0,0,0,0)
	k = k + 1
        pub.publish(msg)       
    else:
        k = 0
        

def compare_all(data):
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
        #log for post processing
        #joystick log
        c = csv.writer(open("/home/jinahadam/catkin_ws/src/testing/gps_joy.csv", "ab"))
        c.writerow([data.header.stamp.secs,row[1],row[2],row[4],row[5]])
        #rc Inn log
        c = csv.writer(open("/home/jinahadam/catkin_ws/src/testing/rc_in.csv", "ab"))
        c.writerow([data.header.stamp.secs,convert_ppm(data.channels[3]),convert_ppm(data.channels[1]),convert_ppm(data.channels[0]),convert_ppm(data.channels[2])])


        msg = Joy()
	msg.axes = (float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]),float(row[7]))
        msg.buttons = (0,0,0,0,0,0,0,0,0,0,0)
	k = k + 1
        pub.publish(msg)       
    else:
        #k = 0
        print("Joystick & RC In data logged with GPS Time")
        exit()

if __name__ == '__main__':
    
    try:
        load_data() #load test data from CSV
        listener() 
        #empty log files
        c = csv.writer(open("/home/jinahadam/catkin_ws/src/testing/gps_joy.csv", "wb")) 
        c = csv.writer(open("/home/jinahadam/catkin_ws/src/testing/rc_in.csv", "wb"))           
    except rospy.ROSInterruptException:
        pass
