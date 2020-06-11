#!/usr/bin/env pybricks-micropython

#Modified to work with ROBOZOZ3R micro-python R3 Apr 23, 2020
#Modified to work with EV3 micro-python Rev3  Mar 30, 2020
#Modified for EV3RSTORM ; started Feb 18 2020
#RC Mode, Detect objects and Ambient Light, Gyro turns, Check directions or Random reverse or Run blades on detect object modes

#KRAZ3 modified with Scan Head to get directions  Jan 9 2020
#KRAZ3_RC_SCAN_HEAD Project

#from pybricks import ev3brick as brick
from pybricks.hubs import EV3Brick
brick =EV3Brick()

from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
#from pybricks.parameters import (Port, Stop, Direction, Color,
#                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
from threading import Thread

import random

import color_tools 

import motion_tools

import object_tools

import sound_tools



#Print Rev
print("ROBO_SCAN EV3 micro-python-R2 No Threads JS 6/10/2020")

#Print Flags
GeneralLoopPrint = False
DirectionInfoPrint = False
ObjectDetectPrint = False
ObjectDetectPrintIfDetected = True
Follow_line_diagnostic = False
FollowLinePrint = False
ColorSensorPrint = False
ColorSensorPrintIfBlack = True
FollowBeaconPrint = False
motion_tools.motion_print = False
object_tools.ObjectDetectSoundPrint = False

#Hardware Configuration Flags 
InfraredSensorPortAvailable_1 = True
InfraredSensorPortAvailable_2 = False
UltrasonicPresent =True
UltrasonicPresent_2 =False
GyroAvailable = False
OpticalSensorAvailable = True
OpticalSensorAvailable_2 = True
ScanHeadPresent = True
ScanHeadPresent_2 = False

#Scanhead Home direction
ScanHeadHomeRight = True
ScanHeadHomeRight_2 = False

#Scanhead offset from Home to Forward position
ScanHeadHomeOffset = -55
ScanHeadHomeOffset_2 =  90

#Ports for Sensor Inputs
InfraredSensorPort = Port.S4
InfraredSensorPort_2 = Port.S2

object_tools.UltrasonicSensorPort =Port.S3
object_tools.UltrasonicSensorPort_2 =Port.S3

color_tools.ColorSensorPort = Port.S2
color_tools.ColorSensorPort_2 = Port.S1

#Medium Motor Ports
motion_tools.GeneralMotor1_port =Port.D
motion_tools.GeneralMotor2_port =Port.D


#Features Config variables
UseSonicObjectDetect = True
UseScanHeadObjectDetect = True
UseOpticalSensors =True
object_tools.object_detect_sound_on = True


#  Test head directions

#For Bobodozer
target_angle = [ 45,  0, -45, -90, -135, -180, -225, -270]
target_direc = [  1,  0,   7,   6,    5,    4,    3,    2]
num_head_poistions =8


#variables used later
buttons=[]

# Play a sound.
#brick.sound.beep()
brick.speaker.beep(500, 100)


 # Turn the light green
brick.light.on(Color.GREEN)

# Set Display
#brick.display.image(ImageFile.EV3)
brick.screen.load_image(ImageFile.EV3)


#Init the Ultrasonic Distance sensors
if UseSonicObjectDetect:
    if UltrasonicPresent:
        object_tools.Init_UltrasonicSensor()
    if UltrasonicPresent_2:
        object_tools.Init_UltrasonicSensor_2()

#Init Small Motors if present
if ScanHeadPresent :
    motion_tools.Init_GeneralMotor1()
if ScanHeadPresent_2 :
    motion_tools.Init_GeneralMotor2()

#set up some motor speeds
head_speed = 300


