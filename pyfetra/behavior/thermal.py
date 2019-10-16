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


class Thermal(Behavior):
    def __init__(self):
        super(Thermal, self).__init__()

    def installRequires(self):
        self._coeffs_req = ["conductivity",]
        self._dual = "q"
        self._require = [("gradT","vector"), ("q", "vector")]
        
    def integrate(self, delta_grad ):
        self._data["gradT"][:,:] = self._data["gradT_ini"] + delta_grad
        self._data["q"][:,:] = self._conductivity.dot( self._data["gradT"] )
        tgt = self._conductivity
        return tgt
