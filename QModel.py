from numpy import array,sign,linspace,pi
from threading import Thread
from LegModel import LegModel
from time import sleep

class QModel(Thread):
    def __init__(self,legs_lengths,legs_positions,legs_base_angles,*args,**kwargs):
        assert len(legs_lengths)==len(legs_positions)==len(legs_base_angles), "Number of legs missmatch"
        super().__init__(*args,**kwargs)
        self.legs = [
            LegModel(length, position, angle_base)
            for length, position, angle_base
            in zip(legs_lengths,legs_positions, legs_base_angles)
        ]
        self._updater = None
        self.__input = None
        self.__walk_phase = 0.
        self.__updates_per_phase = 25
        self.__gaint_offset = array([2,0.5,-1.])
        self.__gaint_offset_up = 0.75
        self.__d = 8
        self.__ds = (self.__d-1.)/self.__d
        self.__legs_shift = [0. , 0.75, 0.50, 0.25]
        def _sign(x):
            t = sign(x)
            t[t==0] = 1
            return t
        self.gaint_pattern_base = array([
            [
                leg.position + (_sign(leg.position)*self.__gaint_offset ),
                leg.position + (_sign(leg.position)*self.__gaint_offset )
            ]
            for leg in self.legs
        ])
        self.gaint_pattern_base = array([
            [
                _sign(leg.position)*[4,4,-1.],
                _sign(leg.position)*[4,4,-1.]
            ]
            for leg in self.legs
        ])
        self.rotate_d = array([
            [ [-1,1],[1,-1] ],
            [ [-1,-1],[1,1] ],
            [ [1,-1],[-1,1] ],
            [ [1,1],[-1,-1] ],
        ])*-1
        self.rotate_h = array([
            [1,1],[-1,1],[-1,-1],[1,-1]
        ])
        self.advance_max, self.side_max, self.rotate_max = 1.3,.75,.5



    def set_updater(self,fnc):
        self._updater = fnc

    def set_user_input(self,inp):
        self.__input = inp

    def fk(self,angles,*args,**kwargs): return [ leg.forward_kinetics(angle,*args,**kwargs) for leg,angle in zip(self.legs,angles)]
    def ik(self,points,update=True,*args,**kwargs): return array([ leg.inverse_kinetics(point,update=update,*args,**kwargs) for leg,point in zip(self.legs,points)  ])

    def __call__(self,points=None,angles=None,update=True,*args,**kwargs):
        if self._updater:
            if points is not None:
                return self._updater(self.ik(points,update=update,*args,**kwargs))
            elif angles is not None:
                if update:
                    for leg,angle in zip(self.legs, angles):
                        leg.current = angle
                return self._updater(angles)
        else: raise Exception('Set updater first!')

    def run(self):
        # Init walk
        ## Each leg center point
        gaint_pattern = self.gaint_pattern_base.copy()
        ## Calculate each leg angles for center point and go there
        legs_base_angles = array([
            leg(target=gp[0],starting_angles=[0.,1.,-2.])
            for leg,gp in zip(self.legs,gaint_pattern)
        ])
        ## Calculate update interval, steps ect.
        interval = 1 / self.__updates_per_phase
        phase_steps = linspace(0,1,self.__updates_per_phase)
        ## Stare input reader
        self.__input.start()
        ## Get current input state
        last_state = self.__input.state
        # Main loop
        while True:
            if len(self.__input.button_down)==0:
                for phase_step in phase_steps:
                    ## Get input
                    state = self.__input.state
                    ## Do we need to update gaint pattern
                    if last_state != state:
                        advance, side, rotate, height, gx, gy = state
                        ## OK, lets update
                        gaint_pattern = self.gaint_pattern_base.copy()
                        for gp,rd,rh in zip(gaint_pattern,self.rotate_d,self.rotate_h):
                            gp[0][1] += advance*self.advance_max
                            gp[1][1] -= advance*self.advance_max
                            gp[0][0] += side*self.side_max
                            gp[1][0] -= side*self.side_max
                            gp[0][0] += rotate*self.rotate_max*rd[0][0]
                            gp[0][1] += rotate*self.rotate_max*rd[0][1]
                            gp[1][0] += rotate*self.rotate_max*rd[1][0]
                            gp[1][1] += rotate*self.rotate_max*rd[1][1]
                            gp[0][2] = -height*2.5
                            gp[1][2] = -height*2.5

                            gp[0][0] += gx
                            gp[1][0] += gx
                            gp[0][1] += gy
                            gp[1][1] += gy

                            # gp[0][2] += rh[0]*gx + rh[1]*gy
                            # gp[1][2] += rh[0]*gx + rh[1]*gy

                        legs_base_angles = array([
                            leg(target=gp[0],starting_angles=[0.,1.,-2.])
                            for leg,gp in zip(self.legs,gaint_pattern)
                        ])
                        last_state = state
                    ## Do we have any velocity
                    all_angels = []
                    if state[0] != 0 or state[1] != 0 or state[2] != 0:
                        ### OK, lets move to new angles
                        for leg,leg_shift,gp,leg_base_angles in zip(self.legs,self.__legs_shift,gaint_pattern,legs_base_angles):
                            leg_phase = leg_shift + phase_step
                            if leg_phase> 1.: leg_phase-=1
                            if leg_phase > self.__ds:
                                leg_p,leg_up = -self.__d*leg_phase+self.__d, True
                            else:
                                leg_p,leg_up = leg_phase/self.__ds, False
                            target = array([
                                gp[0][0]*(1.-leg_p) + gp[1][0]*leg_p,
                                gp[0][1]*(1.-leg_p) + gp[1][1]*leg_p,
                                gp[0][2]
                            ])
                            if leg_up: target[2] = 0 # self.__gaint_offset_up
                            angels = leg(target=target,starting_angles = leg_base_angles)
                            for a in angels: all_angels.append(a)
                        self._updater(all_angels)
                        sleep(interval)
                    else:
                        self._updater(legs_base_angles)
                        sleep(interval)
                        break
            else:
                angel = list(self.__input.state[0:3])
                angel = [-angel[2]*pi/2,-angel[0]*pi/2,angel[1]*pi/2]
                angels = legs_base_angles.copy()

                if 1 in self.__input.button_down:
                    angel[0] += 1
                    angel[1] += 1
                    angel[2] += -1
                    angels[0] = angel
                    angels[1][0] = -1.

                if 5 in self.__input.button_down:
                    angels[0] = angel
                if 4 in self.__input.button_down:
                    angels[1] = angel
                if 2 in self.__input.button_down:
                    angels[2] = angel
                if 3 in self.__input.button_down:
                    angels[3] = angel
                self._updater(angels)
                sleep(interval)
        self.__input.stop()

if __name__ == "__main__":
    from JoystickInput import JoystickInput
    from configs import my_quad as config
    from q_controller import set_angles

    try:
        MyQuadrupet = QModel(*config)
        MyQuadrupet.set_user_input(JoystickInput())
        MyQuadrupet.set_updater(set_angles)
        MyQuadrupet.start()

    except KeyboardInterrupt: pass
