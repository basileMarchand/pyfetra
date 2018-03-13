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




class Integrator:
    def __init__(self):
        self._scheme = ""
        self._t0     = 0.
        self._dt     = 0.
        
    def setOptions( opt ):
        raise NotImplementedError

    def setTime(self, t0, dt):
        pass

    def setInit(self, xInit ):
        pass

    def integrate( mat ):
        raise NotImplementedError

    
class ImplicitIntegrator(Integrator):
    def __init__(self):
        Integrator.__init__(self)
        self._scheme = "implicit"

    

class ExplicitIntegrator(Integrator):
    def __init__(self):
        Integrator.__init__(self)
        self._scheme = "explicit"


