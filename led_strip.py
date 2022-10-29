#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import RPi.GPIO as GPIO
import time
from rpi_ws281x import PixelStrip, Color
import argparse

# LED strip configuration:
LED_COUNT = 209       # Number of LED pixels.
#LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)


class LedStripThread():
    
    running = False

    def __init__(self):
        self.running = True
        self.strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()
        self.strip.setBrightness(155)

    # Define functions which animate LEDs in various ways.
    def colorWipe(self, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        if not self.running: return
        for i in range(self.strip.numPixels()):
            if not self.running: break
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def theaterChase(self, color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        if not self.running: return
        for j in range(iterations):
            for q in range(3):
                if not self.running: break
                for i in range(0, self.strip.numPixels(), 3):
                    if not self.running: break
                    self.strip.setPixelColor(i + q, color)
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    if not self.running: break
                    self.strip.setPixelColor(i + q, 0)

    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if not self.running: return
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    def rainbow(self, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        if not self.running: return
        for j in range(256 * iterations):
            if not self.running: break
            for i in range(self.strip.numPixels()):
                if not self.running: break
                self.strip.setPixelColor(i, self.wheel((i + j) & 255))
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def rainbowCycle(self, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        if not self.running: return
        for j in range(256 * iterations):
            if not self.running: break
            for i in range(self.strip.numPixels()):
                if not self.running: break
                self.strip.setPixelColor(i, self.wheel(
                    (int(i * 256 / self.strip.numPixels()) + j) & 255))
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def theaterChaseRainbow(self, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        if not self.running: return
        for j in range(256):
            for q in range(3):
                if not self.running: break
                for i in range(0, self.strip.numPixels(), 3):
                    if not self.running: break
                    self.strip.setPixelColor(i + q, self.wheel((i + j) % 255))
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    if not self.running: break
                    self.strip.setPixelColor(i + q, 0)
                    
    def cycleColors(self):
        self.running = True
        
        while self.running:
            #self.rainbow(wait_ms = 200)
            self.rainbowCycle(wait_ms = 200)
            #self.theaterChaseRainbow()
            
        
        # Colour wipe the strip
        self.colorWipe(Color(0, 0, 0), 10)
        
    def setWhite(self):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(241, 231, 211))
        self.strip.show()
        
    def setColor(self, Color):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color)
        self.strip.show()
        
    def increaseBrightness(self):
        self.strip.setBrightness(min(self.strip.getBrightness() + 10, 255))
        self.strip.show()
        
    def decreaseBrightness(self):
        self.strip.setBrightness(max(self.strip.getBrightness() - 10, 0))
        self.strip.show()
        

# Main program logic follows:
if __name__ == '__main__':

    time.sleep(.5)

    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
    # Create NeoPixel object with appropriate configuration.
    #strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    #strip.begin()


    strip_thread = LedStripThread()

    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')
        


    try:
        while True:
            strip_thread.cycleColors()

    except KeyboardInterrupt:
        strip_thread.running = False
        strip_thread.colorWipe(strip, Color(0, 0, 0), 10)
        
