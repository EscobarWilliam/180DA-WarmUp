/*
 This example connects to an unencrypted WiFi network.
 Then it prints the MAC address of the WiFi module,
 the IP address obtained, and other network details.

 created 13 July 2010
 by dlf (Metodo2 srl)
 modified 31 May 2012
 by Tom Igoe
 */
#include <SPI.h>
#include <WiFiNINA.h>

///////please enter your sensitive data in the Secret tab/arduino_secrets.h
char ssid[] = "ATTTMBDHWa";    // your network SSID (name)
char pass[] = "fx7eyh+gdjnn";  // your network password (use for WPA, or use as key for WEP)



void setup() {
  //Initialize serial and wait for port to open:
  SerialUSB.begin(9600);
  while (!Serial) {
    ;  // wait for serial port to connect. Needed for native USB port only
  }

  // check for the WiFi module:
  if (WiFi.status() == WL_NO_MODULE) {
    SerialUSB.println("Communication with WiFi module failed!");
    // don't continue
    while (true)
      ;
  }

  int status = WiFi.begin(ssid, pass);
  // attempt to connect to WiFi network:
  while (status != WL_CONNECTED) {
    SerialUSB.println(ssid);
    // Connect to WPA/WPA2 network:
    status = WiFi.begin(ssid, pass);

    // wait 10 seconds for connection:
    delay(10000);
  }

  // you're connected now, so print out the data:
  SerialUSB.print("You're connected to the network");
  printCurrentNet();
  printWifiData();
}

void loop() {
  // Nothing to do
}

void printWifiData() {
  // print your board's IP address:
  IPAddress ip = WiFi.localIP();
  SerialUSB.print("IP Address: ");
  SerialUSB.println(ip);
  SerialUSB.println(ip);

  // print your MAC address:
  byte mac[6];
  WiFi.macAddress(mac);
  Serial.print("MAC address: ");
  printMacAddress(mac);
}

void printCurrentNet() {
  // print the SSID of the network you're attached to:
  SerialUSB.print("SSID: ");
  SerialUSB.println(WiFi.SSID());

  // print the MAC address of the router you're attached to:
  byte bssid[6];
  WiFi.BSSID(bssid);
  SerialUSB.print("BSSID: ");
  printMacAddress(bssid);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  SerialUSB.print("signal strength (RSSI):");
  SerialUSB.println(rssi);

  // print the encryption type:
  byte encryption = WiFi.encryptionType();
  SerialUSB.print("Encryption Type:");
  SerialUSB.println(encryption, HEX);
  SerialUSB.println();
}

void printMacAddress(byte mac[]) {
  for (int i = 5; i >= 0; i--) {
    if (mac[i] < 16) {
      SerialUSB.print("0");
    }
    SerialUSB.print(mac[i], HEX);
    if (i > 0) {
      SerialUSB.print(":");
    }
  }
  SerialUSB.println();
}