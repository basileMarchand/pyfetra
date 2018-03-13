import numpy as np

from .elasticityMatrix import elasticityMatrix

class Behavior:
    def __init__(self):
        self._name = "Behavior"
        self._require = {}
        self._fields = {}
        self._group = "" 
        self._increment = 0
        self._data = {}
        self._mat_coeffs = {}
        self._elasticity = None
        self.installRequires()

    def getGroup(self):
        return self._group

    def setCoefficients(self, coeffs  ):
        for key in self._coeffs_req:
            if key not in coeffs.keys():
                break
            elif key=="elasticity":
                self._elasticity = elasticityMatrix( coeffs["elasticity"] )
            else:
                self._mat_coeffs[key] = coeffs[key]

    def components(self):
        """
        Virtal method implemented in daughter
        """
        raise NotImplementedError

    def needFields(self):
        return self._require

    def attachTime(self, time_incr):
        self._increment = time_incr


    def pull(self, elem_rk, integ_pt, sol ):
        for f in self._require:
            self._data[f] = np.zeros(sol.getFieldShape(f))
            self._data[f] = sol.getFieldAtElemInteg(f, self._increment, elem_rk, integ_pt)
            self._data[f+"_ini"] = sol.getFieldAtElemInteg(f, self._increment-1, elem_rk, integ_pt)
       
    def push(self, elem_rk, integ_pt, sol ):
        for f in self._require:
            sol.setFieldAtElemInteg(f, self._increment, elem_rk, integ_pt, self._data[f]) 
            
         
    
    def integrate(self, deps ):
        raise NotImplementedError


    def yieldGrad(self ):
        raise NotImplementedError


