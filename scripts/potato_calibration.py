#! /usr/bin/env python

from adafruit_servokit import ServoKit
import time
import json
import os

kit = ServoKit(channels=16) #instantiate pwm driver object; everything is done automatically and will work out of the box for jetson

# channel 0 is throttle
# channel 1 is steering

# right now the steering is actually perfectly calibrated with this library
# however the throttle is still very sensitive, so 0.1 is pretty fast already
# look at https://learn.adafruit.com/16-channel-pwm-servo-driver/python-circuitpython for more documentation
# specifically the set_pulse_width_range() function; you will use this to build the calibration script

#steering calibration
# Ask user to input values around 0 and 180 to determine where the 
# maximum and minimum steering is. Also ask for values around 90 to determine the "straight" value.

#initialize lists containing the info reqd. to calibrate the steering and throttle
# each is a list, first value represents the steering/throttle value. Second value is used to indicate if the variable has been calibrated
straight = [90.0,'n']
max_right = [170.0,'n']
max_left = [10.0,'n']
abs_max_right = [2000,'n']
abs_max_left = [1000,'n']

neutral_throttle = [0.0,'n'] 
max_throttle = [0.2,'n']
reverse = [-0.5,'n']

pause = .1 #number of seconds to pause for the input values to change the motor/servo values

#start by finding the absolute maximum and minimum steering positions via pwm width values
#kit.servo[1].set_pulse_width_range(abs_max_left[0],abs_max_right[0])
#if abs_max_right[1] == 'n' or abs_max_left[1] == 'n':
#    while abs_max_right[1] == 'n'
#        abs_max_right[0] = input('Please input a value near 1000 to search for the maximum possible left steering angle: ')
        
# set max right angle
kit.servo[1].angle = 90 #set steering to the approximate straight value
while max_right[1] == 'n':
    max_right[0] = input('Input a value between 90 and 180 to search for the cars maximum right steering position: ')
    kit.servo[1].angle = max_right[0] #publish the steering value to the car to observe the steering angle
    time.sleep(pause) #pause for "pause" seconds to allow the servo to move
    max_right[1] = input('Do you want to store this value as the maximum right steering angle? y/n')
    if max_right[1] == 'y':
        print('The maximum right steering angle has been set to: ',max_right[0])
        kit.servo[1].angle = 90 #set steering back to straight
        break
    elif max_right[1] != 'y' or max_right[1] != 'n':
        kit.servo[1].angle = 90 #set steering back to straight
        while max_right[1] != 'y' or max_right[1] != 'n':
            print('Please enter y to set the max value, or n to try a new value.')
            max_right[1] = input('Do you want to store the current steering angle as the maximum right steering angle? y/n ')

# set max left angle
while max_left[1] == 'n':
    max_left[0] = input('Input a value between 0 and 90 to search for the cars maximum left steering position: ')
    kit.servo[1].angle = max_left[0] #publish the steering value to the car to observe the steering angle
    time.sleep(pause) #pause for "pause" seconds to allow the servo to move
    max_left[1] = input('Do you want to store this value as the maximum left steering angle? y/n')
    if max_left[1] == 'y':
        print('The maximum left steering angle has been set to: ',max_left[0])
        kit.servo[1].angle = 90 #set steering back to straight
        break
    elif max_left[1] != 'y' or max_left[1] != 'n':
        kit.servo[1].angle = 90 #set steering back to straight
        while max_left[1] != 'y' or max_left[1] != 'n':
            print('Please enter y to set the max value, or n to try a new value.')
            max_left[1] = input('Do you want to store the current steering angle as the maximum left steering angle? y/n ')
 
# set straight forward
while straight[1] == 'n':
    straight[0] = input('Input a value between 0 and 180 to search for the cars straight steering position: ')
    kit.servo[1].angle = straight[0] #publish the steering value to the car to observe the steering angle
    time.sleep(pause) #pause for "pause" seconds to allow the servo to move
    straight[1] = input('Do you want to store this value as the straight steering angle? y/n')
    if straight[1] == 'y':
        print('The straight steering angle has been set to: ',straight[0])
        kit.servo[1].angle = straight[0] #set steering back to straight
        break
    elif straight[1] != 'y' or straight[1] != 'n':
        kit.servo[1].angle = 90 #set steering back to straight
        while straight[1] != 'y' or straight[1] != 'n':
            print('Please enter y to set the max value, or n to try a new value.')
            straight[1] = input('Do you want to store the current steering angle as the straight steering angle? y/n ')



