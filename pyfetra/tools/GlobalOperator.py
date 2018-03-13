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
import scipy.sparse as sp


class GlobalMatrix:
    def __init__(self, mesh):
        self._mesh = mesh
        self._irn = []
        self._jcn = []
        self._data = []
        self._rows = self._cols = mesh.nbDof()
        self._is_build = False

    def reset(self):
        self._irn = []
        self._jcn = []
        self._data = []


    def addContribution(self, elem, elem_matrix):
        e_data = elem_matrix.ravel()
        dofs = elem.getDofs()
        nb_dofs = elem.nbDof()
        e_irn  = np.repeat(dofs, nb_dofs)
        e_jcn  = np.tile(dofs, nb_dofs)
        self._data += e_data.tolist()
        self._irn  += e_irn.tolist()
        self._jcn  += e_jcn.tolist()
        
    def getSparse(self):
        ret = sp.coo_matrix((self._data,(self._irn, self._jcn)), (self._rows, self._cols))
        return ret

    def setFromSpSparse(self, spmatrix):
        tmp = spmatrix.tocoo()
        self._data = tmp.data
        self._irn  = tmp.row
        self._jcn  = tmp.col
        self._rows = spmatrix.shape[0]
        self._cols = spmatrix.shape[1]
        
class GlobalVector:
    def __init__(self, mesh):
        self._mesh = mesh
        self._data = np.zeros((mesh.nbDof(),1))
        self._rows = mesh.nbDof()
        self._cols = 1

    def reset(self):
        self._data = np.zeros_like(self._data)


    def addContribution(self, elem, elem_rhs):
        self._data[elem.getDofs(),:] += elem_rhs

    def setFromNumpy(self, npvec):
        self._data = npvec
        self._rows = npvec.shape[0]
        self._cols = npvec.shape[1]

    def __getitem__(self, index):
        raise NotImplementedError

    def __setitem__(self, index, value):
        raise NotImplementedError

    def __add__(self, other):
        ret = GlobalVector(self._mesh)
        ret.setFromNumpy( self._data + other._data )
        return ret

    def __sub__(self, other):
        ret = GlobalVector(self._mesh)
        ret.setFromNumpy( self._data - other._data )
        return ret


    def norm(self):
        return np.linalg.norm(self._data)
