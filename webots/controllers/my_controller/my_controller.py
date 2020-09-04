from controller import Robot
import threading
import socket
import re
import numpy as np
import time

robot = Robot()

timestep = int(robot.getBasicTimeStep())

isRunning = True
joints_names = ['LPC','LPF','LPT','RPC','RPF','RPT','RAC','RAF','RAT','LAC','LAF','LAT']
joints = [robot.getMotor(name) for name in joints_names ]
positions = [ 0 for _ in joints ]


def server():
    global positions
    global isRunning
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 2367))
    sf = s.makefile()
    buffer = ''

    while isRunning:
        buffer += sf.read(64)
        buffer = buffer[:256]
        m = re.match(r'.*\<RAW:(\d*):(-?\d*.\d*)\>.*',buffer)
        if m:
            buffer = ''
            v = m.groups()
            positions[int(v[0])] = float(v[1])
            continue
        m = re.match(r'.*\<RAW:(-?\d*.\d*);(-?\d*.\d*);(-?\d*.\d*);(-?\d*.\d*);(-?\d*.\d*);(-?\d*.\d*);(-?\d*.\d*);(-?\d*.\d*);(-?\d*.\d*);(-?\d*.\d*);(-?\d*.\d*);(-?\d*.\d*)\>.*',buffer)
        if m:
            buffer = ''
            v = m.groups()
            positions = [ float(e) for e in m.groups() ]
            continue

def main():
    global joints
    global positions
    global isRunning
    while robot.step(timestep) != -1:
        for joint, position in zip(joints,positions):
            joint.setPosition(position)
    isRunning = False

server_thread = threading.Thread(target=server)
server_thread.start()
main()
server_thread.join()
