import numpy  as np

import scipy.linalg as spl

from .ElemSkeleton import Element
from ..tools import Factory, myInv3, myDet3

class Tet4(Element):
    def __init__(self):
        Element.__init__(self)
        self._type = "TET4"




class Tet4MechSmallStrain(Tet4):
    def __init__(self):
        Tet4.__init__(self)
        self._type = "TET4"
        self._nnodes = 4
        self._ndofByNode = 3
        self._dofsByNode = ["U1","U2","U3"]

    def initIntegRule(self):
        self._ngp = 4
        a  = (5.-5.**0.5)/(20.)
        b  = (5.+3*5.**0.5)/(20.)
        p  = 1./24.
        self._gx = ((a,a,a),(a,a,b),(a,b,a),(b,a,a))
        self._gw = (p, p, p, p)

    def jacobian(self, ip):
        dN = np.array([[0.,1.,0.],
                       [0.,0.,1.],
                       [-1.,-1.,-1.],
                       [1.,0.,0.]])

        j = self._coors.T.dot(dN)
        return abs(myDet3( j ))
        
    def jacobianInv(self, ip):
        dN = np.array([[0.,1.,0.],
                       [0.,0.,1.],
                       [-1.,-1.,-1.],
                       [1.,0.,0.]])

        j = self._coors.T.dot(dN)
        return myInv3( j )



    def shape(self, ip):
        a = self._gx[ip]
        N = np.array([[a[1], 0, 0],
                      [0, a[1], 0],
                      [0, 0, a[1]],
                      [a[2], 0, 0],
                      [0, a[2], 0],
                      [0, 0, a[2]],
                      [1-a[0]-a[1]-a[2], 0, 0],
                      [0, 1-a[0]-a[1]-a[2], 0],
                      [0, 0, 1-a[0]-a[1]-a[2]],
                      [a[0], 0, 0],
                      [0, a[0], 0],
                      [0, 0, a[0]]])
        return N

    def grad(self, ip):
        dN  = np.array([[0.,1.,0.],
                        [0.,0.,1.],
                        [-1.,-1.,-1.],
                        [1.,0.,0.]])
        j_inv = self.jacobianInv(ip)
        Gn = dN.dot(j_inv)
        B = np.array([[Gn[0,0], 0., 0., Gn[0,1], 0., Gn[0,2]],
                      [0., Gn[0,1], 0., Gn[0,0], Gn[0,2], 0.],
                      [0., 0., Gn[0,2], 0., Gn[0,1], Gn[0,0]],
                      [Gn[1,0], 0., 0., Gn[1,1], 0., Gn[1,2]],
                      [0., Gn[1,1], 0., Gn[1,0], Gn[1,2], 0.],
                      [0., 0., Gn[1,2], 0., Gn[1,1], Gn[1,0]],
                      [Gn[2,0], 0., 0., Gn[2,1], 0., Gn[2,2]],
                      [0., Gn[2,1], 0., Gn[2,0], Gn[2,2], 0.],
                      [0., 0., Gn[2,2], 0., Gn[2,1], Gn[2,0]],
                      [Gn[3,0], 0., 0., Gn[3,1], 0., Gn[3,2]],
                      [0., Gn[3,1], 0., Gn[3,0], Gn[3,2], 0.],
                      [0., 0., Gn[3,2], 0., Gn[3,1], Gn[3,0]]])
        return B




        

# Register Tet4MechSmallDef in the object factory

Factory.Register("Element", Tet4MechSmallStrain, "TET4MechSmallStrain")
