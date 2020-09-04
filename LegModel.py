#!/usr/bin/env python3
import numpy as np

class LegModel:
    @staticmethod
    def default_forward_kinetics(length,position,angle_base):
        '''Simple kinetics for leg of spier like robot'''
        def inner(angle):
            output = np.zeros( (len(angle)+1 , 3) )
            angle = np.array(angle,dtype=np.float)
            angle += angle_base
            # Base
            output[0] += position
            # Apply 1st angle
            output[1] += output[0] + [
                np.cos(angle[0])*length[0],
                np.sin(angle[0])*length[0],
                0.0
            ]
            # Apply 2nd angle
            output[2] += output[1] + [
                np.cos(angle[0]) * length[1] * np.cos(angle[1]),
                np.sin(angle[0]) * length[1] * np.cos(angle[1]),
                np.sin(angle[1]) * length[1]
            ]
            # Apply 3nd angle
            output[3] += output[2] + [
                np.cos(angle[0]) * length[2] * np.cos(angle[1]+angle[2]),
                np.sin(angle[0]) * length[2] * np.cos(angle[1]+angle[2]),
                np.sin(angle[1]+angle[2]) * length[2]
            ]
            return output
        return inner

    def __init__(
            self,
            length,position,angle_base,
            forward_kinetics=None
        ):
        self.lengths,self.position,self.angle_base = length,position,np.array(angle_base)
        self.forward_kinetics = forward_kinetics if forward_kinetics else self.default_forward_kinetics(length,position,angle_base)
        self.current = np.zeros_like(angle_base)

    def __call__(self,*args,**kwargs):
        return self.inverse_kinetics(*args,**kwargs)

    def inverse_kinetics(self,target,max_iter = 6,starting_angles = None,update=True,__cache={}):
        if not __cache:
            dim = len(self.angle_base)
            num = 3
            modes  = np.empty( (num**dim,dim)  )
            values = np.linspace(-np.pi,np.pi,num)*0.2
            for i in range(modes.shape[0]):
                for d in range(dim):
                    modes[i][d] = values[( i//(dim**d) )%num]
            __cache['modes'] = modes
        if starting_angles is not None:
            angles = np.array(starting_angles)
        else:
            angles = self.current.copy()
        modes = __cache['modes'].copy()
        target = np.array(target)
        for iter in range(max_iter):
            ds = np.array([
                np.sqrt(((target - self.forward_kinetics(angles + m)[-1])**2).sum())
                for m in modes
            ])
            d = ds.argmin()
            angles += modes[d]
            angles[angles > np.pi] -= np.pi
            angles[angles < -np.pi] += np.pi
            modes *= 0.5
        if update:
            self.current = angles
        return angles

    def test(self):
        import datetime
        y = np.random.uniform(low=-np.pi*0.8, high=np.pi*0.8, size=(300,3))
        x = np.empty( (y.shape[0],3) )
        for i in range(y.shape[0]):
            x[i] = self.forward_kinetics(y[i])[-1]
        time_sum = 0.
        diff_sum = 0.
        for xp in x:
            start = datetime.datetime.now()
            e = self.inverse_kinetics(xp,max_iter=8,update=False)
            end = datetime.datetime.now()
            xe = self.forward_kinetics(e)[-1]
            time_sum += (end-start).total_seconds()
            diff_sum += np.sqrt(((xp - xe)**2).sum())
        time_sum *= 1000/len(x)
        diff_sum /= len(x)
        print(time_sum,diff_sum)

    def show_plots(self,legs=True,missmatch=True):
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D

        if legs or missmatch:
            y = np.random.uniform(low=-np.pi*0.8, high=np.pi*0.8, size=(5,3))
            x = np.empty( (y.shape[0],3) )
            for i in range(y.shape[0]):
                x[i] = self.forward_kinetics(y[i])[-1]
            yp = []
            time_sum = 0
            for xp in x:
                start = datetime.datetime.now()
                e = self.inverse_kinetics(xp)
                end = datetime.datetime.now()
                time_sum += (end-start).total_seconds()
                yp.append(e)

            print("Mean time for calculation: {}".format(time_sum/len(x)))

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            for real_target,predictet_angles in zip(x,yp):
                leg_joints = self.forward_kinetics(predictet_angles)
                if legs:
                    ax.plot3D(
                        [joint[0] for joint in leg_joints ],
                        [joint[1] for joint in leg_joints ],
                        [joint[2] for joint in leg_joints ],
                        'o-r'
                    )
                if missmatch:
                    ax.plot3D(
                        [real_target[0], leg_joints[-1][0] ],
                        [real_target[1], leg_joints[-1][1] ],
                        [real_target[2], leg_joints[-1][2] ],
                        'o-g'
                    )
                    ax.quiver3D(
                        [leg_joints[-1][0] ],
                        [leg_joints[-1][1] ],
                        [leg_joints[-1][2] ],
                        [real_target[0] - leg_joints[-1][0]],
                        [real_target[1] - leg_joints[-1][1]],
                        [real_target[2] - leg_joints[-1][2]]
                    )

            plt.title('Simulation')
        plt.show()
if __name__ == "__main__":
    TestLeg = LegModel(
        (3,4,8),
        (2.5,4.5,0),
        np.deg2rad((30,0,0))
    )
    TestLeg.test()
    TestLeg.show_plots()
