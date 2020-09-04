#!/usr/bin/env python3.5

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import threading

import socket
import struct
from time import sleep
import sys,os

servo_no, freq, isRunning,act = 0,0,True,False

def sender():
    global servo_no
    global freq
    global isRunning
    global act
    for _ in range(10):
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(b'U', ('192.168.4.1',7080))
        sleep(0.01)

    while isRunning:
        freqs = [0]*12
        if act:freqs[servo_no] = freq
        buffer = struct.pack('<cIIIIIIIIIIII',b'F',*freqs)
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

    def updateFreq(self, *args, **kwargs):
        global freq
        freq = int(self.f.get_value())

    def updateActive(self, *args, **kwargs):
        global act
        act = self.a.get_active()


sender_th = threading.Thread(target=sender)
sender_th.start()

builder = Gtk.Builder()
builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/ServoTester.glade")
sh = GtkSignalHandler(
    builder.get_object("freq"),
    builder.get_object("servo"),
    builder.get_object("Aktywny")
)
builder.connect_signals(sh)
builder.get_object("window1").show_all()
Gtk.main()
