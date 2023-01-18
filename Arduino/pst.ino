#include <SPI.h>
#include <WiFiNINA.h>
#include <Arduino_LSM6DS3.h>
#define SWITCH_PIN 2u
///ACCELERO
float x, y, z;
int degreesX = 0;
int degreesY = 0;
int h;
///////please enter your sensitive data in the Secret tab/arduino_secrets.h
char ssid[] = "SSID DE TA CONNECTION";        // your network SSID (name)
char pass[] = "MDP DE TA CONNECTION";    // your network password (use for WPA, or use as key for WEP)
int keyIndex = 0;                 // your network key Index number (needed only for WEP)

int status = WL_IDLE_STATUS;

WiFiServer server(80);
static bool isPressed;
void setup() {
  //ACCELERO
  h = 1;
  isPressed = false;
  Serial.begin(9600);
  Serial.println("Started");

  if (!IMU.begin()) {
    while (1);
  }

  ///
  

  // check for the WiFi module:
  if (WiFi.status() == WL_NO_MODULE) {
    // don't continue
    while (true);
  }

  String fv = WiFi.firmwareVersion();

  // attempt to connect to Wifi network:
  while (status != WL_CONNECTED) {
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
    status = WiFi.begin(ssid, pass);

    // wait 10 seconds for connection:
    delay(10000);
  }
  server.begin();
  // you're connected now, so print out the status:
  printWifiStatus();
}


void loop() {
  // listen for incoming clients
  
  if (digitalRead(SWITCH_PIN) == HIGH)
  {
      if (!isPressed)
      {
          isPressed = true;
          h++;
          if (h>2){
            h=1;
          }
      }
  }
  else
  {
      if (isPressed)
      {
          isPressed = false;
      }
  }
  WiFiClient client = server.available();
  if (client) {
    
    // an http request ends with a blank line
    boolean currentLineIsBlank = true;
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        Serial.println("request");
        // if you've gotten to the end of the line (received a newline
        // character) and the line is blank, the http request has ended,
        // so you can send a reply
        if (c == '\n' && currentLineIsBlank) {
          // send a standard http response header
          client.println("HTTP/1.1 200 OK");
          client.println("Content-Type: text/html");
          client.println("Connection: close");  // the connection will be closed after completion of the response
          client.println("Refresh: 5");  // refresh the page automatically every 5 sec
          client.println();
          if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);
  }
  if (x > 0.4) {
    client.println(1*h);
    break;
  }
  if (x < -0.4) {
    client.println(3*h);
    break;
    }
  if (y > 0.4) {

    client.println(4*h);
    break;
    }
  if (y < -0.4) {
    client.println(5*h);
    break;
    }
          
          client.println("9");
          break;
        }
        if (c == '\n') {
          // you're starting a new line
          currentLineIsBlank = true;
        } else if (c != '\r') {
          // you've gotten a character on the current line
          currentLineIsBlank = false;
        }
      }
    } 
    // give the web browser time to receive the data
    delay(1);

    // close the connection:
    client.stop();
  }
}


void printWifiStatus() {

  // print your board's IP address:
  IPAddress ip = WiFi.localIP();

  // print the received signal strength:
  long rssi = WiFi.RSSI();
}
