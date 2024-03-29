from time import sleep
import RPi.GPIO as GPIO
import constants

class Motor:
	
	pin_direction = 0
	pin_step = 0
	pins_mode = 0
	pin_enable = 0
	resolution = 0
	
	run = False
	
	def setup(self):
		self.run = False
		GPIO.setup(self.pin_direction, GPIO.OUT)
		GPIO.setup(self.pin_step, GPIO.OUT)
		GPIO.setup(self.pins_mode, GPIO.OUT)  # Microstep Resolution GPIO Pins
		GPIO.setup(self.pin_enable, GPIO.OUT)
		GPIO.output(self.pins_mode, self.resolution)
		self.disable_motor() # Disable motor on startup
		
	def __init__(self, pin_direction, pin_step, pins_mode, pin_enable, resolution):
		self.pin_direction = pin_direction
		self.pin_step = pin_step
		self.pins_mode = pins_mode
		self.resolution = resolution
		self.pin_enable = pin_enable
		self.setup()
		
	def enable_motor(self):
		GPIO.output(self.pin_enable, constants.STATE_MOTOR_ENABLED)
		
	def disable_motor(self):
		GPIO.output(self.pin_enable, constants.STATE_MOTOR_DISABLED)
		
	def step(self, steps, delay, direction, switch):
		if steps == 0.0 or delay <= 0.0:
			return
			
		self.run = True

		GPIO.output(self.pin_direction, direction)
		steps = abs(steps)
		while steps > 0 and self.run and (GPIO.input(switch) != constants.STATE_SWITCH_PRESSED if switch is not None else True):
			GPIO.output(self.pin_step, GPIO.HIGH)
			sleep(delay)
			GPIO.output(self.pin_step, GPIO.LOW)
			sleep(delay)
			steps -=1
						
	def step_until_switch(self, direction, delay, switch):
		if switch is None:
			return
		
		self.run = True

		GPIO.output(self.pin_direction, direction)
		steps = 0
		while self.run and GPIO.input(switch) != constants.STATE_SWITCH_PRESSED:
			GPIO.output(self.pin_step, GPIO.HIGH)
			sleep(delay)
			GPIO.output(self.pin_step, GPIO.LOW)
			sleep(delay)
			steps+=1
			
		return steps
