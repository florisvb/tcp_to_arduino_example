// Ethernet client for Arduino, intended for use with ROS
// Floris van Breugel 2012

#include <SPI.h>
#include <Ethernet.h>

boolean reading = false;
boolean readAction = false;
boolean readDataName = false;
boolean readDataVal = false;

char action[4];
char dataName[10];
char dataVal[33];
char inChar = -1;
byte index = 0;

// Enter a MAC address, IP address and Portnumber for your Server below.
// The IP address will be dependent on your local network:
byte mac[] = { 0x90, 0xA2, 0xDA, 0x00, 0x6B, 0xA0 };
IPAddress serverIP(192,168,0,104);
int serverPort=8888;

// Initialize the Ethernet server library
// with the IP address and port you want to use
EthernetServer server(serverPort);

void setup()
{
  // start the serial for debugging
  Serial.begin(9600);
  // start the Ethernet connection and the server:
  Ethernet.begin(mac, serverIP);
  server.begin();
  Serial.println("Server started");//log
}

void loop()
{
  // listen for incoming clients
  EthernetClient client = server.available();
  if (client) {
    String clientMsg;
    String action;
    String dataName;
    String dataVal;
    
    readAction = true;
    
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        clientMsg+=c;//store the recieved characters in a string
        
        // check for delimiters
        if (c==':') {
          readAction = false;
          readDataName = true;
        } else if (c=='=') {
          readDataName = false;
          readDataVal = true;
        } else if (c=='\n') { // if "end of line" run the appropriate function
          if (action=="set") setData(dataName, dataVal, client);
          else if (action=="get") getData(dataName, client);
          Serial.println("Message from Client:"+clientMsg);//print it to the serial, for debugging
          clientMsg = "";
          action = "";
          dataName = "";
          dataVal = "";
          readAction = true;
          readDataVal = false;
        }
        
        // save data into appropriate strings
        else if (readAction) {
          action+=c;
        } else if (readDataName) {
          dataName+=c;
        } else if (readDataVal) {
          dataVal+=c;
        }
        
       
      }
    }
    
    // give the Client time to receive the data
    delay(1);
    // close the connection:
    client.stop();
  }
}

////////////////////////////////////////////////////////////////////////////////////
// functions to do stuff

void getData(String dataName, EthernetClient client) {
  
  if (dataName=="accelerometer") {
    client.println("accelerometer data: ");
  }
  
}
  
  
  
void setData(String dataName, String dataVal, EthernetClient client) {
  
  if (dataName=="motor"){
    client.println("setting motor value");
  }
  
}
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
          
