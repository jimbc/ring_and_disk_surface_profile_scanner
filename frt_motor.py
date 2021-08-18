# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 22:32:53 2019

@author: BaiChong
"""
from serial import Serial
import TMCL
from time import sleep


class single_axis_motor:

    def __init__(self):

        pass

    def connect(self, port_number='COM3'):

        # serial-address as set on the TMCM module.
        MODULE_ADDRESS = 1

        # Open the serial port presented by your rs485 adapter
        try:
            self.serial_port = Serial(port_number)
        except:
            self.serial_port.close()
            sleep(1)
            self.serial_port = Serial(port_number)

        # Create a Bus instance using the open serial port
        bus = TMCL.connect(self.serial_port)

        # Get the motor
        self.motor = bus.get_motor(MODULE_ADDRESS)

    def configure(self, microstep, current, speed):
        self.speed = speed
        self.motor.send(5, 4, 0, self.speed)  # Positioniergeschwindigkeit 200 Schritte/s
        self.motor.send(5, 5, 0, 200)  # Beschleunigung
        self.motor.send(5, 179, 0,
                        1)  # Setze Spannungsbereich, Low Current Range (0 = High Current Range, 1 = Low Current Range)
        self.motor.send(5, 6, 0,
                        current)  # Maximale Spannung (Darf nicht höher sein als 230 => Kann zu Überhitzung führen) Achte auf Current Range
        self.motor.send(5, 7, 0, 8)  # Standby Spannung (zum Abkühlen)
        self.motor.send(5, 140, 0, microstep)  # Microstep Auflösung in 2-Potenz
        #        sleep(2)
        self.motor.send(5, 1, 0, 0)  # Setze aktuelle Position auf 0
        self.motor.send(4, 0, 0, 0)  # Bewege Motor auf Position 0
        self.motor.send(27, 1, 0, 100)  # Wait until position is reached or ticks reached (1 tick = 10 ms)
        sleep(1)

    def rotate_right(self, steps):
        self.motor.send(1, 0, 0, steps)  # ROR: Rotate right by "step" steps
        self.motor.send(27, 1, 0, 100)  # Wait until position is reached or ticks reached (1 tick = 10 ms)

    def rotate_left(self, steps):
        self.motor.send(2, 0, 0, steps)  # ROL: Rotate left by "step" steps
        self.motor.send(27, 1, 0, 100)  # Wait until position is reached or ticks reached (1 tick = 10 ms)

    def stop(self):
        self.motor.send(3, 0, 0, 0)

    def mov_abs(self, position):
        self.motor.send(4, 0, 0, position)
        # self.motor.send(27,1,0,0)
        self.motor.send(5, 1, 0, 0)
        # self.motor.send(27,1,0,0)
        sleeptime = position / self.speed
        sleep(sleeptime)

    def mov_rel(self, steps):
        self.motor.send(4, 1, 0, steps)
        self.motor.send(27, 1, 0, 150)
        sleeptime = steps / self.speed
        sleep(sleeptime)

    def disconnect(self, port_number='COM3'):
        self.serial_port.close()
