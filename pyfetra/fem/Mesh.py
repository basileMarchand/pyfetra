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
from .ElemSkeleton import Element
from ..tools import Factory

class FemMesh:
    __nelem = 0
    __nnode = 0

    def __init__(self, msh_name):
        self.msh_name = msh_name
        self._groups = {"elem":{}, "node":{}}
        self._dofsOnNodes = []
        self._nb_dofs = 0
        self._ip_offset = None

    def getElement(self, index):
        return self._elements[index]

    def getNodes(self, index):
        return self._nodes[index]

    def reserveNodes(self, nn ):
        self.__nnode = nn
        self.__nodes = np.zeros((nn,3))
        self._dofsOnNodes = [None]*(nn)

    def addNode(self, rank, coords):
        self.__nodes[rank,:] = coords

    def getCoordinates(self):
        return self.__nodes

    def reserveElements(self, ne ):
        self.__nelem = ne
        self._elements = np.zeros((ne,), dtype=Element)


    def addElement(self, rank, e_type, connectivity):
        elem = Factory.Create("Element", e_type + "MechSmallStrain")
        elem.setRank( rank )
        elem.setConnectivity(connectivity, self.__nodes)
        self._elements[rank] = elem
        for i,n_id in enumerate(elem._connec):
            self._dofsOnNodes[n_id] = np.array([elem._dofs[k] for k in range(i*elem._ndofByNode,(i+1)*elem._ndofByNode)])
        

    def finalize(self):
        self._nb_dofs = 0
        for a in self._dofsOnNodes:
            self._nb_dofs += a.shape[0]

        print("Global number of dofs : {}".format(self._nb_dofs))

    def buildGlobalIp(self):
        self._ip_offset = [0]*(self.__nelem+1)
        for e in self._elements:
            self._ip_offset[e._rank+1] = self._ip_offset[e._rank] + e._ngp
        

    def addGroup(self, grp):
        self._groups["elem"][grp.name()] = grp
        
    def nbNode(self):
        return self.__nnode

    def nbElem(self):
        return self.__nelem

    def nbDof(self):
        return self._nb_dofs

    def nbIntegPoints(self):
        return self._ip_offset[-1]

    def dimension(self):
        return 3

    def nodeGroupFromElemGroup(self, elem_group_name, node_group_name):
        grp = self._groups["elem"][elem_group_name]
        new_grp = NodeGroup(node_group_name)
        new_grp.fromElemGroup(grp, self)
        self._groups["node"][node_group_name] = new_grp

    def renameElemGroup(self, grp_name, new_name):
        self._groups["elem"][new_name] = self._groups["elem"][grp_name]

    def getGroup(self,  grp_type, grp_name):
        return self._groups[grp_type][grp_name]


    def getNodeGroup(self, grp_name):
        return self.getGroup("node", grp_name)

    def getDofsOnNode(self, node_rk):
        return self._dofsOnNodes[node_rk]


    def getGlobalIp(self, elem_rk):
        return self._ip_offset[elem_rk]



class Group:
    def __init__(self, name):
        self._name = name
        self._entities_rk = None
        self._index = 0
        self._size = 0

    def name(self):
        return self._name

    def __iter__(self):
        return self

    def __next__(self):
        if(self._index >= self._size):
            self._index = 0
            raise StopIteration
        else:
            x = self._entities_rk[self._index]
            self._index += 1
            return x

        
class ElemGroup(Group):
    def __init__(self, name):
        Group.__init__(self, name)

    def setElements( self, elements ):
        self._entities_rk = elements
        self._size = len(self._entities_rk)

        

class NodeGroup(Group):
    def __init__(self, name):
        Group.__init__(self, name)

    def setNodes(self, nodes):
        self._entities_rk = nodes
        self._size = len( self._entities_rk )

    def fromElemGroup(self, elem_grp, mesh):
        all_nodes = []
        for e_rk in elem_grp:
            for node in mesh._elements[e_rk]._connec:
                all_nodes.append( node )
        self._entities_rk = list(set(all_nodes))
        self._size = len( self._entities_rk )
