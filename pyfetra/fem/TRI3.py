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


from .ElemSkeleton import Element
from ..tools import Factory

class Tri3(Element):
    def __init__(self):
        Element.__init__(self)
        self._type = "TRI3"
        



class Tri3MechSmallStrain(Tri3):
    def __init__(self):
        Tri3.__init__(self)
        self._type = "TRI3"



# Register Tri3MechSmallDef in the object factory

Factory.Register("Element", Tri3MechSmallStrain, "TRI3MechSmallStrain")
