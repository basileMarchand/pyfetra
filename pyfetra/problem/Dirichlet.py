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


import logging
module_logger = logging.getLogger("yaifem")

import numpy as np


from ..tools import GlobalMatrix, GlobalVector


class Dirichlet:
    def __init__(self, group, dofs, values):
        self._group = [group,]
        self._directions = [dofs, ]
        self._values = [values, ]
        self._method = "elimination"
        self._is_initialized = False
        self._active_dofs = []
        self._fixed_dofs  = []
        self._fixed_values=[]

    def initialize(self, mesh ):
        """
        Method which compute active/locked dofs
        """
        for grp_name, direc, value in zip(self._group[0], self._directions[0], self._values[0]):
            grp = mesh.getNodeGroup(grp_name)
            for node in grp:
                node_dofs = mesh.getDofsOnNode(node)
                self._fixed_dofs += node_dofs[direc].tolist()
                self._fixed_values += value

        # Check that there is not over constrain dofs 
        if( len(self._fixed_dofs) != len(set(self._fixed_dofs))):
            module_logger.error("At least on DOFs is overconstrains")

        tmp = np.arange(0, mesh.nbDof())
        self._active_dofs = list( np.delete(tmp, self._fixed_dofs))
            

    def setToZero(self, vector):
        """
        Method which set to zero global vector components corrisponding to imposed 
        dirichlet conditions
        """
        vector._data[self._fixed_dofs] = 0.
        
    def constrainOperator(self, mat):
        res = None
        if self._method == "elimination":
            res  = self._constrainOperatorByElimination(mat)
        elif self._method == "lagrange":
            res  = self._constrainOperatorByLagrange(mat)
        elif self._method == "penalisation":
            res = self._constrainOperatorByPenalisation(mat)
        else:
            module_logger.error("Method {} for Dirichlet is not Implemented".format(self._method))
        return res

    def constrainVector(self, vector, t, dt):
        res = None
        if self._method == "elimination":
            res  = self._constrainVectorByElimination(vector, t, dt)
        elif self._method == "lagrange":
            res  = self._constrainVectorByLagrange(vector, t)
        elif self._method == "penalisation":
            res = self._constrainVectorByPenalisation(vector, t)
        else:
            module_logger.error("Method {} for Dirichlet is not Implemented".format(self._method))
        return res


    def _constrainOperatorByElimination(self, mat):
        #-> First build the scipy.sparse matrix
        sp_mat = mat.getSparse()
        #-> Small trick with csr, csc to optimize sub-matrix extraction
        
        mat_ii = sp_mat.tocsr()[self._active_dofs,:].tocsc()[:,self._active_dofs]
        self._mat_if = sp_mat.tocsr()[self._active_dofs,:].tocsc()[:,self._fixed_dofs]
        res = GlobalMatrix(mat._mesh)
        res.setFromSpSparse(mat_ii)
        return res

    def _constrainVectorByElimination(self, vector, t, dt):
        impo_values = np.array([ [f(t+dt) - f(t),] for f in self._fixed_values])
        tmp = vector._data[self._active_dofs,:] 
        #- self._mat_if.dot(impo_values)
        res = GlobalVector(vector._mesh)
        res.setFromNumpy( tmp )
        return res

    def rebuildVector(self, vec):
        ret = None
        if self._method == "elimination":
            ret = self._rebuildVectorElimination(vec)
        else:
            module_logger.error("Method {} for Dirichlet is not Implemented".format(self._method))

        return ret


    def _rebuildVectorElimination(self, vec):
        pass


    def __add__(self, other ):
        res = Dirichlet( self._group + other._group,
                         self._directions + other._directions,
                         self._values + other._values)
    
        if self._is_initialized or other._is_initialized:
            module_logger.warning("Be carrefull you add two dirichlet conditions where one of theme is already initialized\n You need two recall the Dirichlet.initialize(mesh) method on the resulting object")
 
        return res


    def setBoundaryValues(self, vector, t):
        impo_values = np.array([ f(t) for f in self._fixed_values])
        vector._data[self._fixed_dofs] = impo_values

    def values(self, t):
        impo_values = np.array([ [f(t),] for f in self._fixed_values])
        return impo_values

    def deltaValues(self, t, dt):
        impo_values = np.array([ [f(t+dt)-f(t),] for f in self._fixed_values])
        return impo_values
        

    def setBoundaryDeltaValues(self, vector, t, dt):
        impo_values = np.array([ f(t+dt)-f(t) for f in self._fixed_values])
        vector._data[self._fixed_dofs] = impo_values


    def reaction(self, mesh, t, dt):
        impo_values = np.array([ [f(t+dt) - f(t),] for f in self._fixed_values])
        tmp = self._mat_if.dot(impo_values)
        res = GlobalVector(mesh)
        res.setFromNumpy( tmp )
        return res        