# Init the Scan Head
if UseScanHeadObjectDetect:
    if ScanHeadPresent:
        motion_tools.init_scan_head(head_speed, ScanHeadHomeRight, ScanHeadHomeOffset)
        #  Test head directions
        for i in range(num_head_poistions):
            motion_tools.move_scan_head_target(head_speed, target_angle[i])
            motion_tools.direction_sound(target_direc[i], False)
            wait(250)
        #Reset head to 0 position
        motion_tools.move_scan_head_target(head_speed, 0)

# Init the Scan Head 2
    if ScanHeadPresent_2:
        motion_tools.init_scan_head_2(head_speed, ScanHeadHomeRight_2, ScanHeadHomeOffset_2)
        #  Test head directions
        for i in range(num_head_poistions):
            motion_tools.move_scan_head_target_2(head_speed, target_angle[i])
            motion_tools.direction_sound(target_direc[i], False)
            wait(250)
        #Reset head to 0 position
        motion_tools.move_scan_head_target_2(head_speed, 0)

# Play another beep sound.
# This time with a higher pitch (1000 Hz) and longer duration (500 ms).
brick.speaker.beep(1000, 500)

# Initialize IR sensors
if InfraredSensorPortAvailable_1:
    ir =InfraredSensor(InfraredSensorPort)
if InfraredSensorPortAvailable_2:
    ir_2= InfraredSensor(InfraredSensorPort_2)


#Enable object detect 
if UseSonicObjectDetect:
    if UltrasonicPresent:
        object_tools.object_detect_run= True
    if UltrasonicPresent_2:
        object_tools.object_detect_run_2 = True


#Start Optical Sensors
if UseOpticalSensors:
    if OpticalSensorAvailable:
        color_tools.optical_sensor_run= True
    if OpticalSensorAvailable_2:
        color_tools.optical_sensor_run_2 = True
    #Init Optical Sensors    
    color_tools.optical_sensor_init()


#Enable Scan heads moves 
if UseScanHeadObjectDetect:
    if ScanHeadPresent:
        motion_tools.scan_head_move = True
    if ScanHeadPresent_2:
        motion_tools.scan_head_move_2 = True
    if (ScanHeadPresent or ScanHeadPresent_2):
        motion_tools.scan_head_speed = head_speed
     

# Main loop 
# Will exit based on IR Exit Beacon Button

#Set some Control Flags
main_loop = True

butt_len1 = 0
butt_len2 = 0
butt_len3 = 0
butt_len4 = 0

main_loop_wait_time = 10

#Start the scan head move generator routine using yield
if UseScanHeadObjectDetect:
    action_task = motion_tools.scan_head_step_move()

