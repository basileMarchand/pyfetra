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


        

