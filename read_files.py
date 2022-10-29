import os
import os.path
from os import path
import random
import numpy as np
import constants 

filepath = os.path.split(os.path.realpath(__file__))[0]

def get_pattern_file():
    print('Getting new pattern')
    file = get_file(filepath + '/patterns')
    return file
    
def get_eraser_file():
    print('Getting new eraser')
    file = get_file(filepath + '/erasers') 
    return file
    
def move_pattern_file(file):
    print('Moving pattern {0}'.format(file))
    move_file(filepath + '/patterns/new/{0}'.format(file))
    
def move_eraser_file(file):
    print('Moving eraser {0}'.format(file))
    move_file(filepath + '/erasers/new/{0}'.format(file))
    
def move_file(filepath):
    if path.exists(filepath):
        new_filepath = filepath.replace('new', 'processed')
        print('Move file from {0} to {1}'.format(filepath, new_filepath))
        os.rename(filepath, new_filepath)
    else:
        print('Move file, path {0} does not exist'.format(filepath))
    
def get_file(rootfolder):
    files = os.listdir('{0}/new'.format(rootfolder))
    
    # No files -> all have been processed. Move all from 'processed' to 'new'
    if len(files) == 0:
        print('Processed all files, moving processed files to new')
        files = os.listdir('{0}/processed'.format(rootfolder))
        
        # Move all files
        for file in files:
            os.rename('{0}/processed/{1}'.format(rootfolder, file), '{0}/new/{1}'.format(rootfolder, file))
        
        # Fetch files again
        files = os.listdir('{0}/new'.format(rootfolder))
        
    file = random.choice(files)
    print('Choosing file {0}'.format(file))
    return rootfolder + '/new/' + file

def get_lines(filepath):

    with open(filepath, 'r') as pattern:
        lines = pattern.readlines()
        
        for index, line in enumerate(lines):
            lines[index] = line.replace('\n', '')
            
        return lines

def lines_to_steps(lines):
    arr = np.zeros(shape=(len(lines),2), dtype=int)
    
    for index, line in enumerate(lines):
        # To steps
        theta = round(float(line.split(' ')[0]) * constants.STEPS_DISK_ROTATION / 6.283)
        rho = round(float(line.split(' ')[1]) * constants.STEPS_LINEAR_LENGTH)
        arr[index] = [theta, rho]
    arr = arr[1:] - arr[:-1]
    
    # Set first tetha to 0 to avoid random turn at the beginning
    arr[0, 0] = 0
    return arr

def add_delays(steps):
    
    # Calculate time using Theta. Given calculated time, check if delay for Rho is not too small
    arr = np.zeros(shape=(len(steps),4), dtype=float)
    # Array to hold steps and delays
    # 0 = Theta
    # 1 = Rho
    # 2 = Delay theta
    # 3 = Delay rho

    for index, step in enumerate(steps):
        time_theta = abs(step[0]) / constants.DEFAULT_SPEED
        
        # Check time is not 0, and delay for Rho would not be too small
        if time_theta != 0 and (abs(step[1]) / time_theta) <= constants.MAX_SPEED:
            # Both theta and rho -> different amount of steps, same speed -> use calculated time with amount of steps
            delay_theta = round(1/constants.DEFAULT_SPEED, 5)
            delay_rho = round(1/(abs(step[1]) / time_theta), 5) if step[1] != 0 else 0
        else:
            # Theta time is either 0, or too small for rho to perform amount of steps in given time -> use rho to calculate time for theta
            time_rho = abs(step[1]) / constants.DEFAULT_SPEED
            delay_theta = round(1/(abs(step[0]) / time_rho), 5) if step[0] != 0 else 0
            delay_rho = round(1/constants.DEFAULT_SPEED, 5)
        
        arr[index] = [step[0], step[1], delay_theta, delay_rho]

    return arr

def file_to_steps(filepath):
    lines = get_lines(filepath)
    steps = lines_to_steps(lines)
    return add_delays(steps)

