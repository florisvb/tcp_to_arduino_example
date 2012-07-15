#!/usr/bin/env python
import roslib
roslib.load_manifest('tcp_to_arduino_example')
import rospy
import socket
from tcp_to_arduino_example.srv import *

class Arduino_Data_Client:
    def __init__ (self, rate):
        rospy.init_node('send_data_to_arduino_client', anonymous=True) 
        rospy.wait_for_service('send_data_to_arduino')
        self.send_data_to_arduino = rospy.ServiceProxy('send_data_to_arduino', SendDataToArduino)
        self.prev_msg = 'set'
        
        self.main(rate)
                
    def main(self, rate):
        try:
            rospy.Timer( rospy.Duration(1/float(rate)), self.send_data )
            rospy.spin()
        except KeyboardInterrupt:
            print "Shutting Down"
        
    def send_data(self, timer):
        if self.prev_msg == 'set':
            data = self.send_data_to_arduino("get", "sensor1", 0)
            self.prev_msg = 'get'
            print "received data: ", data
        elif self.prev_msg == 'get':
            data = self.send_data_to_arduino("set", "motor", 25)
            self.prev_msg = 'set'
            print "set data: ", data            
        

if __name__ == '__main__':

    rate = 10
    arduino_data_transmission = Arduino_Data_Client(rate)
