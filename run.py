from pynput.keyboard import Key, Listener
from time import sleep
import RPi.GPIO as GPIO
import threading
import constants
from motor import *
from led_strip import *
from read_files import *
from webserver import *
import time

class mainController:
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(constants.PIN_SWITCH_UP, GPIO.IN)
    GPIO.setup(constants.PIN_SWITCH_DOWN, GPIO.IN)
    stop_exec = False
    stop_program = False
    thread_mrot = threading.Thread()
    thread_mlin = threading.Thread()
    thread_led = threading.Thread()
    thread_webserver = None
    MRot = Motor(constants.PIN_MOTOR_ROT_DIR, constants.PIN_MOTOR_ROT_STEP, constants.PIN_MOTOR_ROT_MODE, constants.PIN_MOTOR_ROT_ENABLE, constants.RESOLUTION[constants.MOTOR_ROT_RES])
    MLin = Motor(constants.PIN_MOTOR_LIN_DIR, constants.PIN_MOTOR_LIN_STEP, constants.PIN_MOTOR_LIN_MODE, constants.PIN_MOTOR_LIN_ENABLE, constants.RESOLUTION[constants.MOTOR_LIN_RES])
    LedStrip = LedStripThread()
    webserver = None
    
    def setBrightness(self, brightness):
        if brightness is None:
            return
        
        self.LedStrip.setBrightness(brightness)
    
    def setColor(self, Color):       
        if Color == constants.Color.WHITE:
            # Check if color is already white. If not, switch to white
            if self.thread_led.is_alive():
                self.LedStrip.running = False
                self.thread_led.join()

                self.LedStrip.running = True
                self.LedStrip.setWhite()
            # Else do nothing, already white
        elif Color == constants.Color.RAINBOW:
            if self.thread_led.is_alive():
                # Already in color, do nothing
                return
            else:
                self.thread_led = threading.Thread(target = self.LedStrip.cycleColors)
                self.thread_led.start()
        else:
            return
                
    def pauseProgram(self):
        # Just pause, no big deal
        self.stop_exec = True
        
    def resumeProgram(self):
        self.stop_exec = False
   
    def quitProgram(self):
        #Do all cleanup necessary
        print('Quitting program')
        
        self.stop_exec = True
        self.stop_program = True
        self.MLin.run = False
        self.MRot.run = False
        self.LedStrip.running = False
        
        # Kill webserver
        #if self.thread_webserver.is_alive():
        #    self.thread_webserver.terminate()
        #    self.thread_webserver.join()
            
        # Stop rotational motor
        if self.thread_mrot.is_alive():
            self.thread_mrot.join()
                
        # Stop linear motor
        if self.thread_mlin.is_alive():
            self.thread_mlin.join()
                
        # Stop LED strip
        if self.thread_led.is_alive():
            self.thread_led.join()
            
        # Cleanup
        print('Quitting program, goodbye')
        self.MRot.disable_motor()
        self.MLin.disable_motor()
        GPIO.cleanup()
    
    def __init__(self):
        print('Initializing main controller')
        # Create webserver
        self.webserver = WebServer(self)
    
    def run(self):
        
        print('Starting main')
        
        # Create & start thread for LEDs
        self.thread_led = threading.Thread(target = self.LedStrip.cycleColors)
        self.thread_led.start()
        
        # Start webserver
        self.thread_webserver = threading.Thread(target = self.webserver.startServer)
        self.thread_webserver.start()
        
        # Enable both motors
        self.MLin.enable_motor()
        #MRot.enable_motor()
        
        # Align carriage
        self.MLin.step_until_switch(direction = constants.MOTOR_LIN_DOWN, delay = 0.006 / constants.FACTOR[constants.MOTOR_LIN_RES], switch = constants.PIN_SWITCH_DOWN) # Go till shortest end switch
        self.MLin.step(steps = constants.STEPS_LINEAR_FROM_SHORT_END, delay = 0.006 / constants.FACTOR[constants.MOTOR_LIN_RES], direction = constants.MOTOR_LIN_UP, switch = constants.PIN_SWITCH_UP) # Move known amount of steps to center
          
        # Infinite loop processing files
        while not self.stop_program:
            
            if self.stop_exec:
                # Pause program for 5 seconds
                time.sleep(5)
                continue
            
            # Disable motors when calculating steps, can take some time
            self.MLin.disable_motor()
            self.MRot.disable_motor()

            pattern = get_pattern_file()
            print('Creating pattern using {0}'.format(pattern))
                
            # Get steps
            steps = file_to_steps(pattern)
            print('Starting pattern')
            
            # Enable motors again
            self.MLin.enable_motor()
            self.MRot.enable_motor()
            
            # Begin pattern
            for step in steps:
                # Quit program
                if self.stop_program:
                    break
                elif self.stop_exec:
                    # Pause program here
                    while(self.stop_exec):
                        time.sleep(5)
                        continue
                      
                    
                #All conditions ok, do the steps
                # Create motor thread
                self.thread_mrot = threading.Thread(target=self.MRot.step, args=(step[0], step[2], constants.MOTOR_ROT_CW if step[0] > 0 else constants.MOTOR_ROT_CCW, None))
                self.thread_mlin = threading.Thread(target=self.MLin.step, args=(step[1], step[3], constants.MOTOR_LIN_UP if step[1] > 0 else constants.MOTOR_LIN_DOWN, constants.PIN_SWITCH_UP if step[1] > 0 else constants.PIN_SWITCH_DOWN))
                    
                # Start both motors
                self.thread_mrot.start()
                self.thread_mlin.start()
                    
                # Wait for both motors to finish
                self.thread_mrot.join()
                self.thread_mlin.join()
                        
            # Move processed pattern/eraser
            move_file(pattern)
        

if __name__ == '__main__':
    controller = mainController()
    controller.run()
    
