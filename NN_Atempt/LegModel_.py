#!/usr/bin/env python3
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
keras = tf.keras
Model = keras.Model
Dense, Dropout, Flatten = keras.layers.Dense ,keras.layers.Dropout ,keras.layers.Flatten
sin, cos, concatenate = keras.backend.sin, keras.backend.cos, keras.backend.concatenate

import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class ExamplesGenerator(keras.utils.Sequence):
    def __init__(self,leg,batch_size = 32, batch_number = 1000):
        self.leg, self.batch_size, self.batch_number = leg, batch_size, batch_number
        self.x_size = (self.batch_size,3)
        self.__random_param = {'low':-np.pi*0.9, 'high':np.pi*0.9, 'size':(self.batch_size,len(self.leg.angle_base))}
        self.__range = range(self.batch_size)
    def __len__(self):
        return self.batch_number
    def __getitem__(self, idx):
        y = np.random.uniform(**self.__random_param)
        x = np.empty( self.x_size )
        for i in self.__range:
            x[i] = self.leg.forward_kinetics(y[i])[-1]
        return (x,y)

class LegModel(Model):
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

    @staticmethod
    def __identity__(x,*args,**kwargs):return x
    def _normalize_angle(self,angle):   return angle/(np.pi*0.7)
    def _unnormalize_angle(self,angle): return angle*(np.pi*0.7)
    def _normalize_point(self,point):   return 2*(point-self.position)/self.full_radius
    def _unnormalize_point(self,point): return (point*self.full_radius/2)+self.position

    def __init__(
            self,
            length,position,angle_base,
            forward_kinetics=None,
            ik_ann=(12,15,12),loss='mae',keep_rate=0.07,
            activation='relu', output_activation=None,
            use_normalisation = False, use_radial = False
        ):
        super(LegModel, self).__init__()
        self.lengths,self.position,self.angle_base = length,position,angle_base
        self.forward_kinetics = forward_kinetics if forward_kinetics else self.default_forward_kinetics(length,position,angle_base)

        self.ik_ann = [ (Dense(w,activation=activation),Dropout(keep_rate)) for w in ik_ann ]
        self.ik_ann.append( (Dense(len(angle_base), activation=output_activation),self.__identity__) )

        if use_radial:
            def expander_radial(x,*args,**kwargs): return concatenate((x,sin(x),cos(x)))
            self.ik_ann.insert(0, (expander_radial,self.__identity__) )

        if use_normalisation:
            self.ik_ann.insert(0, (self._normalize_point,self.__identity__) )
            self.ik_ann.append( (self._unnormalize_angle,self.__identity__) )

        self.full_radius = sum(self.lengths)

        self.compile(optimizer='adam',loss=loss)

    def inverse_kinetics(self,*args,**kwargs):
        return self(*args,**kwargs).numpy()

    def call(self, x, training=False):
        if training:
            for layer,wrapper in self.ik_ann:
                x=wrapper(layer(x),training=True)
        else:
            for layer,wrapper in self.ik_ann:
                x=layer(x)
        return x
    def train(self,**kwargs):
        # return self.train_random(**kwargs)
        return self.train_generator(**kwargs)
        # return self.train_normfill(**kwargs)

    def train_generator(self,batch_size=32,batch_number=1000,**kwargs):
        return self.fit( ExamplesGenerator(self,batch_size,batch_number), **kwargs)

    def train_normfill(self, num=20, **kwargs):
        dim = len(self.angle_base)
        y = np.empty( (num**dim,dim)  )
        values = np.linspace(-np.pi*0.9,np.pi*0.9,num)
        for i in range(y.shape[0]):
            for d in range(dim):
                y[i][d] = values[( i//(dim**d) )%num]
        np.random.shuffle(y)
        x = np.empty( (y.shape[0],3) )
        for i in range(x.shape[0]):
            x[i] = self.forward_kinetics(y[i])[-1]
        return self.fit(x=x,y=y,validation_data=(x,y),**kwargs)

    def train_random( self, samples = 10_000,  **kwargs):
        y = np.random.uniform(low=-np.pi*0.9, high=np.pi*0.9, size=(samples,len(self.angle_base)))
        val_y = np.random.uniform(low=-np.pi*0.9, high=np.pi*0.9, size=(samples//10,len(self.angle_base)))

        # True points for angles
        x = np.empty( (y.shape[0],3) )
        for i in range(y.shape[0]): x[i] = self.forward_kinetics(y[i])[-1]
        val_x = np.empty( (val_y.shape[0],3) )
        for i in range(val_y.shape[0]): val_x[i] = self.forward_kinetics(val_y[i])[-1]

        return self.fit(x=x,y=y,validation_data=(val_x,val_y),**kwargs)

    def show_plots(self,legs=True,missmatch=True,loss=True):
        if loss:
            labels = []
            for label,y in self.history.history.items():
                plt.plot(range(1,len(y)+1),y)
                labels.append(label)
            plt.legend(labels)
            plt.title('Learning')

        if legs or missmatch:
            y = np.random.uniform(low=-np.pi*0.8, high=np.pi*0.8, size=(7,3))
            x = np.empty( (y.shape[0],3) )
            for i in range(y.shape[0]):
                x[i] = self.forward_kinetics(y[i])[-1]
            yp = self(x)

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
    def export(self):
        return {
            'w':[ e.numpy() for e in self.weights[::2]],
            'b':[ e.numpy() for e in self.weights[1::2]]
        }
    def load_weights(self,*args,**kwargs):
        TestLeg.build(input_shape=(None,len(self.angle_base)))
        super().load_weights(*args,**kwargs)

if __name__ == "__main__":
    with tf.device("GPU:0"):
        try:
            TestLeg = LegModel(
                (3,4,8),
                (2.5,4.5,0),
                np.deg2rad((30,0,0)),
                ik_ann = (32,24,16,12,8),
                use_radial = True,
                use_normalisation = True,
                activation='tanh'
            )
            # try: TestLeg.load_weights('noga.h5')
            # except Exception: print("Nie udało się wczytać.")
            last_epoch = 0
            epoch = 4
            loss = []
            while True:
                # TestLeg.train(epochs=last_epoch+epoch,initial_epoch=last_epoch,verbose=2)
                TestLeg.train_normfill(epochs=last_epoch+epoch,initial_epoch=last_epoch,verbose=2)
                loss += TestLeg.history.history['loss']
                last_epoch += epoch
                if min(TestLeg.history.history['loss']) < 0.1:
                    break

        except KeyboardInterrupt:
            pass
        TestLeg.history.history['loss'] = loss
        TestLeg.save_weights('noga.h5')
        TestLeg.summary()
        TestLeg.show_plots()
