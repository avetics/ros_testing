#!/usr/bin/env python

import rospy
import csv
from std_msgs.msg import String
from sensor_msgs.msg import Joy
from mavros_msgs.msg import RCIn
from geometry_msgs.msg import Quaternion

flip = 0
cdata = 0
error_offset = 3
pub = rospy.Publisher('joytester', Joy, queue_size=10)
csv_data = []
k = 0

testing_pub = rospy.Publisher('testing_diff', Quaternion, queue_size = 10)

def convert_ppm(ppm_val):
    result = 0
    if ppm_val < 0:
        result = (ppm_val - 1500)/500.0        
    elif ppm_val > 0:
        result = ((ppm_val - 1500)/500.0)*-1
    return result

def callback(data):
    global cdata 
    global error_offset
    global k 
    
    last_row = csv_data[k-1]
    diff = Quaternion()
    #print(round(float(last_row[1])-convert_ppm(data.channels[3]),4), data.channels[3])
    #print(round(float(last_row[2])-convert_ppm(data.channels[1]),4), data.channels[1])
    #print(round(float(last_row[4])-convert_ppm(data.channels[0]),4), data.channels[0])
    #print(round(float(last_row[5])+convert_ppm(data.channels[2]),4), data.channels[2])

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

    #print("DEBUG "+str(data.channels[3]-error_offset),str(cdata),str(data.channels[3]+error_offset));
    #if  1 != 1:#data.channels[6]-error_offset <= cdata <= data.channels[6]+error_offset: 
    #    pass
    #    #PWM value not updated so dont send 
    #else:
    #    msg = Joy()
    #    cdata = data.channels[3]
    #    global flip
    #    if (flip == 0):
    #       if (k <= len(csv_data)):
    #           row = csv_data[k]
    #            print("testing with : "+row[1],row[2],row[3],row[4],row[5],row[6]);
    #	   	msg.axes = (float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]))
    #       	msg.buttons = (0,0,0,0,0,0,0,0,0,0,0) 
    #	   	flip = 1
    #            k = k + 1
    #
    #	   print("-0.5  = "+ str(data.channels[3]))
    # 	else:
    #       #reset PWM
    #	   flip = 0
    #	   msg.axes = (0,0,0,0,0,0,0)
    #	   print("1   = "+ str(data.channels[3]))
    #	   msg.buttons = (0,0,0,0,0,0,0,0,0,0,0)
    # d d     pub.publish(msg)
       
    
    
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/mavros/rc/in", RCIn, callback)
    rospy.spin()

def load_data():
    global csv_data
    with open('/home/jinahadam/catkin_ws/src/joy_logger/joy.csv', 'rb') as f:
    	   reader = csv.reader(f)
           csv_data = list(reader)



    

if __name__ == '__main__':
    
    try:
        load_data()
        listener()
        
    except rospy.ROSInterruptException:
        pass