# kit.continuous_servo[0].throttle = 0.1 #throttle is forward (pretty fast)
# kit.continuous_servo[0].throttle = -0.5 #throttle electronically brakes (it will e-brake when pwm goes from high number like 0.2 suddenly to low number like -0.5)
# kit.continuous_servo[0].throttle = 0 #throttle is at rest (but not braking so similar to neutral)

# set neutral throttle
while neutral_throttle[1] == 'n':
    neutral_throttle[0] = input('Input a value near zero to search for the point at which the throttle is just at zero output: ')
    kit.continuous_servo[0].throttle = neutral_throttle[0] #publish the throttle value to the car for observation
    time.sleep(pause) #pause for "pause" seconds to allow the throttle to spin up
    neutral_throttle[1] = input('Do you want to store this value as the neutral throttle? y/n')
    if neutral_throttle[1] == 'y':
        print('The neutral throttle value has been set to: ',neutral_throttle[0])
        kit.continuous_servo[0].throttle = neutral_throttle[0] #set throttle back to neutral.
        break
    elif neutral_throttle[1] != 'y' or neutral_throttle[1] != 'n':
        kit.continuous_servo[0].throttle = neutral_throttle[0] #set throttle back to neutral.
        while neutral_throttle[1] != 'y' or neutral_throttle[1] != 'n':
            print('Please enter y to set the neutral throttle value, or n to try a new value.')
            neutral_throttle[1] = input('Do you want to store the entered value as the neutral throttle? y/n ')
        
# set max throttle
while max_throttle[1] == 'n':
    max_throttle[0] = input('Input a value between 0 and 1 to set the max throttle: ')
    kit.continuous_servo[0].throttle = max_throttle[0] #publish the throttle value to the car for observation
    time.sleep(pause) #pause for "pause" seconds to allow the throttle to spin up
    max_throttle[1] = input('Do you want to store this value as the max throttle? y/n')
    if max_throttle[1] == 'y':
        print('The max throttle value has been set to: ',max_throttle[0])
        kit.continuous_servo[0].throttle = neutral_throttle[0] #set throttle back to neutral.
        break
    elif max_throttle[1] != 'y' or max_throttle[1] != 'n':
        kit.continuous_servo[0].throttle = neutral_throttle[0] #set throttle back to neutral.
        while max_throttle[1] != 'y' or max_throttle[1] != 'n':
            print('Please enter y to set the neutral throttle value, or n to try a new value.')
            max_throttle[1] = input('Do you want to store the entered value as the max throttle? y/n ')

# set reverse throttle
while reverse[1] == 'n':
    reverse[0] = input('Input a value between 0 and -1 to set the max reverse throttle: ')
    kit.continuous_servo[0].throttle = reverse[0] #publish the throttle value to the car for observation
    time.sleep(pause) #pause for "pause" seconds to allow the throttle to spin up
    reverse[1] = input('Do you want to store this value as the max reverse throttle? y/n')
    if reverse[1] == 'y':
        print('The max reverse throttle value has been set to: ',reverse[0])
        kit.continuous_servo[0].throttle = neutral_throttle[0] #set throttle back to neutral.
        break
    elif reverse[1] != 'y' or reverse[1] != 'n':
        kit.continuous_servo[0].throttle = neutral_throttle[0] #set throttle back to neutral.
        while reverse[1] != 'y' or reverse[1] != 'n':
            print('Please enter y to set the max reverse throttle value, or n to try a new value.')
            reverse[1] = input('Do you want to store the entered value as the max reverse throttle? y/n ')

decision = 'n'
parent_path = os.path.dirname(os.getcwd()) #this assumes the script will be run from the .../scripts directory with the json file located in a directory, one directory above
json_path = os.path.join(parent_path,'json_files','car_config.json')
while decision == 'n'or decision != 'y': #write the calibration values to the text caliration file
    decision = input('Do you want to write these values to the car configuration text file? y/n?')
    if decision == 'y': 
        config_file = open(json_path,"w")
        calibration_pack = {'straight':straight[0],'max_left':max_left[0],'max_right':max_right[0],'max_throttle':max_throttle[0],'neutral_throttle':neutral_throttle[0],'reverse':reverse[0]}
        json.dump(calibration_pack,config_file)
        config_file.close()
        print('The config file has been updated.')
    elif decision == 'n':
        print('The calibration values were not saved to car_config.json.')
        break
    else:
        print('Please select either y or n.')