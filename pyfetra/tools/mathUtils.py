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
from numba import jit, float64

@jit
def myDet3(m):
    m_det = m[0][0]*(m[1,1]*m[2,2]-m[1,2]*m[2,1])+m[0][1]*(m[1,2]*m[2,0]-m[1,0]*m[2,2])+m[0][2]*(m[1,0]*m[2,1]-m[1,1]*m[2,0])
    return m_det

@jit
def myDet2(m):
    return m[0][0]*m[1,1]-m[1,0]*m[0,1]

@jit
def myInv3(m):
    m_det = myDet3(m)
    m_inv = (1./m_det) * np.array([[m[1,1]*m[2,2]-m[1,2]*m[2,1] , m[0,2]*m[2,1]-m[0,1]*m[2,2] , m[0,1]*m[1,2]-m[0,2]*m[1,1] ],
                                   [m[1,2]*m[2,0]-m[1,0]*m[2,2] , m[0,0]*m[2,2]-m[0,2]*m[2,0] , m[0,2]*m[1,0]-m[0,0]*m[1,2] ],
                                   [m[1,0]*m[2,1]-m[1,1]*m[2,0] , m[0,1]*m[2,0]-m[0,0]*m[2,1] , m[0,0]*m[1,1]-m[0,1]*m[1,0] ]])
    return m_inv

@jit
def myInv2(m):
    m_det = myDet2(m)
    m_inv = (1./m_det) * np.array([[ m[1,1],-m[0,1]],[-m[1,0],m[0,0] ]])
    return m_inv
