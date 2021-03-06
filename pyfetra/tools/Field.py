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
import math 

class Field(object):
    def __init__(self, field_name, mesh):
        self._name = field_name
        self._mesh = mesh
        self._data = None
        self._nb_component = 0
        self.initialize()
        
    def nbComponent(self):
        return self._nb_component

    def initialize(self):
        raise NotImplementedError


def NodeComponent(fname, dim):
    if( fname == "U" ):
        return dim


class NodalField(Field):
    def __init__(self, field_name, mesh):
        self._dof_by_node = None
        Field.__init__(self, field_name, mesh)
        self._nb_component = int(self._mesh.nbDof()/self._mesh.nbNode())
        ###NodeComponent(field_name, mesh.dimension())

    def initialize( self ):
        self._data = np.zeros( self._mesh.nbDof() )

    def getField(self, elem_rk):
        dofs = self._mesh._elements[elem_rk].getDofs()
        return self._data[dofs].reshape((-1,1))

    def getFieldOnElem(self, elem ):
        pass

    def reset(self):
        self._data = np.zeros_like(self._data)



def IntegComponent(kind, dim):
    if kind=="tensor2":
        if (dim==3):
            return 6
        elif dim==2:
            return 3
    elif kind=="vector":
        return dim
    elif kind=="scalar":
        return 1



class IntegField(Field):
    def __init__(self, field_name, kind, mesh):
        self._kind = kind
        Field.__init__(self, field_name, mesh)

    def initialize(self ):
        self._nb_component = IntegComponent(self._kind, self._mesh.dimension())
        self._data = np.zeros( self._mesh.nbIntegPoints()*self._nb_component )
        if self._kind == "tensor2" and self._mesh.dimension()==2:
            def add_sqrt2( tens ):
                return np.array([x for x in tens[:2]] + [ math.sqrt(2.)*x for x in tens[2:]])
            def del_sqrt2( tens ):
                return np.array([x for x in tens[:2]] + [ x/math.sqrt(2.) for x in tens[2:]])
        elif self._kind == "tensor2" and self._mesh.dimension()==3:
            def add_sqrt2( tens ):
                return np.array([x for x in tens[:3]] + [ math.sqrt(2.)*x for x in tens[3:]])
            def del_sqrt2( tens ):
                return np.array([x for x in tens[:3]] + [ x/math.sqrt(2.) for x in tens[3:]])
        else:
            def add_sqrt2( tens ):
                return tens
            def del_sqrt2(tens):
                return tens
            
        self._add_sqrt2 = add_sqrt2
        self._del_sqrt2 = del_sqrt2


    def getField(self, elem_rk, ip):
        global_ip = self._mesh.getGlobalIp(elem_rk) + ip
        return self._add_sqrt2(self._data[global_ip:(global_ip+self._nb_component)].reshape((-1,1)))

    def setField(self, elem_rk, ip, val):
        global_ip = self._mesh.getGlobalIp(elem_rk) + ip
        self._data[global_ip:(global_ip+self._nb_component)] = self._del_sqrt2(val.ravel())


    def getFieldReference(self, elem_rk, ip, out):
        global_ip = self._mesh.getGlobalIp(elem_rk) + ip
        out[:,:] = self._data[global_ip:(global_ip+self._nb_component)].reshape((-1,1))



    
