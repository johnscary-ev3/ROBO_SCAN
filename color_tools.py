#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick 
brick = EV3Brick()

from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
from threading import Thread

import sound_tools

import object_tools


ColorSensorPort = Port.S3
ColorSensorPort_2 = Port.S1

color_detect_loop_fast_flag = False
color_sound_on   = False
color_sound_on_2 = False
color_detected   = Color.BLACK
color_detected_2 = Color.BLACK
color_detected_name   = "Black"
color_detected_name_2 = "Black"
color_rgb_int   = [0,0,0]
color_rgb_int_2 = [0,0,0]
color_rgb_int_ave   = 0
color_rgb_int_ave_2 = 0
optical_sensor_run = False
optical_sensor_run_2 = False
cs_error = False
cs_error_2 = False

def optical_sensor_init():
    global cs
    cs = ColorSensor(ColorSensorPort)

def optical_sensor_init_2():
    global cs_2   
    cs_2 = ColorSensor(ColorSensorPort_2)

#Do Optical Sensor reads
def optical_sensor_detect():
    global color_detect_loop_fast_flag
    global color_detected
    global color_detected_2
    global color_detected_name
    global color_detected_name_2
    global color_rgb_int
    global color_rgb_int_2
    global color_rgb_int_ave
    global color_rgb_int_ave_2
    global optical_sensor_run 
    global optical_sensor_run_2 
    global color_sound_on
    global color_sound_on_2
    global cs
    global cs_2
    global cs_error
    global cs_error_2
    error_fix_wait = 3000

    if optical_sensor_run:
        try: 
            if cs_error:
                #Wait some and then try to connect again
                wait(error_fix_wait)
                cs = ColorSensor(ColorSensorPort)
                cs_error = False        
            if color_detect_loop_fast_flag:
                color_rgb_int_ave= cs.reflection()
            else:
                color_rgb_int= cs.rgb()       
                color_rgb_int_ave =sum(color_rgb_int)/3
                color_detected = cs.color()
                color_detected_name = color_name(color_detected)
                if color_sound_on:
                    color_sound(color_detected,1)
        except:
            cs_error = True
            print("Color Sensor 1 Error")
            sound_tools.play_file(SoundFile.COLOR)
            sound_tools.play_file(SoundFile.ERROR)
            sound_tools.play_file(SoundFile.ONE)

    if optical_sensor_run_2:
        try: 
            if cs_error_2:
                #Wait some and then try to connect again
                wait(error_fix_wait)
                cs_2 = ColorSensor(ColorSensorPort_2)
                cs_error_2 = False 
            if color_detect_loop_fast_flag:
                color_rgb_int_ave_2= cs_2.reflection()
            else:
                color_rgb_int_2= cs_2.rgb()       
                color_rgb_int_ave_2 =sum(color_rgb_int_2)/3
                color_detected_2 = cs_2.color()
                color_detected_name_2 = color_name(color_detected_2)
                if color_sound_on_2:
                    color_sound(color_detected_2,2) 
        except:
            cs_error_2 = True
            print("Color Sensor 2 Error")
            sound_tools.play_file(SoundFile.COLOR)
            sound_tools.play_file(SoundFile.ERROR)
            sound_tools.play_file(SoundFile.TWO)
     

def color_name(color):
    # This function changes color code into string
    if color == Color.BLACK:
        return "Black"
    elif color == Color.BLUE:
        return "Blue"
    elif color == Color.GREEN:
        return "Green"
    elif color == Color.YELLOW:
        return "Yellow"
    elif color == Color.RED:
        return "Red"
    elif color == Color.WHITE:
        return "White"
    elif color == Color.BROWN:
        return "Brown"
    elif color == Color.ORANGE:
        return "Orange"
    elif color == Color.PURPLE:
        return "Purple"
    else:
        return "None"

def color_sound(color,color_sensor):
    # This function  says color except based on color_sound_on
    global color_sound_on
    global color_sound_on_2
    if color_sound_on or color_sound_on_2:
        if color == Color.WHITE:
            sound_tools.play_file(SoundFile.WHITE)
        elif color == Color.BLACK:
            sound_tools.play_file(SoundFile.BLACK)
        elif color == Color.BROWN:
            sound_tools.play_file(SoundFile.BROWN)
        elif color == Color.BLUE:
            sound_tools.play_file(SoundFile.BLUE)
        elif color == Color.GREEN:
            sound_tools.play_file(SoundFile.GREEN)
        elif color == Color.YELLOW:
            sound_tools.play_file(SoundFile.YELLOW)
        elif color == Color.RED:
            sound_tools.play_file(SoundFile.RED)  
        elif color == Color.ORANGE:
            sound_tools.play_file(SoundFile.ORANGE)
        elif color == Color.PURPLE:
            sound_tools.play_file(SoundFile.PURPLE)

        #Give Sensor number if using both color sensors
        if color_sound_on and color_sound_on_2:
            if color_sensor == 1:
                sound_tools.play_file(SoundFile.ONE)
            elif color_sensor == 2:
                sound_tools.play_file(SoundFile.TWO)
