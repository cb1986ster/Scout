#!/usr/bin/env python3
import os
import numpy as np
from threading import Thread

from LegModel import LegModel

from configs import webot_mantis, my_quad

class QModel:
    def __init__(self,legs_lengths,legs_positions,legs_base_angles,ik_ann=(12,15,12)):
        assert len(legs_lengths)==len(legs_positions)==len(legs_base_angles), "Number of legs missmatch"
        self.legs = [
            LegModel(length, position, angle_base, ik_ann=ik_ann)
            for length, position, angle_base
            in zip(legs_lengths,legs_positions, legs_base_angles)
        ]
        self._updater = None
    def set_updater(self,fnc):
        self._updater = fnc
    def __call__(self,points=None,angles=None):
        if self._updater:
            if points:
                return self._updater(self.ik(points))
            elif angles:
                return self._updater(angles)
            else:
                raise Exception('Set updater first!')
    def train(self,sequential=False,*args,**kwargs):
        if sequential:
            for leg in self.legs:
                leg.train(*args,**kwargs)
        else:
            kwargs['verbose'] = 0
            threads = [Thread(target=leg.train, args=args, kwargs=kwargs) for leg in self.legs]
            [ t.start() for t in threads ]
            print('Treads started...')
            [ t.join() for t in threads ]
            print('All threads join')

    def fk(self,angles):
        return [
            leg.forward_kinetics(angle) for leg,angle in zip(self.legs,angles)
        ]

    def ik(self,points):
        return [
            leg.inverse_kinetics(np.array([point]))[0] for leg,point in zip(self.legs,points)
        ]

    def save(self,directory):
        os.makedirs(directory,exist_ok=True)
        for leg_no,leg in enumerate(self.legs):
            leg.save_weights('{}/leg_{}.h5'.format(directory,leg_no))

    def load(self,directory):
        os.makedirs(directory,exist_ok=True)
        for leg_no,leg in enumerate(self.legs):
            leg.train(epochs=1,samples=1)
            leg.load_weights('{}/leg_{}.h5'.format(directory,leg_no))


if __name__ == "__main__":
    try:
        MyQuadrupet = QModel(*webot_mantis)
        MyQuadrupet.train(epochs=50,samples=10_000,sequential=True)

    except KeyboardInterrupt:
        pass
    MyQuadrupet.save('webot_nn_ik')
