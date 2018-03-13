
from .Behavior import Behavior


class KinematicEVP(Behavior):
    def __init__(self):
        Behavior.__init__(self)

    def components(self):
        self._require = {"grad":["eto","deto","eel","evi"],
                         "flux":["sig"],
                         "aux" :["alpha",]}

        self._require = {"eto", "sig", "evi", "alpha"}


    def integrate(self, deto):
        
        

        for( i in range(100) ):
            f, jac = self.materialJacobian(deto)
            jac = np.eyes(jac.shape[0]) - jac*dt
            res = dt*f - dy
            ddy = np.linalg.solve(jac, res)
            dy  += ddy
            if( norm(res) < 1.e-10 ):
                break
        tgt = None
        return tgt


    def materialJacobain(self, deto):
        

        return None


        

