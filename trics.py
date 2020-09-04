from numpy import array,linspace
from time import sleep

from QModel import QModel
from controller import set_angles
from configs import default

def jump(q):
    while 1:
        points = array([
            list(q.legs[0].position),list(q.legs[1].position),list(q.legs[2].position),list(q.legs[3].position)
        ])

        points[0][0] += 0.8
        points[0][1] += 0.2
        points[0][2] = -0.3
        #
        points[1][0] -= 0.8
        points[1][1] += 0.2
        points[1][2] = -0.3
        #
        points[2][0] -= 0.8
        points[2][1] -= 0.2
        points[2][2] = -0.3
        #
        points[3][0] +=0.8
        points[3][1] -=0.2
        points[3][2] = -0.3

        q(points=points)
        q(points=points)
        q(points=points)
        sleep(.5)

        for leg in range(4):
            points[leg] += [0,0,0.4]
        q(points=points)
        q(points=points)
        q(points=points)
        sleep(2.5)
        for leg in range(4):
            points[leg] += [0,0,-2]
        q(points=points)
        q(points=points)
        q(points=points)
        sleep(0.7)

        for leg in range(4):
            points[leg][0]*=2
            points[leg][1]*=2
            points[leg][2] = -0.8
        q(points=points)
        q(points=points)
        q(points=points)
        sleep(2)


def push_2(q):
    points = array([
        list(q.legs[0].position),list(q.legs[1].position),list(q.legs[2].position),list(q.legs[3].position)
    ])

    points[0][0] += 0.8
    points[0][1] += 0.2
    points[0][2] -= 0
    #
    points[1][0] -= 0.8
    points[1][1] += 0.2
    points[1][2] -= 0
    #
    points[2][0] -= 0.8
    points[2][1] -= 2
    points[2][2] -= 0
    #
    points[3][0] +=0.8
    points[3][1] -= 2
    points[3][2] -= 0

    q(points=points)

    d = array([0,-0.01,-0.05])
    while 1:
        for i in range(50*2):
            points[0] += d/2
            points[1] += d/2
            q(points=points)
            sleep(0.05/2)
        for i in range(50*2):
            points[0] -= d/2
            points[1] -= d/2
            q(points=points)
            sleep(0.05/2)

def push(q):
    points = array([
        list(q.legs[0].position),list(q.legs[1].position),list(q.legs[2].position),list(q.legs[3].position)
    ])

    points[0][0] += 0.8
    points[0][1] += 0.2
    points[0][2] -= 0
    #
    points[1][0] -= 0.8
    points[1][1] += 0.2
    points[1][2] -= 0
    #
    points[2][0] = 0
    points[2][1] -= 1.2
    points[2][2] -= 0
    #
    points[3][0] +=1.8
    points[3][1] -=1.2
    points[3][2] = 1

    q(points=points)
    while 1:
        for i in linspace(0,-2):
            points.T[2] = i
            points[3][2] = 2.3+i
            q(points=points)
            sleep(0.05)
        for i in linspace(-2,0):
            points.T[2] = i
            points[3][2] = 2.3+i
            q(points=points)
            sleep(0.05)


def push_1(q):
    points = array([
        list(q.legs[0].position),list(q.legs[1].position),list(q.legs[2].position),list(q.legs[3].position)
    ])

    points[0][0] = 0
    points[0][1] += 1
    points[0][2] -= 0
    #
    points[1][0] = 0.4
    points[1][1] += 0
    points[1][2] += 0.4
    #
    points[2][0] -= 1.2
    points[2][1] -= 2
    points[2][2] -= 0
    #
    points[3][0] +=1.2
    points[3][1] -= 2
    points[3][2] -= 0

    q(points=points)

    d = array([0,-0.01,-0.05])
    while 1:
        for i in range(50*2):
            points[0] += d/2
            q(points=points)
            sleep(0.05/2)
        for i in range(50*2):
            points[0] -= d/2
            q(points=points)
            sleep(0.05/2)

if __name__ == "__main__":
    MyQuadrupet = QModel( *default )
    MyQuadrupet.set_updater(set_angles)

    try:
        push(MyQuadrupet)
    except KeyboardInterrupt:
        pass
