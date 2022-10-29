from pynput.keyboard import Key, Listener
from time import sleep
import RPi.GPIO as GPIO
import threading
import constants
from motor import *
from led_strip import *
from read_files import *

GPIO.setmode(GPIO.BCM)
GPIO.setup(constants.PIN_SWITCH_UP, GPIO.IN)
GPIO.setup(constants.PIN_SWITCH_DOWN, GPIO.IN)
stop_exec = False
thread_mrot = threading.Thread()
thread_mlin = threading.Thread()
thread_led = threading.Thread()
MRot = Motor(constants.PIN_MOTOR_ROT_DIR, constants.PIN_MOTOR_ROT_STEP, constants.PIN_MOTOR_ROT_MODE, constants.PIN_MOTOR_ROT_ENABLE, constants.RESOLUTION[constants.MOTOR_ROT_RES])
MLin = Motor(constants.PIN_MOTOR_LIN_DIR, constants.PIN_MOTOR_LIN_STEP, constants.PIN_MOTOR_LIN_MODE, constants.PIN_MOTOR_LIN_ENABLE, constants.RESOLUTION[constants.MOTOR_LIN_RES])
LedStrip = LedStripThread()

def on_press(key):
    global thread_led
    global stop_exec
    
    # Switch LEDs between colours and white
    if key.char == 'l':
        
        print('Switching LED!')
        # If going through colours, stop thread & start white
        if thread_led.is_alive():
            LedStrip.running = False
            thread_led.join()

            LedStrip.running = True
            LedStrip.setWhite()
        
        # Set LED to cycling through colours
        else:
            thread_led = threading.Thread(target = LedStrip.cycleColors)
            thread_led.start()            

    # Increase brightness
    if key.char == 'i':
        print('Increasing brightness')
        LedStrip.increaseBrightness()
        
    # Decrese brightness
    if key.char == 'd':
        print('Decresing brightness')
        LedStrip.decreaseBrightness()
    
    if key.char == 'p' or key.char == 'q':
        print('Stopping / pausing program')
        # Stop program
        stop_exec = True
        
        MLin.run = False
        MRot.run = False
        LedStrip.running = False
        
        # Stop rotational motor
        if thread_mrot.is_alive():
            thread_mrot.join()
            
        # Stop linear motor
        if thread_mlin.is_alive():
            thread_mlin.join()
            
        # Stop LED strip
        print('Set Led Strip running to {0}'.format(LedStrip.running))
        if thread_led.is_alive():
            thread_led.join()
            
        # If Q, quit program, stops the listener
        if key.char =='q':
            return False
            
    if key.char == 's':
        print('Restarting program')
        # If program has been stopped, restart
        if stop_exec:
            stop_exec = False
            main()        

#Collect keyboard events
listener = Listener(
    on_press = on_press
)
listener.start()

def main():
    global thread_led
    global thread_mlin
    global thread_mrot
    global stop_exec
    
    print('Starting main')
    
    # Create & start thread for LEDs
    thread_led = threading.Thread(target = LedStrip.cycleColors)
    thread_led.start()
    
    # Enable both motors
    MLin.enable_motor()
    MRot.enable_motor()
    
    # Align carriage centrally
    MLin.step_until_switch(direction = constants.MOTOR_LIN_DOWN, delay = 0.006 / constants.FACTOR[constants.MOTOR_LIN_RES], switch = constants.PIN_SWITCH_DOWN) # Go till shortest end switch
    MLin.step(steps = constants.STEPS_LINEAR_FROM_SHORT_END, delay = 0.006 / constants.FACTOR[constants.MOTOR_LIN_RES], direction = constants.MOTOR_LIN_UP, switch = constants.PIN_SWITCH_UP) # Move known amount of steps to center
      
    # Infinite loop processing files
    while not stop_exec:

        pattern = get_pattern_file()
        print('Creating pattern using {0}'.format(pattern))
            
        # Get steps
        steps = file_to_steps(pattern)
        print('Starting pattern')
        
        # Begin pattern
        for step in steps:
            if not stop_exec:
                # Create motor thread
                thread_mrot = threading.Thread(target=MRot.step, args=(step[0], step[2], constants.MOTOR_ROT_CW if step[0] > 0 else constants.MOTOR_ROT_CCW, None))
                thread_mlin = threading.Thread(target=MLin.step, args=(step[1], step[3], constants.MOTOR_LIN_UP if step[1] > 0 else constants.MOTOR_LIN_DOWN, constants.PIN_SWITCH_UP if step[1] > 0 else constants.PIN_SWITCH_DOWN))
                
                # Start both motors
                thread_mrot.start()
                thread_mlin.start()
                
                # Wait for both motors to finish
                thread_mrot.join()
                thread_mlin.join()
        
        # Move processed pattern/eraser
        move_file(pattern)
    
    # Disable both motors
    MLin.disable_motor()
    MRot.disable_motor()
    
# Start main sequence
main()

# Cleanup
listener.join()
print('Quitting program, goodbye')
MRot.disable_motor()
MLin.disable_motor()
GPIO.cleanup()
