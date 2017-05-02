from math import sin, cos, acos, tan, sqrt, copysign, log

class Ray():
    def __init__(self, beta_i, izs, props):
        self.beta = beta_i
        self.props = props
        self.diz = 1 if beta_i > 0 else -1
        self.state = {
            'r': 0,
            'abs': 0,
            's': 0,
            'z': izs
        }

    def __iter__(self):
        return self

    def __next__(self):
        ind_from = self.state['z']
        ind_to = ind_from+self.diz
        #print(ind_from, ind_to)
        layer = LinVelLayer(self.props[ind_from], self.props[ind_to])
        result = layer.propagate(self.beta)
        if self.beta*result['beta'] < 0:
            self.diz *= -1
        else:
            self.state['z'] += self.diz
        self.beta = result['beta']
        self.state['r'] += result['dr']
        self.state['s'] += result['ds']
        self.state['abs'] += result['abs']
        return self.state

class LinVelLayer():
    def __init__(self, p_i, p_o):
        self.zi, self.ci, _ = p_i
        self.zo, self.co, _ = p_o
        self.cg = (p_o.c-p_i.c)/(p_o.z-p_i.z)
        self.a_av = (p_o.a+p_i.a)/2

    def propagate(self, beta_i):
        if self.cg == 0:
            beta_o = beta_i
            dz = self.zo-self.zi
            dr = dz/tan(beta_i)
            ds = sqrt(dr**2+dz**2)
            tt = ds/self.ci
        else:
            self.rc = self.ci/(self.cg*cos(beta_i))
            cbo = self.co*cos(beta_i)/self.ci
            if cbo > 1:
                beta_o = -beta_i
            else:
                beta_o = copysign(acos(cbo), beta_i)
            dr = self.rc*(sin(beta_i)-sin(beta_o))
            ds = self.rc*(beta_i-beta_o)
            tt = log((self.co*(1+sin(beta_i)))/(self.ci*(1+sin(beta_o))))/self.cg

        labs = ds*self.a_av

        return {
            'beta': beta_o,
            'dr':dr,
            'tt': tt,
            'ds': ds,
            'abs': labs
            }
