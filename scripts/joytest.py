#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Joy

flip = 0
def talker():
    pub = rospy.Publisher('joytester', Joy, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1) # 10hz
    while not rospy.is_shutdown():
        msg = Joy()
	global flip
        if (flip == 0):
        	msg.axes = (0.02,0,0,0,0,0,0)
                flip = 1
        else:
                flip = 0
        	msg.axes = (0,0,0,0,0,0,0)
        msg.buttons = (0,0,0,0,0,0,0,0,0,0,0)
        pub.publish(msg)
        rate.sleep()
     

if __name__ == '__main__':
    
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
