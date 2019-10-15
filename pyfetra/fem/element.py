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


import numpy as np

class Element:
    def __init__(self):
        self._type = "FAKE"
        self._rank = 0
        self._coors= None
        self._connec=None
        self._ndofByNode=0
        self._dofsByNode=[]
        self._dofs = []
        self._nnodes = 0
        self._ndofs=0

        self._integrator = None
        self._interpolator = None

        """
        self._gx   = []
        self._gw   = []
        self._ngp  = 0
        """

    def nbDof(self):
        return self._ndofs

    def nbIntegPts(self):
        return len(self._integrator)

    def getDofs(self):
        return self._dofs

    def type(self):
        return self._type

    def setRank(self,rk):
        self._rank = rk

    def initIntegRule(self):
        """
        pure virtual method
        """
        pass

    def _internalInitialize(self):
        """
        callback method defined in the true element implementation if needed
        """
        pass

    def initializeDofs(self):
        self._ndofs = self._nnodes*self._ndofByNode
        self._dofs = [None]*(self._ndofs)
        for i, rk in enumerate(self._connec):
            for j in range(self._ndofByNode):

                self._dofs[i*self._ndofByNode+j] = rk*self._ndofByNode + j
 
    def setConnectivity(self, connec, nodes):
        self._connec = connec
        self._coors = np.zeros((len(connec), 3))
        for i,nid in enumerate(connec):
            self._coors[i,:] = nodes[nid,:]
        
        self._internalInitialize()
        self.initializeDofs()
        self.initIntegRule()

    def shape(self, ip ):
        raise NotImplementedError

    def grad(self, ip ):
        raise NotImplementedError

    def jacobian(self, ip ):
        raise NotImplementedError

    def weight(self, ip ):
        return self._gw[ip]

    def internalReactionAndTangent( self, pb, mat, tang_elem, reac_elem, t_incr):
        du_elem = pb._solution.getFieldAtNodes("dU",0,self._rank) 
        for ip in self._integrator:
            grad = self.grad(ip)
            deto = grad.dot( du_elem )
            mat.pull(self._rank, ip, pb._solution)
            tgt = mat.integrate(deto)
            mat.push(self._rank, ip, pb._solution)
            w, xip = self._integrator[ip]
            det_j= np.linalg.det(self._interpolator.jacobian(xip, self._coors[:,:pb._solution._mesh.dimension()]))
            tang_elem[:,:] += w * det_j * grad.T.dot(tgt.dot(grad))
            reac_elem[:,:] -= w * det_j * grad.T.dot(pb._solution.getFieldAtElemInteg("sig", t_incr, self._rank, ip))

    
