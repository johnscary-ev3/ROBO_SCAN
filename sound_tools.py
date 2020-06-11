#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick 
brick = EV3Brick()

from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
from threading import (Thread, _thread)



# create a global lock object
sound_lock =  _thread.allocate_lock()


# then use this function to play sounds
def play_file(file):
    sound_lock.acquire()
    try:
        brick.speaker.play_file(file)
    finally:
        sound_lock.release()