/*
 * Add https://dl.espressif.com/dl/package_esp32_index.json as an additional board manager URL.
 * Install "esp32" board via the board manager.
 * Install the "M5StickC 0.1.1" library via Manage Libraries.
 * Select "M5Stick-C" in the boards manager.
 * Select 115200 as the upload speed.
 */
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <M5StickC.h>
#include "settings.h"
#include "src/libraries/atom-printer/ATOM_PRINTER.h"

#define WIFI_RETRIES 2

const unsigned char TICKBOX = 'A';

ATOM_PRINTER printer;

// Make "...Secure" when have HTTPS endpoint, remove with testing with HTTP.
WiFiClientSecure client;

void registerTickBox() {

  // Define char
  unsigned char cmd[5+37];
  cmd[0] = 0x1b; // ESC
  cmd[1] = 0x26; // &
  cmd[2] = 0x03; // Font A. 3 bytes in vertical direction (24 pixels);
  cmd[3] = TICKBOX; // Replace char
  cmd[4] = TICKBOX; // Replace char
  cmd[5] = 12; // 12 bits horizontal
    
  int shift = 6;

  for (int i = 0; i < 36; i++) {

    cmd[i + shift] = 0x0;

    // Top
    if (i < 11) {
        cmd[i + shift] = 0b11000000;
    }

    // Bottom
    if (i > 24 && i < 35) {
        cmd[i + shift] = 0b00000011;
    }

    // Left
    if (i % 12 == 0) {
        cmd[i + shift] = 0xff;
    }

    // Right
    if (i % 12 == 10) {
        cmd[i + shift] = 0xff;
    }
  }
  
  Serial2.write(cmd, sizeof(cmd));

  Serial.print("Register character to replace '\\x" + String(TICKBOX, HEX) + "': ");
  for (int i = 0; i < sizeof(cmd); i++) {
    Serial.print("\\x" + String(cmd[i], HEX));
  }
  Serial.println();
}

bool connectWiFi() {
  int beginTries = 0;
  while(WiFi.status() != WL_CONNECTED) {
    WiFi.begin(ssid, password);

    int waits = 0;
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      waits++;
  
      // If it doesn't work in 5s, then it's bust.
      if (waits > 10) {
        beginTries++;
        if (beginTries > WIFI_RETRIES) {
          return false;
        }
        else {
          break;
        }
      }
    }    
  }

  return true;
}

void setup() {

  M5.begin();
  
  // Setup the serial port for debugging
  Serial.begin(115200);
  Serial.println();
  Serial.println("Ready.");

  printer.begin(&Serial2, 9600, 36, 26);
  printer.init();
  registerTickBox();

  if (!connectWiFi()) {
    Serial.println("Failed to connect to WiFi!");
    Serial2.println("Failed to connect to WiFi!\n\n\n\n");
    return;
  }

  Serial.println("Connected to WiFi!");

  HTTPClient http;
  http.setTimeout(30000);
  http.begin(client, endpoint);

  int httpResult = http.GET();
  if (httpResult != HTTP_CODE_OK) {
    Serial.println("HTTP not OK! " + String(httpResult));
    Serial2.println("HTTP not OK! " + String(httpResult) + "\n\n\n\n");
    return;
  }

  Serial.println("Connected to Server!");

  // get length of document (is -1 when Server sends no Content-Length header)
  int len = http.getSize();
  Serial.println(len);

  // create buffer for read
  uint8_t buff[128] = { 0 };

  // get tcp stream
  WiFiClient * stream = http.getStreamPtr();

  // read all data from server
  while(http.connected() && (len > 0 || len == -1)) {
    // get available data size
    size_t size = stream->available();

    if(size) {
      // read up to 128 byte
      int c = stream->readBytes(buff, ((size > sizeof(buff)) ? sizeof(buff) : size));

      // write it to printer
      Serial2.write(buff, c);

      if(len > 0) {
        len -= c;
      }
    }
    delay(1);
  }

  Serial.println("Done.");
}

void loop() {
    delay(100);
}
