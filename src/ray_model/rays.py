from math import pi, cos, sin, acos, tan, log, sqrt, copysign
from collections import namedtuple
import numpy as np

SoundProp = namedtuple('SoundProp', 'z c a')

class AcousticField():
    def __init__(self, ps):
        self.props = [SoundProp(*row) for row in ps]

    def __iter__(self):
        for beta in np.linspace(-pi/2+0.1, -0.1, 50):
            ray = Ray(beta, self.props)
            yield ray.propagate()

class Ray():
    def __init__(self, beta_i, props):
        self.beta = beta_i
        self.props = props

    def propagate(self):
        layers = []
        for i in range(len(self.props)-1):
            layer = LinearVelocityLayer(self.beta, self.props[i], self.props[i+1])
            prop_result = layer.propagate()
            layers.append(prop_result)
            self.beta = prop_result['beta']
        return sum([x['dr'] for x in layers]), sum([x['tt'] for x in layers])

class LinearVelocityLayer():
    def __init__(self, beta_i, p_i, p_o):
        self.beta_i = beta_i
        self.zi, self.ci, _ = p_i
        self.zo, self.co, _ = p_o
        self.cg = (p_o.c-p_i.c)/(p_o.z-p_i.z)
        self.ag = (p_o.a-p_i.a)/(p_o.z-p_i.z)
        self.aoff = p_i.a-p_i.z*self.ag


    def propagate(self):

        if self.cg == 0:
            beta_o = self.beta_i
            dz = self.zo-self.zi
            dr = dz/tan(self.beta_i)
            ds = sqrt(dr**2+dz**2)
            tt = ds/self.ci
        else:
            self.rc = self.ci/(self.cg*cos(self.beta_i))
            beta_o = copysign(acos(self.co*cos(self.beta_i)/self.ci), self.beta_i)
            dr = self.rc*(sin(self.beta_i)-sin(beta_o))
            ds = self.rc*(self.beta_i-beta_o)

            tt = log((self.co*(1+sin(self.beta_i)))/(self.ci*(1+sin(beta_o))))/self.cg

        dabs = self.aoff*ds+self.ag*self.rc*(dr+(beta_o-self.beta_i)*(self.rc*cos(self.beta_i)-self.zi))
        return {
            'beta': beta_o,
            'dr':dr,
            'tt': tt,
            'ds': ds,
            'dabs': dabs
            }
