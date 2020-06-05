import numpy as np

from pyfetra.fem import Element
from pyfetra.fem import GetIntegrator, GetInterpolator
from pyfetra.tools import Factory

class Seg2Nodes(Element):
    def __init__(self):
        super(Seg2Nodes,self).__init__()
        self._type = "SEG2"
        self._nnodes = 2
        self._ndofByNode = None
        self._dofsByNode = None


class Seg2Thermal(Seg2Nodes):
    def __init__(self):
        super(Seg2Thermal, self).__init__()
        self._ndofByNode = 1
        self._dofsByNode = ["T",]
        self._integrator = GetIntegrator("SEG2PT")

Factory.Register("Element", Seg2Thermal, "SEG2Thermal")


class Seg2MechSmallStrain(Seg2Nodes):
    def __init__(self):
        super(Seg2MechSmallStrain, self).__init__()
        self._ndofByNode = 1
        self._dofsByNode = ["U1",]

        self._integrator = GetIntegrator("SEG2PT")
    
        

Factory.Register("Element", Seg2MechSmallStrain, "SEG2MechSmallStrain")
        
