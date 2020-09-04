
import socket
from numpy import array

def set_angles(angles):
    angles = array(angles).flatten()

    UDP_IP = "127.0.0.1"
    UDP_PORT = 2367
    MESSAGE = '<RAW:'+';'.join( ["{:3.2f}".format(a) for a in angles] )+'>'

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    # print(MESSAGE)
    sock.sendto(MESSAGE.encode('UTF-8'), (UDP_IP, UDP_PORT))
