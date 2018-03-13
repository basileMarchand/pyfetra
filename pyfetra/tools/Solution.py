
from .Field import NodalField, IntegField

class Solution(object):
    def __init__(self, mesh, time):
        self._mesh = mesh
        self._time = time
        self._data = {"main":{}, "grad":{}, "flux":{}, "vint":{}}

    def initializeDofs(self, pb):
        if pb.Type() == "mechanical":
            self._data["U"] = [NodalField("U", self._mesh) for i in self._time._full]
            self._data["dU"] = [NodalField("dU", self._mesh),]
        else:
            raise ValueError("Not supporter problem type : {}".format(pb.Type()))

    def initialize(self, mat):
        if(self._mesh._ip_offset == None):
            self._mesh.buildGlobalIp()

        for f in mat.needFields():
            if f not in self._data.keys():
                self._data[f] = [ IntegField(f, self._mesh) for i in self._time._full ]
            else:
                continue

    def getFieldAtElemInteg(self, f_name, time_incr, elem, ip ):
        return self._data[f_name][time_incr].getField(elem, ip)

    def setFieldAtElemInteg(self, f_name, time_incr, elem, ip, f_val):
        self._data[f_name][time_incr].setField(elem, ip, f_val)


    def getFieldAtNodes(self, f_name, time_incr, elem):
        return self._data[f_name][time_incr].getField(elem)

    def getFieldShape(self, f_name):
        return (self._data[f_name][0]._nb_component,1)
