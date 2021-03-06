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


from .Field import NodalField, IntegField

class Solution(object):
    def __init__(self, mesh, time):
        self._mesh = mesh
        self._time = time
        self._data = {"main":{}, "grad":{}, "flux":{}, "vint":{}}

    def initializeDofs(self, pb):
        self._data["primal"] = [NodalField("U", self._mesh) for i in self._time._full]
        self._data["dprimal"] = [NodalField("dU", self._mesh),]


        if pb.Type() == "mechanical":
            self._data["U"] = self._data["primal"]
        elif pb.Type() == "thermal":
            self._data["T"] = self._data["primal"]
        else:
            raise ValueError("Not supporter problem type : {}".format(pb.Type()))

    def initialize(self, materials):
        if(self._mesh._ip_offset == None):
            self._mesh.buildGlobalIp( materials )

        for mat in materials:
            for f,kind in mat.needFields():
                if f not in self._data.keys():
                    self._data[f] = [ IntegField(f,kind, self._mesh) for i in self._time._full ]
                else:
                    continue

            self._data["dual"] = self._data[mat.dualVariable()]

    def getFieldAtElemInteg(self, f_name, time_incr, elem, ip ):
        return self._data[f_name][time_incr].getField(elem, ip)

    def setFieldAtElemInteg(self, f_name, time_incr, elem, ip, f_val):
        self._data[f_name][time_incr].setField(elem, ip, f_val)


    def getFieldAtNodes(self, f_name, time_incr, elem):
        return self._data[f_name][time_incr].getField(elem)

    def getFieldShape(self, f_name):
        return (self._data[f_name][0]._nb_component,1)
