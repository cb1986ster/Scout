#!/usr/bin/env python3.5

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import threading

import socket
import struct
from time import sleep
import sys,os

servo_no, angle, isRunning,act = 0,0,True,False

def sender():
    global servo_no
    global angle
    global isRunning
    global act
    for _ in range(10):
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(b'U', ('192.168.4.1',7080))
        sleep(0.01)

    while isRunning:
        angels = [0.0]*12
        if act: angels[servo_no] = angle
        buffer = struct.pack('<cffffffffffff',b'A',*angels)
        for i in range(10):
            socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(buffer, ('192.168.4.1',7080))
            sleep(0.01)

class GtkSignalHandler:
    def __init__(self,f,s,a):
        self.f = f
        self.s = s
        self.a = a
    def close(self, *args, **kwargs):
        global isRunning
        isRunning = False
        Gtk.main_quit()

    def updateServo(self, *args, **kwargs):
        global servo_no
        servo_no = int(self.s.get_value())
        print('servo:',servo_no)

    def updateAngle(self, *args, **kwargs):
        global angle
        angle = float(self.f.get_value())
        print('angle:',angle)

    def updateActive(self, *args, **kwargs):
        global act
        act = self.a.get_active()


sender_th = threading.Thread(target=sender)
sender_th.start()

builder = Gtk.Builder()
builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/AngelsTester.glade")
sh = GtkSignalHandler(
    builder.get_object("angle"),
    builder.get_object("servo"),
    builder.get_object("Aktywny")
)
builder.connect_signals(sh)
builder.get_object("window1").show_all()
Gtk.main()
