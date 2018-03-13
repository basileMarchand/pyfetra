import numpy as np



def elasticityMatrix( coeffs ):
    ret = None
    if( coeffs["hypothesis"]=="isotrope" ):
        E = coeffs["young"]
        NU = coeffs["poisson"]
        ret = E/((1.+NU)*(1.-2.*NU)) * np.array([[1-NU,NU,NU,0.,0.,0.],
                                              [NU,1-NU,NU,0.,0.,0.],
                                              [NU,NU,1-NU,0.,0.,0.],
                                              [0.,0.,0.,0.5-NU,0.,0.],
                                              [0.,0.,0.,0.,0.5-NU,0.],
                                              [0.,0.,0.,0.,0.,0.5-NU]])

    return ret
