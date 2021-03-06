

class IntegRule(object):
    def __init__(self):
        self._ngp = None
        self._gx = None
        self._gw = None

    def __len__(self):
        return self._ngp

    def __iter__(self):
        return iter(range(self._ngp))

    def __getitem__(self, idx ):
        return ( self._gw[idx], self._gx[idx] )


class Seg1PtInteg(IntegRule):
    def __init__(self):
        super(Seg2PtInteg, self).__init__()
        self._ngp = 1
        self._gx = ((0.,),)
        self._gw = (2.,)

class Seg2PtInteg(IntegRule):
    def __init__(self):
        super(Seg2PtInteg, self).__init__()
        self._ngp = 2
        self._gx = ((-0.577350269189626,), (0.577350269189626))
        self._gw = (1., 1.)

        
class Tri1PtInteg(IntegRule):
    def __init__(self):
        super(Tri1PtInteg, self).__init__()
        self._ngp = 1
        self._gx = ((1./3.,1./3.),)
        self._gw = (0.5,)

class Tri3PtInteg(IntegRule):
    def __init__(self):
        super(Tri3PtInteg, self).__init__()
        self._ngp = 3
        a = 1/6.
        b = 2/3.
        self._gx = ((a,a),(b,a),(a,b))
        self._gw = (a,a,a)

class Tetra1PtInteg(IntegRule):
    def __init__(self):
        super(Tetra1PtInteg, self).__init__()
        self._ngp = 1
        a  = 1/4.
        p = 1/6.
        self._gx = ((a,a,a),)
        self._gw = (p,)


class Tetra4PtInteg(IntegRule):
    def __init__(self):
        super(Tetra4PtInteg, self).__init__()
        self._ngp = 4
        a  = (5.-5.**0.5)/(20.)
        b  = (5.+3*5.**0.5)/(20.)
        p  = 1./24.
        self._gx = ((a,a,a),(a,a,b),(a,b,a),(b,a,a))
        self._gw = (p, p, p, p)
