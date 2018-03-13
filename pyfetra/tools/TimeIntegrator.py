



class Integrator:
    def __init__(self):
        self._scheme = ""
        self._t0     = 0.
        self._dt     = 0.
        
    def setOptions( opt ):
        raise NotImplementedError

    def setTime(self, t0, dt):
        pass

    def setInit(self, xInit ):
        pass

    def integrate( mat ):
        raise NotImplementedError

    
class ImplicitIntegrator(Integrator):
    def __init__(self):
        Integrator.__init__(self)
        self._scheme = "implicit"

    

class ExplicitIntegrator(Integrator):
    def __init__(self):
        Integrator.__init__(self)
        self._scheme = "explicit"


