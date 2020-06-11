#!/usr/bin/env pybricks-micropython

from pybricks.hubs import (EV3Brick )
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

from pybricks.iodevices import ( AnalogSensor)

#Variables
scan_head_loop = True
scan_head_loop_run = True
scan_head_move = False
scan_head_move_2 = False

GeneralMotor1_port =Port.D
GeneralMotor2_port =Port.D
motion_print = True




#init Medium motors
def Init_GeneralMotor1():
    global GeneralMotor1
    GeneralMotor1 = Motor(GeneralMotor1_port)

def Init_GeneralMotor2():
    global GeneralMotor2
    GeneralMotor2 = Motor(GeneralMotor2_port)
    

#Init Scan Head
#Home at +90 or -90dg
def init_scan_head(head_speed,homedirection,homeoffset):
    if(homedirection):
        GeneralMotor1.run_until_stalled(head_speed, Stop.BRAKE, 50)
        GeneralMotor1.reset_angle(0)
        GeneralMotor1.run_target(head_speed, homeoffset, Stop.BRAKE, True)
    else:
        GeneralMotor1.run_until_stalled(-head_speed, Stop.BRAKE, 50)
        GeneralMotor1.reset_angle(0)
        GeneralMotor1.run_target(head_speed, homeoffset, Stop.BRAKE, True)

    GeneralMotor1.reset_angle(0)

#Init Scan Head 2
#Home at +90 or -90dg
def init_scan_head_2(head_speed,homedirection,homeoffset):
    if(homedirection):
        GeneralMotor2.run_until_stalled(head_speed, Stop.BRAKE, 50)
        GeneralMotor2.reset_angle(0)
        GeneralMotor2.run_target(head_speed, homeoffset, Stop.BRAKE, True)
    else:
        GeneralMotor2.run_until_stalled(-head_speed, Stop.BRAKE, 50)
        GeneralMotor2.reset_angle(0)
        GeneralMotor2.run_target(head_speed, homeoffset, Stop.BRAKE, True)

    GeneralMotor2.reset_angle(0)



# Move Scan Head with Relative Angle
def move_scan_head_angle(head_speed, rotation_angle):
    GeneralMotor1.run_angle(head_speed, rotation_angle, Stop.BRAKE, True)

# Move Scan Head 2with Relative Angle
def move_scan_head_angle_2(head_speed, rotation_angle):
    GeneralMotor2.run_angle(head_speed, rotation_angle, Stop.BRAKE, True)

# Move Scan Head with Target Angle
def move_scan_head_target(head_speed, target_angle, wait = True):
    GeneralMotor1.run_target(head_speed, target_angle, Stop.HOLD, wait)

# Move Scan Head with Target Angle
def move_scan_head_target_2(head_speed, target_angle, wait = True):
    GeneralMotor2.run_target(head_speed, target_angle, Stop.HOLD, wait)

 #Move Scan Head Done Check
def move_scan_head_done():
    done = GeneralMotor1.control.done()
    return done

# Move Scan Head Done Check
def move_scan_head_done_2():
    done = GeneralMotor2.control.done()
    return done

# Home Scan Head to zero dg
def home_scan_head():
    global scan_head_speed
    move_scan_head_target(scan_head_speed, 0)

# Home Scan Head 2 to zero dg
def home_scan_head_2():
    global scan_head_speed
    move_scan_head_target_2(scan_head_speed, 0)


             

#This routine moves the Scan heads using "yield" statements to give control back to caller while busy
#so we don't wait around in here.
action_timer = StopWatch()
#Move Scan head 
def scan_head_step_move():
    global scan_head_loop
    global scan_head_move
    global scan_head_move_2
    global scan_head_speed
    global scan_head_loop_run
    scan_head_wait =1000

    while scan_head_loop:
        # set up the move wait options
        if scan_head_move_2:
            move_wait_1 = False
        else:
            move_wait_1 = True
        move_wait_2 = True

        # Go through angles
        for target_angle in [-25,-50,-25,0,25,50,25,0]:
            if scan_head_loop and scan_head_loop_run:
                if scan_head_move :
                    move_scan_head_target(scan_head_speed,target_angle, move_wait_1)
                    while not move_scan_head_done():
                        yield
                if scan_head_move_2 :
                    move_scan_head_target_2(scan_head_speed,target_angle, move_wait_2)
                    while not move_scan_head_done_2():
                        yield
                
                action_timer.reset()
                while action_timer.time() < scan_head_wait:
                    yield "None"


#Get IR sensor buttons 
def get_ir_buttons(ir,chan):
    buttons=[]
    button_wait = 2
  
    try: 
        buttons = ir.buttons(chan)
    except:
        print("IR Sensor Error")
        sound_tools.play_file(SoundFile.TOUCH)
        sound_tools.play_file(SoundFile.ERROR)

    #wait some
    wait(button_wait)

    return buttons


def direction_sound(direction,GoSound = True):
    # This function  says Direction Number
    if GoSound:
        sound_tools.play_file(SoundFile.GO)
    if direction == 0:
        sound_tools.play_file(SoundFile.ZERO)
    elif direction == 1:
        sound_tools.play_file(SoundFile.ONE)
    elif direction == 2:
        sound_tools.play_file(SoundFile.TWO)
    elif direction == 3:
        sound_tools.play_file(SoundFile.THREE)  
    elif direction == 4:
        sound_tools.play_file(SoundFile.FOUR)    
    elif direction == 5:
        sound_tools.play_file(SoundFile.FIVE)    
    elif direction == 6:
        sound_tools.play_file(SoundFile.SIX)    
    elif direction == 7:
        sound_tools.play_file(SoundFile.SEVEN)  
    elif direction == 8:
        sound_tools.play_file(SoundFile.EIGHT)
    elif direction == 9:
        sound_tools.play_file(SoundFile.NINE) 
    elif direction == 10:
        sound_tools.play_file(SoundFile.TEN)  

