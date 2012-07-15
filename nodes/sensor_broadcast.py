#!/usr/bin/env python
import roslib
roslib.load_manifest('tcp_to_arduino_example')
import rospy
from tcp_to_arduino_example.msg import ArduinoSensorData
import socket

class Arduino_Sensor_Broadcaster:
    def __init__ (self, TCP_IP, TCP_PORT, BUFFER_SIZE, sensor_list, rate):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'socket acquired, connecting...'
        self.sock.connect((TCP_IP, TCP_PORT))
        print 'socket connected to: ', TCP_IP, 'port: ', TCP_PORT 
        self.sensor_list = sensor_list
        
        self.arduino_publisher = rospy.Publisher("arduino", ArduinoSensorData)
        rospy.init_node('arduino_publisher', anonymous=True) 
        
        self.main(rate)
        
    def main(self, rate):
        try:
            rospy.Timer( rospy.Duration(1/float(rate)), self.publish_sensor_data )
            rospy.spin()
        except KeyboardInterrupt:
            print "Shutting Down"
        self.sock.close()
        
    def publish_sensor_data(self, timer):
        ros_msg = self.get_sensor_data()
        self.arduino_publisher.publish(ros_msg)
            
    def get_sensor_data(self):
        ros_msg = ArduinoSensorData()
          
        for sensor in sensor_list:
            msg_to_arduino = 'get:' + sensor + '\n'
            self.sock.send(msg_to_arduino)

            data = ''
            collect_data = True
            while collect_data:
                data += self.sock.recv(BUFFER_SIZE)
                if data[-1] == '\n':
                    collect_data = False
            #print 'data: ', data
                
            ros_msg.__setattr__(sensor, int(data) )
            
        return ros_msg
        
        
        

if __name__ == '__main__':

    TCP_IP = '192.168.0.104'
    TCP_PORT = 8888
    BUFFER_SIZE = 8
    
    sensor_list = ['sensor1', 'sensor2']
    rosrate = 10
    
    arduino_sensor_broadcaster = Arduino_Sensor_Broadcaster(TCP_IP, TCP_PORT, BUFFER_SIZE, sensor_list, rosrate)
