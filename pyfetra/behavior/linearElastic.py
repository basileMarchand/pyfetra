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

class LinearElastic(Behavior):
    def __init__(self):
        Behavior.__init__(self)
        
    def installRequires(self):
        self._coeffs_req = ["elasticity",]
        self._dual = "sig"
        self._require = [("eto", "tensor2"),("sig", "tensor2")]


    def integrate( self, deto ):
        self._data["eto"][:,:] = self._data["eto_ini"] + deto
        self._data["sig"][:,:] = self._elasticity.dot( self._data["eto"] )
        tgt = self._elasticity
        return tgt


# Register behavior in the object factory 
Factory.Register("Behavior", LinearElastic, "linear_elastic")
