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


import scipy.sparse as sp
import scipy.sparse.linalg as spl
from .Factory import Factory



class LinearSolver(object):
    def __init__(self):
        self._solver_type = "fake"
        
    def solve(self, lhs, rhs):
        raise NotImplementedError



class ScipySparseLinSolve(LinearSolver):
    def __init__(self):
        LinearSolver.__init__(self)
        self._solver_type = "scipy.sparse"
        
    def solve(self, lhs, rhs):
        lhs_sp = lhs.getSparse().tocsc()
        res = spl.spsolve(lhs_sp, rhs)
        return res.reshape((-1,1))


class ScipySparseCG(LinearSolver):
    def __init__(self):
        super(ScipySparseCG, self).__init__()
        self._solver_type = "scipy.sparse.cg"
        
    def solve(self, lhs, rhs):
        lhs_sp = lhs.getSparse().tocsc()
        res, info = spl.cg(lhs_sp, rhs)
        return res.reshape((-1,1))
        



### Register the Scipy sparse solver in the object factory
Factory.Register("LinearSolver", ScipySparseLinSolve, "scipy.sparse")
Factory.Register("LinearSolver", ScipySparseCG, "scipy.sparse.cg")
