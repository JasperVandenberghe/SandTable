# SandTable

Code for a Sisyphus sand table.

## Patterns
This folder contains both the processed and pending patters. After completing a pattern, it will be moved to the "processed" folder and a new pattern from the "new" folder will be used.
Patterns are generated using [sandify.org](https://sandify.org).

## Hardware
Following hardware is used for the project:
- Raspberry Pi 4B
- TMC2208 stepper drivers
- NEMA17 stepper motors
- WS2815 addressable LEDs

## Raspberry Pi settings
### WS2815 LEDs
Depending on your version of the Raspberry Pi, some configurations must be made in order for the LEDs to work properly.
This project uses the SPI configuration on a Raspberry Pi 4.
Exact configurations can be [found here](https://github.com/jgarff/rpi_ws281x#spi)

### Autostart
To autostart the program on boot of the Pi, several options are possible.
I added following line to /etc/xdg/lxsession/LXDE-pi/autostart.config
```
@lxterminal -e python2.7 [your_path_here]/run.py
```
Note that the lxterminal part is only necessary if you wish a terminal to display your running program.
