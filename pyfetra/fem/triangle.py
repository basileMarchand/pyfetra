import numpy as np


from pyfetra.fem.element import Element
from pyfetra.fem import GetIntegrator, GetInterpolator
from pyfetra.tools import Factory, myDet2

class Triangle3Nodes(Element):
    def __init__(self):
        super(Triangle3Nodes, self).__init__()
        self._type = "TRI3"
        self._nnodes = 3
        self._ndofByNode = None
        self._dofsByNode = None

    def det(self, mat):
        return myDet2(mat)

class Triangle3Thermal(Triangle3Nodes):
    def __init__(self):
        super(Triangle3Thermal, self).__init__()
        self._ndofByNode = 1
        self._dofsByNode = ['T',]

        self._integrator = GetIntegrator("TRI1PT")
        self._interpolator = GetInterpolator("TRI3NODES")
        

    def shape( self, ip ):
        _, x = self._integrator[ip]
        return self.shape( x )

    def grad( self, ip ):
        _, x = self._integrator[ip]
        return self._interpolator.dshape_dx(x, self._coors[:,:2] )
    
Factory.Register("Element", Triangle3Thermal, "TRI3Thermal")

class Triangle3MechSmallStrain(Triangle3Nodes):
    def __init__(self):
        super(Triangle3MechSmallStrain, self).__init__()
        self._ndofByNode = 2
        self._dofsByNode = ['U1','U2']

        self._integrator = GetIntegrator("TRI1PT")
        self._interpolator = GetInterpolator("TRI3NODES")

    def shape( self, ip ):
        _, x = self._integrator[ip]
        N = self._interpolator.shape( x )
        ret = np.zeros((6,2))
        ret[::2, 0] = N
        ret[1::2, 1] = N
        return ret

    def grad( self, ip ):
        _, x = self._integrator[ip]
        dNdX = self._interpolator.dshape_dx(x, self._coors[:,:2] )
        g = np.zeros((3,6))
        g[0,0] = dNdX[0,0] ; g[0,2] = dNdX[0,1] ; g[0,4] = dNdX[0,2]
        g[1,1] = dNdX[1,0] ; g[1,3] = dNdX[1,1] ; g[1,5] = dNdX[1,2]
        g[2,0] = dNdX[1,0] ; g[2,1] = dNdX[0,0] ; g[2,2] = dNdX[1,1]
        g[2,3] = dNdX[0,1] ; g[2,4] = dNdX[1,2] ; g[2,5] = dNdX[0,2]
        return g
        


Factory.Register("Element", Triangle3MechSmallStrain, "TRI3MechSmallStrain")
