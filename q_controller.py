import socket
from numpy import array,pi
import struct

SERVER = '192.168.4.1',7080

def servo_on(_sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)):
    _sock.sendto(b'U', SERVER)
    _sock.sendto(b'U', SERVER)
    _sock.sendto(b'U', SERVER)

def servo_off(_sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)):
    _sock.sendto(b'D', SERVER)
    _sock.sendto(b'D', SERVER)
    _sock.sendto(b'D', SERVER)

def set_angles(angles, _sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)):
    angles = [a for a in array(angles).flatten()*2/pi]
    MESSAGE = struct.pack('<cffffffffffff',b'A',*angles)

    _sock.sendto(MESSAGE, SERVER)
