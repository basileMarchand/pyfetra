
from .behavior import Behavior
from ..tools import Factory

class LinearElastic(Behavior):
    def __init__(self):
        Behavior.__init__(self)
        

    def setGroup(self, group):
        self._group = group

    def installRequires(self):
        #self._require = {"grad":["eto","deto"],
        #                 "flux":["sig",],
        #                 "aux" :[]}
        self._coeffs_req = ["elasticity",]
        self._require = ["eto","sig"]


    def integrate( self, deto ):
        self._data["eto"][:,:] = self._data["eto_ini"] + deto
        self._data["sig"][:,:] = self._elasticity.dot( self._data["eto"] )
        tgt = self._elasticity
        return tgt


# Register behavior in the object factory 
Factory.Register("Behavior", LinearElastic, "linear_elastic")
