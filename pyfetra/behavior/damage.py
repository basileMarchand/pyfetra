#==============================================================================
# Copyright (C) 2018 Marchand Basile
# 
# This file is part of pyfetra.
# 
# pyfetra is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# pyfetra is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with pyfetra.  If not, see <http://www.gnu.org/licenses/>
#==============================================================================



from .behavior import Behavior
from ..tools import Factory
import numpy as np

class ElasticDamage(Behavior):
    def __init__(self):
        Behavior.__init__(self)
        
    def installRequires(self):
        self._coeffs_req = ["elasticity"]
        self._dual = "sig"
        self._require = [("eto", "tensor2"),("sig", "tensor2"), ("Y", "scalar"), ("d", "scalar"), ("Y_max", "scalar")]

    def setParameters(self, y0, alpha, dmax=0.99):
        self._y0 = y0
        self._alpha = alpha
        self._dmax = dmax

    def integrate( self, deto ):
        self._data["eto"][:,:] = self._data["eto_ini"] + deto
        sig0 = self._elasticity.dot( self._data["eto"] )
        
        energy = np.sum(sig0*self._data["eto"][:,:])
        self._data["Y"][:,:] = energy
        active=False
        if energy > self._data["Y_max_ini"][0]:
            self._data["Y_max"] = energy 
            active = True
        else:
            self._data["Y_max"] = energy 

        ym_sqrt = energy**0.5
        y0_root = self._y0**0.5
        
        if ym_sqrt <= y0_root:
            d = self._data["d_ini"][:,:]
        else:
            d = self._data["d_ini"][:,:]+ self._alpha * ( ym_sqrt - y0_root )

        if d > self._dmax :
            d = self._dmax
        
        self._data["d"][:,:] = d
        self._data["sig"][:,:] = (1 - d )* self._elasticity.dot( self._data["eto"] )
        tgt = (1 - d )*self._elasticity
        if active:
            tgt -= 0.5*self._alpha/ym_sqrt * ( 1./ ((1-d)**2 ) ) * self._data["sig"][:,:].dot( self._data["sig"][:,:].T )
        return tgt


# Register behavior in the object factory 
Factory.Register("Behavior", ElasticDamage, "elastic_damage")
