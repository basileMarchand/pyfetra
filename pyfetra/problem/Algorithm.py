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
from pyfetra.tools import Factory, Solution, GlobalMatrix, GlobalVector

import logging
module_logger = logging.getLogger("pyfetra")


class Algorithm(object):
    def __init__(self, mesh, bcs, materials, sequence, options):
        self._mesh = mesh
        self._bcs = bcs
        self._materials = materials
        self._time = sequence
        self._opt = options
        self._solution = Solution(mesh, sequence)
        self._pb_type = None
        self._is_initialized = False
        
        self._lhs = GlobalMatrix(self._mesh)
        self._rhs_reaction = GlobalVector(self._mesh)
        self._rhs_external = GlobalVector(self._mesh)

    def initialize(self):
        #-> Step 1 : initialize dirichlet boundary conditions 
        #            i.e. compute active and imposed dofs id 
        self._bcs["dirichlet"].initialize(self._mesh)
        #-> Step 2 : instanciate the choosen linear solver
        self._linear_solver = Factory.Create("LinearSolver", self._opt["linear_solver"])
        #-> Step 3 : instanciate and initialize the Solution object according to : 
        #             a) the element formulation (nodel dofs)
        #             b) the materials used and the associated internal variables needed
        self._solution.initializeDofs(self)

        ##for mat in self._materials:
        self._solution.initialize(self._materials)
        
    def Type(self):
        return self._pb_type

    def solve(self):
        if( not self._is_initialized ):
            self.initialize()

        for i,t in enumerate(self._time):
            self._incr = i+1 
            module_logger.info(" Increment {} - t = {}".format(i+1, t))
            
            self.initDofIncrement()
                
            self.computeInternalReac()
            #self.computeExternalLoad()
            
            ok_convergence = False
            self._bcs["dirichlet"].setToZero( self._rhs_reaction )
            resid0 = self._rhs_reaction.norm()
            ddu = np.zeros((len(self._bcs["dirichlet"]._active_dofs), 1))
            for k in range(self._opt["iterations"]):
                lhs, rhs = self.applyDirichlet2(self._rhs_reaction, t )
                ddu = self._linear_solver.solve(lhs, rhs)
                self.updateIncr( ddu )
                self.computeInternalReac()
                resid = self._rhs_reaction
                self._bcs["dirichlet"].setToZero( resid )
                residual = resid.norm()
                ratio = residual/resid0 
                module_logger.info("    iter {} : {} ({})".format(k+1, ratio, resid0) )
                if(  ratio < self._opt["ratio"] ):
                    module_logger.info("     -> Newton algorithm converge in {} iterations with ratio {}".format(k+1, ratio))
                    ok_convergence = True
                    break
                    
            if not ok_convergence:
                raise Exception("No convergence error in the global newton iterations")
            else:
                self.endIncrement()
                
    def updateIncr(self, ddU):
        """
        Update displacement increment 
        """ 
        #-> update U
        self._solution._data["dprimal"][0]._data[self._bcs["dirichlet"]._active_dofs] += ddU.ravel()
        #-> set to zero K and Fint
        self._lhs.reset()
        self._rhs_reaction.reset()

    def endIncrement(self):
        self._solution._data["primal"][self._incr]._data = self._solution._data["primal"][self._incr-1]._data + self._solution._data["dprimal"][0]._data
        self._solution._data["dprimal"][0].reset()
        self._lhs.reset()
        self._rhs_reaction.reset()
        
    def computeInternalReac(self):
        module_logger.debug("compute internal reaction ...")
        for mat in self._materials:
            mat.attachTime(self._time.getIncr())
            grp = self._mesh.getGroup("elem", mat.getGroup())
            for elem_rk in grp._entities_rk:
                elem = self._mesh.getElement(elem_rk)
                tang_elem = np.zeros((elem.nbDof(), elem.nbDof()))
                reac_elem = np.zeros((elem.nbDof(),1)) 
                elem.internalReactionAndTangent( self, mat , tang_elem, reac_elem, self._time.getIncr())
                self._lhs.addContribution(elem, tang_elem)
                self._rhs_reaction.addContribution(elem, reac_elem)
        module_logger.debug("done")

    def computeExternalLoad(self):

        raise NotImplementedError


    def applyDirichlet2(self, resid,t):
        """
        Apply Dirichlet boundary conditions on the lhs and rhs
        """

        lhs_d = self._bcs["dirichlet"].constrainOperator(self._lhs)

        ac_dofs = self._bcs["dirichlet"]._active_dofs
        fi_dofs = self._bcs["dirichlet"]._fixed_dofs

        rhs_d = resid._data[self._bcs["dirichlet"]._active_dofs] - self._bcs["dirichlet"]._mat_if.dot(self._bcs["dirichlet"].deltaValues(self._time.previous(), self._time.dt()) - self._solution._data["dprimal"][0]._data[fi_dofs].reshape((-1,1)) )
        
        return lhs_d, rhs_d
    
    def initDofIncrement(self):
        self._bcs["dirichlet"].setBoundaryDeltaValues(self._solution._data["dprimal"][0], self._time.previous(), self._time.dt())

