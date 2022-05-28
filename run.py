from pynput.keyboard import Key, Listener
from time import sleep
import RPi.GPIO as GPIO
import threading
import constants
from motor import *
from read_files import *

GPIO.setmode(GPIO.BCM)
GPIO.setup(constants.PIN_SWITCH_UP, GPIO.IN)
GPIO.setup(constants.PIN_SWITCH_DOWN, GPIO.IN)
stop_exec = False
thread_mrot = threading.Thread()
thread_mlin = threading.Thread()
MRot = Motor(constants.PIN_MOTOR_ROT_DIR, constants.PIN_MOTOR_ROT_STEP, constants.PIN_MOTOR_ROT_MODE, constants.RESOLUTION[constants.MOTOR_ROT_RES])
MLin = Motor(constants.PIN_MOTOR_LIN_DIR, constants.PIN_MOTOR_LIN_STEP, constants.PIN_MOTOR_LIN_MODE, constants.RESOLUTION[constants.MOTOR_LIN_RES])

def on_press(key):
    global thread_mrot
    global thread_mlin
    global stop_exec
    print('{0} pressed'.format(key))

    if key.char == 'p' or key.char == 'q':
        # Stop program
        stop_exec = True
        MRot.run = False
        if thread_mrot.is_alive():
            thread_mrot.join()
        MLin.run = False
        if thread_mlin.is_alive():
            thread_mlin.join()
            
        # If Q, quit program, stops the listener
        if key.char =='q':
            return False
            
    if key.char == 's':
        
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
    # Align carriage centrally
    MLin.step_until_switch(direction = constants.MOTOR_LIN_DOWN, delay = 0.0001, switch = constants.PIN_SWITCH_DOWN) # Go till shortest end switch
    MLin.step(steps = constants.STEPS_LINEAR_FROM_SHORT_END, delay = 0.0001, direction = constants.MOTOR_LIN_UP, switch = constants.PIN_SWITCH_UP) # Move known amount of steps to center
      
    # Infinite loop processing files
    erase = False
    while not stop_exec:
        # Get pattern or eraser
        if erase:
            pattern = get_eraser_file()
            print('Erasing table using eraser {0}'.format(pattern))
        else:
            pattern = get_pattern_file()
            print('Creating pattern using {0}'.format(pattern))
            
        # Get steps
        steps = file_to_steps(pattern)
        
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
                
        # Swap erasing/non-erasing
        erase = not erase
        # Move processed pattern/eraser
        move_file(pattern)
    
# Start main sequence
main()

# Cleanup
listener.join()
print('Quitting program, goodbye')
GPIO.output(constants.PIN_MOTOR_ROT_STEP, GPIO.LOW)
GPIO.cleanup()
