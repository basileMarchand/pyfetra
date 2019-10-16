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

from pyfetra.problem import Algorithm
from pyfetra.tools import Factory, Solution, GlobalMatrix, GlobalVector

import logging
module_logger = logging.getLogger("pyfetra")


class ProblemMechanical(Algorithm):
    def __init__(self, mesh, boundaries, materials, sequence, options):
        super(ProblemMechanical, self).__init__(mesh, boundaries, materials, sequence, options)
        self._pb_type = "mechanical"

        
