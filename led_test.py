from random import *
from time import *
from rpi_ws281x import *

# LED strip configuration
LED_COUNT = 20
LED_PIN = 10
LED_FREQ_HZ = 800000
LED_DMA = 1
LED_BRIGHTNESS = 100
LED_INVERT = False
LED_CHANNEL = 0

# Create and initialize strip
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()
print('Initialized strip')

def wipe():
    for i in range(LED_COUNT):
        strip.setPixelColor(i, 05)
        strip.show()

def colorCycleTest():
    color = 10
    for i in range(200):
        strip.setPixelColor(3, color)
        strip.show()
        sleep(0.05)
        color = (color + 1)

#wipe()
#colorCycleTest()

strip.setPixelColor(1, Color(0,0,255))
strip.setPixelColor(2, Color(255,0,0))
strip.setPixelColor(3, Color(0,255,0))
strip.setPixelColor(4, Color(0,0,255))
strip.setPixelColor(5, Color(255,0,0))
strip.setPixelColor(6, Color(0,255,0))
strip.setPixelColor(7, Color(0,0,255))
strip.setPixelColor(8, Color(255,0,0))
strip.setPixelColor(9, Color(0,255,0))
strip.setPixelColor(10, 100)
strip.setPixelColor(11, 200)
strip.setPixelColor(12, 200)
strip.setPixelColor(13, 200)
strip.setPixelColor(14, 200)
strip.setPixelColor(15, 200)
strip.setPixelColor(16, 200)
strip.setPixelColor(17, 200)
strip.show()
