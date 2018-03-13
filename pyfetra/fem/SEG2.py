from .ElemSkeleton import Element
from ..tools import Factory

class Seg2(Element):
    def __init__(self):
        Element.__init__(self)
        self._type = "TRI3"
        



class Seg2MechSmallStrain(Seg2):
    def __init__(self):
        Seg2.__init__(self)
        self._type = "TRI3"


# Register Tri3MechSmallDef in the object factory

Factory.Register("Element", Seg2MechSmallStrain, "SEG2MechSmallStrain")
