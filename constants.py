# For DRV8825
""" 
RESOLUTION = {
                'Full': (0,0,0),
                'Half': (1,0,0),
                '1/4': (0,1,0),
                '1/8': (1,1,0),
                '1/16': (0,0,1),
                '1/32': (1,0,1)
            }

FACTOR = {
                'Full': 1,
                'Half': 2,
                '1/4': 4,
                '1/8': 8,
                '1/16': 16,
                '1/32': 32
"""

# For TMC2208
RESOLUTION = {
        'Half': (1,0),
        '1/4': (0,1),
        '1/8': (0,0),
        '1/16': (1,1)
        }
    
FACTOR = {
        'Half': 2,
        '1/4': 4,
        '1/8': 8,
        '1/16': 16
        }
            
MOTOR_ROT_RES = '1/16'
MOTOR_LIN_RES = '1/16'

MOTOR_LIN_UP = 0
MOTOR_LIN_DOWN = 1
MOTOR_ROT_CW = 0
MOTOR_ROT_CCW = 1

TEETH_PULLEY = 30.0
TEETH_BELT = 309 # Was 311 but seemed a bit too much with some patterns
GEAR_RATIO = TEETH_BELT / TEETH_PULLEY
STEPS_DISK_ROTATION = 200.0 * FACTOR[MOTOR_ROT_RES] * GEAR_RATIO

STEPS_FULL_MODE_LENGTH = 2002 #2004 is full, but prevent touching the switch by reducing with 2 steps
STEPS_FULL_MODE_SHORT = 525
STEPS_LINEAR_LENGTH = ((STEPS_FULL_MODE_LENGTH - STEPS_FULL_MODE_SHORT) * FACTOR[MOTOR_LIN_RES])
STEPS_LINEAR_FROM_SHORT_END = STEPS_FULL_MODE_SHORT * FACTOR[MOTOR_LIN_RES]

PIN_MOTOR_LIN_DIR = 24
PIN_MOTOR_LIN_STEP = 23
# For DRV8825
#PIN_MOTOR_LIN_MODE = (5,6,13)
# For TMC2208
PIN_MOTOR_LIN_MODE = (14, 15)
PIN_MOTOR_ROT_DIR = 26
PIN_MOTOR_ROT_STEP = 19
PIN_MOTOR_LIN_ENABLE = 22
PIN_MOTOR_ROT_ENABLE = 17

# For DRV8825
#PIN_MOTOR_ROT_MODE = (14,15,18)
# For TMC2208
PIN_MOTOR_ROT_MODE = (5, 6)

PIN_SWITCH_UP = 20
PIN_SWITCH_DOWN = 12

STATE_SWITCH_PRESSED = 0
STATE_MOTOR_ENABLED = 0
STATE_MOTOR_DISABLED = 1

DEFAULT_SPEED = 1800.0
MAX_SPEED = 2200.0
