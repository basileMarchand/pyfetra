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
module_logger = logging.getLogger("pyfetra")


from pyfetra.tools import Factory 

class NonLinearSolver(object):
    def __init__(self):
        self._boss = None
        self._niter_max = None
        self._ratio = None
        self._linsolve = None
    
    def initialize(self, boss, opt):
        self._boss = boss
        self._niter_max = opt['iterations']
        self._ratio = opt["ratio"]


class NewtonSolver(NonLinearSolver):
    def __init__(self):
        super(NewtonSolver, self).__init__()

    def solve(self, incr, time ):
        self._boss.computeSystem()
        #self.computeExternalLoad()
        
        ok_convergence = False
        self._boss._bcs["dirichlet"].setToZero( self._boss._rhs_reaction )
        resid0 = self._boss._rhs_reaction.norm()
        ##### ddu = np.zeros((len(self._bcs["dirichlet"]._active_dofs), 1))
        for k in range(self._niter_max):
            ###lhs, rhs = self.applyDirichlet2(self._rhs_reaction, t )
            lhs, rhs = self._boss._bcs["dirichlet"].constrainSystem(self._boss._lhs, self._boss._rhs_reaction)
            ddu = self._boss._linear_solver.solve(lhs, rhs)
            self._boss.updateSolution( ddu )
            self._boss._lhs.reset()
            self._boss._rhs_reaction.reset()
            self._boss.computeSystem()
            resid = self._boss._rhs_reaction
            self._boss._bcs["dirichlet"].setToZero( resid )
            residual = resid.norm()
            ratio = residual/resid0 
            module_logger.info("    iter {} : {} ({})".format(k+1, ratio, resid0) )
            if(  ratio < self._ratio ):
                module_logger.info("     -> Newton algorithm converge in {} iterations with ratio {}".format(k+1, ratio))
                ok_convergence = True
                break
                
        if not ok_convergence:
            raise Exception("No convergence error in the global newton iterations")




Factory.Register("NonLinearSolver", NewtonSolver, "newton")
