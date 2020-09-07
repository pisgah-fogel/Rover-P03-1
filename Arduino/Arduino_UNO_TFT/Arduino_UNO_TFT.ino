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
  delay(1000);
  tft.fillScreen(ST7735_YELLOW);
  delay(1000);
  tft.setCursor(0, 30);
  tft.setTextColor(ST77XX_RED);
  tft.setTextSize(1);
  tft.println("Hello, World!");
  delay(1000);
}

void loop() {
  Serial.println("Test");
  delay(1);
}
