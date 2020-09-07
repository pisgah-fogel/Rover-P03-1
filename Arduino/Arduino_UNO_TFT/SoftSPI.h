#ifndef SOFTSPI_H
#define SOFTSPI_H

#include <Arduino.h>

const int pin_CS = 9;
const int pin_SCLK = 13;
const int pin_MOSI = 11;

const int CS_notselected = HIGH;
const int CS_selected = LOW;

void SoftSPI_init()
{
    pinMode(pin_CS, OUTPUT);
    pinMode(pin_SCLK, OUTPUT);
    pinMode(pin_MOSI, OUTPUT);

    digitalWrite(pin_CS, CS_notselected);
}

void spi_transfer(unsigned char working) {
    for(int i = 0; i < 8; i++) {
        digitalWrite (pin_MOSI,working & 0x80);
        digitalWrite (pin_SCLK,HIGH);
        working = working << 1;
        digitalWrite(pin_SCLK,LOW);
    }
}

void spi_out(unsigned char cmd, unsigned char data) {
    digitalWrite(pin_CS, CS_selected);
    spi_transfer(cmd);
    spi_transfer(data);
    digitalWrite(pin_CS, CS_notselected);
}

#endif // SOFTSPI_H