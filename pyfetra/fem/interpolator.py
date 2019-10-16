import numpy as np
from pyfetra.tools import myInv2, myInv3

class SpaceInterpolator(object):
    def __init__(self):
        self._order = None
        
    def shape(self, x ):
        raise NotImplementedError

    def dshape(self, x ):
        raise NotImplementedError

    def inv(self, m ):
        raise NotImplementedError

    def dshape_dx(self, x, coord ):
        dN = self.dshape( x )
        jac = self.inv(self.jacobian( x, coord ))
        return jac.dot( dN )

    def jacobian(self, x, coord ):
        dN = self.dshape( x )
        return dN.dot( coord )



class Tri3Interpolator(SpaceInterpolator):
    def __init__(self):
        super(Tri3Interpolator, self).__init__()
        self._order = 1

    def shape(self, x ):
        a = x[0]
        b = x[1]
        return np.array([1.-a-b, a, b])

    def dshape(self, x ):
        return np.array([[-1., 1., 0.], [-1., 0., 1.]])
        
    def inv(self, m):
        return myInv2(m)


class Tetra4Interpolator(SpaceInterpolator):
    def __init__(self ):
        super(Tetra4Interpolator, self).__init__()
        self._order = 1

    def shape(self, x ):
        return np.array([ x[1], x[2], 1.-x[0]-x[1]-x[2], x[0] ])
        
    def dshape(self, x ):
        return np.array([[0., 0., -1., 1],[1., 0., -1., 0.], [0., 1., -1., 0]])

    def inv(self, m):
        return myInv3(m)

    
