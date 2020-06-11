#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick 
brick = EV3Brick()


from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
#from threading import Thread
from threading import (Thread, _thread)


import motion_tools

import sound_tools

# create a global lock object for sonic sensor reads
sensor_lock =  _thread.allocate_lock()

#Configuration Variables
UltrasonicSensorPort =Port.S2
UltrasonicSensorPort_2 =Port.S3
dist = 500
dist_2= 500
object_detect_limit = 300
object_detect_loop = True
object_detect_run = True
object_detect_run_2 = False
object_detected = False
object_detected_1 = False
object_detected_2 = False
object_detect_sound_on = False
object_detect_MoveMotor1_run = False
ObjectDetectSoundPrint = False
ss_error =False
ss_error_2= False

def Init_UltrasonicSensor():
    global us
    us = UltrasonicSensor(UltrasonicSensorPort)

def Init_UltrasonicSensor_2():
    global us_2
    us_2 = UltrasonicSensor(UltrasonicSensorPort_2)


def object_sound():
    global object_detected
    global object_detected_1
    global object_detected_2
    global object_detect_run
    global object_detect_run_2
    global object_detect_loop
    global object_detect_sound_on
    global ObjectDetectSoundPrint

    if  object_detected and object_detect_run  and object_detect_sound_on:
            
        if ObjectDetectSoundPrint:
            print("Object Detect Sound Triggered:", "    Object_detected_1= ", object_detected_1, "    Object_detected_2= ", object_detected_2 )

        if  (object_detected_1 and not object_detect_run_2):
             sound_tools.play_file(SoundFile.DETECTED)

        elif(object_detected_2 and not object_detect_run_1):
            sound_tools.play_file(SoundFile.DETECTED)

        elif object_detected_1 and not object_detected_2:
            sound_tools.play_file(SoundFile.DETECTED)
            sound_tools.play_file(SoundFile.ONE)

        elif not object_detected_1 and object_detected_2:
            sound_tools.play_file(SoundFile.DETECTED)
            sound_tools.play_file(SoundFile.TWO)

        elif object_detected_1 and object_detected_2:
            sound_tools.play_file(SoundFile.DETECTED)
            sound_tools.play_file(SoundFile.ONE)
            sound_tools.play_file(SoundFile.TWO)
    

#get distance to objects
def get_object_dist():
    global us
    object_dist = us.distance(False)
    return object_dist

#get distance to objects Sensor 2
def get_object_dist_2():
    global us_2
    object_dist_2 = us_2.distance(False)
    return object_dist_2

     
#Sonic sensor object detect;  Handles 2 Sensors
def sonic_sensor_object_detect():
    global dist
    global dist_2
    global object_detected
    global object_detected_1
    global object_detected_2
    global object_detect_run
    global object_detect_run_2
    global object_detect_limit
    global ss_error 
    global ss_error_2

    object_detect_wait_time = 50
    error_fix_wait =3000
    
     #Sensor 1
    if object_detect_run:
        try:
            if ss_error:
                #Wait some and then try to connect again
                wait(error_fix_wait)
                Init_UltrasonicSensor()
                ss_error=False 
            #wait some so we don't go to fast
            wait(object_detect_wait_time) 
            dist = get_object_dist()
            if dist < object_detect_limit:
                object_detected_1 =True  
            else:
                object_detected_1 =False
        except:
            ss_error = True
            print("Sonic Sensor 1 Error")
            sound_tools.play_file(SoundFile.DETECTED)
            sound_tools.play_file(SoundFile.ERROR)
            sound_tools.play_file(SoundFile.ONE)
        if dist == 0 and not ss_error:
            ss_error = True
            print("Sonic Sensor 1 ZERO Error")
            sound_tools.play_file(SoundFile.DETECTED)
            sound_tools.play_file(SoundFile.ZERO)
            sound_tools.play_file(SoundFile.ERROR)
            sound_tools.play_file(SoundFile.ONE)

    else:
        object_detected_1 =False 

    if object_detected_1:
        object_detected = True

    #Sensor 2
    if object_detect_run_2:
        try:
            if ss_error_2:
                #Wait some and then try to connect again
                wait(error_fix_wait)
                Init_UltrasonicSensor_2()
                ss_error_2=False 
            #wait some so we don't go to fast
            wait(object_detect_wait_time)  
            dist_2 = get_object_dist_2()
            if dist_2 < object_detect_limit:
                object_detected_2 = True  
            else:
                object_detected_2 = False
        except:
            ss_error_2 = True
            print("Sonic Sensor 2 Error")
            sound_tools.play_file(SoundFile.DETECTED)
            sound_tools.play_file(SoundFile.ERROR)
            sound_tools.play_file(SoundFile.TWO)
        if dist_2 == 0 and not ss_error_2:
            ss_error_2 = True
            print("Sonic Sensor 2 ZERO Error")
            sound_tools.play_file(SoundFile.DETECTED)
            sound_tools.play_file(SoundFile.ZERO)
            sound_tools.play_file(SoundFile.ERROR)
            sound_tools.play_file(SoundFile.TWO)
    else:
        object_detected_2 = False

    #Set Combined Objected detected flag
    if object_detected_1 or object_detected_2:
        object_detected = True
    else:
        object_detected = False

    


