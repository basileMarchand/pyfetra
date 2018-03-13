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
        



### Register the Scipy sparse solver in the object factory
Factory.Register("LinearSolver", ScipySparseLinSolve, "scipy.sparse")