#Main Loop
while main_loop ==True:
    #Read Sensors
    color_tools.optical_sensor_detect()
    object_tools.sonic_sensor_object_detect()

    #move Scan head if enabled
    if UseScanHeadObjectDetect:
        action = next(action_task)

    #Do Printouts
    if GeneralLoopPrint:
        print(" ")
        print("OpticalSensorAvailable=", OpticalSensorAvailable )
    if object_tools.object_detect_loop and ObjectDetectPrint:
        print("dist=", object_tools.dist, "mm","    dist_2=", object_tools.dist_2, "mm")
        print("object_detected=", object_tools.object_detected, "object_detected_1=", object_tools.object_detected_1,"object_detected_2=", object_tools.object_detected_2)
    if object_tools.object_detect_loop and ObjectDetectPrintIfDetected and object_tools.object_detected:
        print("object_detected:")
        print("dist=", object_tools.dist, "mm","    dist_2=", object_tools.dist_2, "mm")
        print("object_detected_1=", object_tools.object_detected_1,"object_detected_2=", object_tools.object_detected_2)
    if OpticalSensorAvailable and ColorSensorPrint and UseOpticalSensors:
        print("color= ", color_tools.color_detected, "color_name= ", color_tools.color_detected_name)
        print("rgb_int= ",'R: {:.2f} G: {:.2f} B: {:.2f} '.format(color_tools.color_rgb_int[0],color_tools.color_rgb_int[1],color_tools.color_rgb_int[2]) )
        print("rgb_int_ave= ",'{:.2f} '.format(color_tools.color_rgb_int_ave) ) 
    if OpticalSensorAvailable and ColorSensorPrintIfBlack and UseOpticalSensors and color_tools.color_detected_name == "Black":
        print("Black detected:")
        print("rgb_int= ",'R: {:.2f} G: {:.2f} B: {:.2f} '.format(color_tools.color_rgb_int[0],color_tools.color_rgb_int[1],color_tools.color_rgb_int[2]) )
        print("rgb_int_ave= ",'{:.2f} '.format(color_tools.color_rgb_int_ave) ) 
    if OpticalSensorAvailable_2 and ColorSensorPrint and UseOpticalSensors:
        print("color_2= ", color_tools.color_detected_2, "color_name_2= ", color_tools.color_detected_name_2)
        print("rgb_int_2= ",'R: {:.2f} G: {:.2f} B: {:.2f} '.format(color_tools.color_rgb_int_2[0],color_tools.color_rgb_int_2[1],color_tools.color_rgb_int_2[2]) )
        print("rgb_int_ave_2= ",'{:.2f} '.format(color_tools.color_rgb_int_ave_2) ) 
    if OpticalSensorAvailable_2 and ColorSensorPrintIfBlack and UseOpticalSensors and color_tools.color_detected_name_2 == "Black":
        print("Black detected 2:")
        print("rgb_int_2= ",'R: {:.2f} G: {:.2f} B: {:.2f} '.format(color_tools.color_rgb_int_2[0],color_tools.color_rgb_int_2[1],color_tools.color_rgb_int_2[2]) )
        print("rgb_int_ave_2= ",'{:.2f} '.format(color_tools.color_rgb_int_ave_2) ) 
    if GeneralLoopPrint:
        print("butt_len1=", butt_len1, "butt_len2=", butt_len2, "butt_len3=", butt_len3, "butt_len4=", butt_len4)        
    
    
    # Make the light orange for Object and play sound
    if object_tools.object_detect_loop and object_tools.object_detected:
        brick.light.on(Color.ORANGE)
        #Play Object sound if needed
        object_tools.object_sound() 
    else:
        #set light back to Green
        brick.light.on(Color.GREEN)
   
    # IR buttons
    # Check for button press on Chan 1 
    chan = 1
    # IR Button Command Mode
    if InfraredSensorPortAvailable_1 :
        buttons = motion_tools.get_ir_buttons(ir,chan)      
        butt_len1=len(buttons)
    else:
        buttons.clear()
    butt_len1=len(buttons)

    # Exit Button
    if (Button.BEACON in buttons):
        main_loop =False

    # Check for button press on Chan 2 
    chan = 2  
    if InfraredSensorPortAvailable_1:       
        buttons = motion_tools.get_ir_buttons(ir,chan)  
    else:
        buttons.clear()
    butt_len2= len(buttons)

    
    # Exit Button
    if (Button.BEACON in buttons):
        main_loop =False
       

    # Check for button press on Chan 3 
    chan = 3
    if(InfraredSensorPortAvailable_1):      
        buttons = motion_tools.get_ir_buttons(ir,chan)
    else:
        buttons.clear()
    butt_len3 =len(buttons)

    
    # Exit Button (use for follow  Beacon)
    if (Button.BEACON in buttons):
       main_loop =False
    

    # Check for button press on Chan 4 
    chan = 4
    if(InfraredSensorPortAvailable_1):  
        buttons = motion_tools.get_ir_buttons(ir,chan)
    else:
        buttons.clear()
    butt_len4 = len(buttons)


    # Exit Button
    if Button.BEACON in buttons  :
        main_loop =False
 
    
    #wait at end of main_loop
    wait(main_loop_wait_time)
    

# Terminate progam  after saying stop
sound_tools.play_file(SoundFile.STOP)
