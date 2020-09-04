import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from QModel import QModel
import numpy as np
from webot_controller import set_angles
from configs import webot_mantis, my_quad

def draw_target(target_points):
    for point in target_points:
        glBegin(GL_LINES)
        glColor3ub(255,0,0)
        glVertex3fv(point + [-1,0,0])
        glVertex3fv(point + [1,0,0])
        glVertex3fv(point + [0,-1,0])
        glVertex3fv(point + [0,1,0])
        glVertex3fv(point + [0,0,-1])
        glVertex3fv(point + [0,0,1])
        glEnd()

def draw_legs(legs):
    for leg in legs:
        glBegin(GL_LINES)
        glColor3ub(255,255,255)
        for joint_a, joint_b in zip(leg[:-1],leg[1:],):
            glVertex3fv(joint_a)
            glVertex3fv(joint_b)
        glEnd()

def draw_body(legs):
    glBegin(GL_LINES)
    glColor3ub(0,0,255)
    for leg_no in range(4):
        glVertex3fv(legs[leg_no][0])
        glVertex3fv(legs[(leg_no+1)%4][0])
    glEnd()

def main():

    MyQuadrupet = QModel( *webot_mantis )
    # MyQuadrupet.train(epochs=6)
    # MyQuadrupet.load('webot_nn_ik')

    angles = [[0,1,-2],[0,1,-2],[0,1,-2],[0,1,-2]]
    angle_delta = 0.02

    clock = pygame.time.Clock()
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(60, (display[0]/display[1]), 0.1, 150.0)
    glTranslatef(0, -10, -30)
    glRotatef(90, -1, 0, 0)

    running = True
    key_down = set()
    target_points = []
    while running:
        # Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if len(target_points) == 0:
                        target_angles = np.random.uniform( size=(4,3), low=-np.pi*0.4, high=np.pi*0.4 )
                        target_points = [p[-1] for p in MyQuadrupet.fk(target_angles)]
                        angles        = MyQuadrupet.ik(target_points)
                    else:
                        target_points = []
                else:
                    key_down.add(event.key)
            if event.type == pygame.KEYUP:
                try: key_down.remove(event.key)
                except Exception as e: pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: glTranslatef(0,0,-1)
                if event.button == 5: glTranslatef(0,0,1)
        # Camera
        if pygame.K_LEFT in key_down: glRotatef(3, 0, 0, -1)
        if pygame.K_RIGHT in key_down: glRotatef(3, 0, 0, 1)
        if pygame.K_UP in key_down: glRotatef(3, 0, 1, 0)
        if pygame.K_DOWN in key_down: glRotatef(3, 0, -1, 0)

        # Manual angle
        if pygame.K_q in key_down: angles[0][0] += angle_delta
        if pygame.K_a in key_down: angles[0][0] -= angle_delta
        if pygame.K_w in key_down: angles[0][1] += angle_delta
        if pygame.K_s in key_down: angles[0][1] -= angle_delta
        if pygame.K_e in key_down: angles[0][2] += angle_delta
        if pygame.K_d in key_down: angles[0][2] -= angle_delta
        if pygame.K_r in key_down: angles[1][0] += angle_delta
        if pygame.K_f in key_down: angles[1][0] -= angle_delta
        if pygame.K_t in key_down: angles[1][1] += angle_delta
        if pygame.K_g in key_down: angles[1][1] -= angle_delta
        if pygame.K_y in key_down: angles[1][2] += angle_delta
        if pygame.K_h in key_down: angles[1][2] -= angle_delta
        if pygame.K_u in key_down: angles[2][0] += angle_delta
        if pygame.K_j in key_down: angles[2][0] -= angle_delta
        if pygame.K_i in key_down: angles[2][1] += angle_delta
        if pygame.K_k in key_down: angles[2][1] -= angle_delta
        if pygame.K_o in key_down: angles[2][2] += angle_delta
        if pygame.K_l in key_down: angles[2][2] -= angle_delta
        if pygame.K_z in key_down: angles[3][0] += angle_delta
        if pygame.K_x in key_down: angles[3][0] -= angle_delta
        if pygame.K_c in key_down: angles[3][1] += angle_delta
        if pygame.K_v in key_down: angles[3][1] -= angle_delta
        if pygame.K_b in key_down: angles[3][2] += angle_delta
        if pygame.K_n in key_down: angles[3][2] -= angle_delta

        # Simulate
        set_angles(angles)
        legs = MyQuadrupet.fk(angles)

        # Draw
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        draw_legs(legs)
        draw_target(target_points)
        draw_body(legs)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    quit()

main()
