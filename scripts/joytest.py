#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Joy
from mavros_msgs.msg import RCIn

flip = 0
cdata = 0
error_offset = 3
pub = rospy.Publisher('joytester', Joy, queue_size=10)

def callback(data):
    global cdata 
    global error_offset
    
    #print(data.channels[3]-error_offset,cdata,data.channels[3]+error_offset)
    
    if  data.channels[3]-error_offset <= cdata <= data.channels[3]+error_offset: 
        #cdata = data.channels[3]
        pass
    else:
        msg = Joy()
        cdata = data.channels[3]
        global flip
        if (flip == 0):
           
	   msg.axes = (-0.5,0,0,0,0,0,0)
           msg.buttons = (0,0,0,0,0,0,0,0,0,0,0)
	   flip = 1

	   print("-0.5  = "+ str(data.channels[3]))
	else:
	   msg = Joy()
	   flip = 0
	   msg.axes = (1,0,0,0,0,0,0)
	   print("1   = "+ str(data.channels[3]))
	   msg.buttons = (0,0,0,0,0,0,0,0,0,0,0)
        pub.publish(msg)
       

    
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/mavros/rc/in", RCIn, callback)
    rospy.spin()

if __name__ == '__main__':
    
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
