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

def elasticityMatrix( coeffs ):
    ret = None
    if "plane_strain" in coeffs["hypothesis"]:
        if( "isotrope" in coeffs["hypothesis"] ):
            E = coeffs["young"]
            NU = coeffs["poisson"]
            ret = E/((1.+NU)*(1.-2.*NU)) * np.array([[1-NU,NU  ,0.],
                                                     [NU  ,1-NU,0.],
                                                     [0.  ,0.  ,0.5-NU]])
    else:
        if( "isotrope" in coeffs["hypothesis"] ):
            E = coeffs["young"]
            NU = coeffs["poisson"]
            lame0 = E/(1+NU)
            lame1 = E*NU/((1+NU)*(1-2*NU))
            lame = lame0 + lame1
            ret = np.array([[lame,lame1,lame1,0.,0.,0.],
                            [lame1,lame,lame1,0.,0.,0.],
                            [lame1,lame1,lame,0.,0.,0.],
                            [0.,0.,0.,lame0,0.,0.],
                            [0.,0.,0.,0.,lame0,0.],
                            [0.,0.,0.,0.,0.,lame0]])

    return ret




def conductivityMatrix( coeffs ):
    ret = None
    if "plane" in coeffs["hypothesis"]:
        k = coeffs["kappa"]
        ret = np.diag(np.array([-k,-k]))
    elif "isotrope" in coeffs["hypothesis"]:
        k = coeffs["kappa"]
        ret = np.diag(np.array([-k,-k,-k]))    
    return ret
