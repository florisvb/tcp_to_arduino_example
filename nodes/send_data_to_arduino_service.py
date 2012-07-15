#!/usr/bin/env python
import roslib
roslib.load_manifest('tcp_to_arduino_example')
import rospy
import socket
from tcp_to_arduino_example.srv import *

class Arduino_Data_Transmission:
    def __init__ (self, TCP_IP, TCP_PORT, BUFFER_SIZE):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'socket acquired, connecting...'
        self.sock.connect((TCP_IP, TCP_PORT))
        print 'socket connected to: ', TCP_IP, 'port: ', TCP_PORT 
        rospy.init_node('send_data_to_arduino_service', anonymous=True) 
        
        self.service = rospy.Service('send_data_to_arduino', SendDataToArduino, self.handle_transmission)
        
        self.main()
                
    def main(self):
        try:
            rospy.spin()
        except KeyboardInterrupt:
            print "Shutting Down"
        self.sock.close()
        
    def handle_transmission(self, request):
        msg_to_arduino = request.action + ":" + request.dataName + "=" + str(request.dataVal) + '\n'
        print 'sending msg: ', msg_to_arduino 
        self.sock.send(msg_to_arduino)
        
        data = ''
        collect_data = True
        while collect_data:
            data += self.sock.recv(BUFFER_SIZE)
            if data[-1] == '\n':
                collect_data = False
        
        return int(data)
            
        

if __name__ == '__main__':

    TCP_IP = '192.168.0.104'
    TCP_PORT = 8888
    BUFFER_SIZE = 8
    
    arduino_data_transmission = Arduino_Data_Transmission(TCP_IP, TCP_PORT, BUFFER_SIZE)
