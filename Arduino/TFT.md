# Working with 1,8'128x160 RGB_TFT Driver IC: ST7735S and Genuino 101 (Intel)

## Setup
Display: 1,8'128x160 RGB_TFT Driver IC: ST7735S bought on aliexpress (2019)
Device: Arduino Genuino 101
Arduino IDE 1.8.13
Adafruit GFX Library 1.10.0
Adafruit ST7735 Library 1.6.0

## Pinout

GND -> GND
VDD -> +5V
SCL -> 1k -> Pin 13
SDA -> 1k -> Pin 11
RST -> 1k -> Pin 8
DC -> 1k -> Pin 10
CS -> 1k -> Pin 9
BLK -> 1k -> +5V

## Problem and fix

I tried to run this code snippet:
```c
#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ST7735.h>

#define SCLK 13
#define MOSI 11
#define CS   9
#define DC   10
#define RESET 8

Adafruit_ST7735 tft = Adafruit_ST7735(CS, DC, MOSI, SCLK, RESET);

const float pi = 3.1415927;

void setup() {
  Serial.begin(9600);

  tft.initR(INITR_BLACKTAB);
  uint16_t time = millis();
  tft.fillScreen(ST7735_BLACK);
  time = millis() - time;
  delay(100);
  tft.fillScreen(ST7735_YELLOW);
  delay(100);
}

void loop() {
  Serial.println("Test");
  delay(1);
}
```

I got the error "Cannot convert int to BitOrder".

The fix is:

In wiring_constants.h:
'''c
// Comment those lines for Genuino 101 (l.47)
// enum BitOrder {
//    LSBFIRST = 0,
//    MSBFirst = 1,
//};

#define BitOrder uint8_t
#define LSBFIRST 0
#define MSBFIRST 1
'''

In Adafruit_SPIDevice.h:
```
// l.6
#include <wiring_constants.h>
#define SPI_BITORDER_MSBFIRST MSBFIRST
#define SPI_BITORDER_LSBFIRST LSBFIRST
// Comment line 10 to 28
```
