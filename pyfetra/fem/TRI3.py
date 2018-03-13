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
