import numpy as np



from pyfetra.fem.element import Element
from pyfetra.fem import GetIntegrator, GetInterpolator
from pyfetra.tools import Factory 


class Tetra4Nodes(Element):
    def __init__(self):
        super(Tetra4Nodes, self).__init__()
        self._type = "TET4"
        self._nnodes = 4
        self._ndofByNode = None
        self._dofsByNode = None

    
class Tetra4Thermal(Tetra4Nodes):
    def __init__(self):
        super(Tetra4Thermal, self).__init__()
        self._ndofByNode = 1
        self._dofsByNode = ['T',]
    
        self._integrator = GetIntegrator("TETRA4PT")
        self._interpolator = GetInterpolator("TETRA4NODES")
        

    def shape( self, ip ):
        _, x = self._integrator[ip]
        return self.shape( x )

    def grad( self, ip ):
        _, x = self._integrator[ip]
        return self._interpolator.dshape_dx(x, self._coors )


Factory.Register("Element", Tetra4Thermal, "TET4Thermal")

    
class Tetra4MechSmallStrain(Tetra4Nodes):
    def __init__(self):
        super(Tetra4MechSmallStrain, self).__init__()
        self._ndofByNode = 3
        self._dofsByNode = ['U1', 'U2', 'U3']
    
        self._integrator = GetIntegrator("TETRA4PT")
        self._interpolator = GetInterpolator("TETRA4NODES")
    
    def shape( self, ip ):
        _, x = self._integrator[ip]
        N = self._interpolator.shape( x )
        ret = np.zeros((12, 3 ) )
        ret[::3, 0] = N
        ret[1::3, 1] = N
        ret[2::3, 2] = N
        return ret

    def grad( self, ip ):
        _, x = self._integrator[ip]
        dNdX = self._interpolator.dshape_dx( x, self._coors)
        g = np.zeros((6,12))
        g[0,::3] = dNdX[0,:]
        g[1,1::3] = dNdX[1,:]
        g[2,2::3] = dNdX[2,:]
        g[3,0] = dNdX[1,0] ; g[3,1] = dNdX[0,0]
        g[3,3] = dNdX[1,1] ; g[3,4] = dNdX[0,1]
        g[3,6] = dNdX[1,2] ; g[3,7] = dNdX[0,2]
        g[3,9] = dNdX[1,3] ; g[3,10] = dNdX[0,3]

        g[4,1] = dNdX[2,0] ; g[4,2] = dNdX[1,0]
        g[4,4] = dNdX[2,1] ; g[4,5] = dNdX[1,1]
        g[4,7] = dNdX[2,2] ; g[4,8] = dNdX[1,2]
        g[4,10] = dNdX[2,3] ; g[4,11] = dNdX[1,3]

        g[5,0] = dNdX[2,0] ; g[5,2] = dNdX[0,0]
        g[5,3] = dNdX[2,1] ; g[5,5] = dNdX[0,1]
        g[5,6] = dNdX[2,2] ; g[5,8] = dNdX[0,2]
        g[5,9] = dNdX[2,3] ; g[5,11] = dNdX[0,3]
        return g

Factory.Register("Element", Tetra4MechSmallStrain, "TET4MechSmallStrain")
