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
from operator import itemgetter

from pyfetra.fem import FemMesh, ElemGroup, NodeGroup

import logging
module_logger = logging.getLogger("pyfetra")


class MeshReader:
    def __init__(self, mesh_path):
        self._mesh_path = mesh_path
        self._mesh_object = FemMesh( mesh_path )

    def open(self):
        try:
            filePath = open(self._mesh_path, 'rt')
            module_logger.info("mesh file {} succesfully opened".format(self._mesh_path))
        except IOError:
            module_logger.error("mesh file {} doesn't exist".format(self._mesh_path))
            sys.exit()
            
        self._content = filePath.read().split('\n')
        filePath.close()        


    def setFormulation(self, hypothesis ):
        self._mesh_object.setFormulation( hypothesis )

GMSH2PYTOTE={"1" : "SEG2",    # SEG2
             "2" : "TRI3",    # TRI3
             "3" : "QUA4",    # QUA4
             "4" : "TET4",   # TET4
             "5" : "HEX8",   # HEX8
             "6" : "PRI6",   # PRI6
             "7" : "PYR5",   # PYR5
             "8" : "SEG3",   # SEG3
             "9" : "TRI6",   # TRI6
             "11" :"TET10",  # TET10
             "15" : "VERTEX",    # VERTEX
             "16" : "QUA8"}  # QUA8 

GEOF2PYFETRA={"c2d2" : "SEG2",    # SEG2
             "c2d3" : "TRI3",    # TRI3
             "c2d4" : "QUA4",    # QUA4
             "c3d4" : "TET4",   # TET4
             "c3d8" : "HEX8",   # HEX8
             "c3d6" : "PRI6"}


class GMSHReader(MeshReader):
    def __init__(self, mesh_path):
        MeshReader.__init__(self, mesh_path)
        self._index = 0

    def read(self, hypothesis):
        self.setFormulation( hypothesis )
        module_logger.info(" Read mesh : {}".format(self._mesh_path))
        n_line = len(self._content)
        while(self._index < n_line ):
            line = self._content[self._index]
            self._index += 1
            if( "$Nodes" in line ):
                self.readNodes()
            elif( "$Elements" in line):
                self.readElements()

    def readNodes(self):
        module_logger.info("  - read nodes")
        line = self._content[self._index]
        n_node = int(line)
        self._index += 1
        node_rk = 0
        self._mesh_object.reserveNodes(n_node)
        line = self._content[self._index]
        while( "$EndNodes" not in line ):
            line = line.split()
            node_coord = np.array([float(x) for x in line[1:]])
            self._mesh_object.addNode(node_rk, node_coord)
            self._index += 1
            line = self._content[self._index]
            node_rk +=1

    def readElements(self):
        module_logger.info("  - read elements")
        line = self._content[self._index]
        n_elem = int(line)
        self._mesh_object.reserveElements(n_elem)
        self._index += 1
        group_list = []
        line = self._content[self._index]
        while( "$EndElements" not in line ):
            line = line.split()
            line_list = [int(x) for x in line]
            elem_rk = int(line[0])-1 
            type_elem = GMSH2PYTOTE[line[1]]
            id_group = line[3]
            nodes    = [int(x)-1 for x in line[5:]]
            self._mesh_object.addElement(elem_rk, type_elem,  nodes)
            group_list.append([id_group, elem_rk])
            self._index += 1
            line = self._content[self._index]

        self.buildGroups(group_list)

    def buildGroups(self, group_elem):
        # Sort element list by group
        sorted(group_elem,key=itemgetter(0))
        group_elem_array = np.array(group_elem)    
        
        tmp = list(set(group_elem_array[:,0].tolist()))
        
        # Store element id group by group
        for group_id in tmp:
            grp = ElemGroup(group_id)
            self._mesh_object.addGroup( grp )
            e_rk_list = [ int(x) for x in group_elem_array[group_elem_array[:,0]==group_id][:,1] ]
            grp.setElements( e_rk_list )
        
    
class GeofMeshReader(MeshReader):
    def __init__(self, mesh_path):
        MeshReader.__init__(self, mesh_path)
        self._index = 0
        
    def read(self, hypothesis):
        self.setFormulation( hypothesis )
        module_logger.info(" Read mesh : {}".format(self._mesh_path))
        n_line = len(self._content)
        while(self._index < n_line ):
            line = self._content[self._index]
            self._index += 1
            if( "**node" in line ):
                self.readNodes()
            elif( "**element" in line):
                self.readElements()
            elif "**group" in line:
                self.readGroups()

    def readNodes(self):
        module_logger.info("  - read nodes")
        line = self._content[self._index]
        n_node = int(line.split(" ")[0])
        dim = int(line.split(" ")[1])
        self._index += 1
        node_rk = 0
        self._mesh_object.reserveNodes(n_node)
        line = self._content[self._index]
        while( "**element" not in line ):
            line = line.split()
            node_coord = [float(x) for x in line[1:]]
            coords = np.zeros(3)
            coords[:dim] = node_coord
            self._mesh_object.addNode(node_rk, coords)
            self._index += 1
            line = self._content[self._index]
            node_rk +=1
        self._index -=1

    def readElements(self):
        module_logger.info("  - read elements")
        module_logger.warning("    quadratic element are not supported yet")
        line = self._content[self._index]
        n_elem = int(line)
        self._mesh_object.reserveElements(n_elem)
        self._index += 1
        line = self._content[self._index]
        while( "***group" not in line ):
            line = line.split()
            elem_id = int(line[0])
            type_elem = line[1]
            nodes    = [int(x)-1 for x in line[2:]]
            self._mesh_object.addElement(elem_id-1, GEOF2PYFETRA[type_elem], nodes)
            self._index += 1
            line = self._content[self._index]


    def readGroups(self):
        module_logger.info("  - read groups")
        module_logger.warning("    faset and liset are not supported yet")
        line = self._content[self._index]
        while "***return" not in line:
            if "**elset" in line:
                name = line.split(" ")[1]
                grp = ElemGroup(name)
                elem_rks = []
                self._index += 1
                line = self._content[self._index]
                while "**" not in line:
                    elem_rks += [ int(x)-1 for x in line.split() ]
                    self._index += 1
                    line = self._content[self._index]
                grp.setElements(elem_rks)

            elif "**faset" in line or "**liset" in line:
                #name = line.split(" ")[1]
                #grp = ElemGroup()
                self._index += 1
                line = self._content[self._index]
                continue
            elif "**nset" in line:
                name = line.split(" ")[1]
                grp = NodeGroup(name)
                self._index += 1
                line = self._content[self._index]
                node_rks = []
                while "**" not in line:
                    node_rks += [ int(x)-1 for x in line.split() ]
                    self._index+=1
                    line = self._content[self._index]

                grp.setNodes(node_rks)
            else:
                self._index+=1
                line = self._content[self._index]
                continue

            self._mesh_object.addGroup(grp)
            line = self._content[self._index]


if __name__ == '__main__':
    mesh_path = "../../examples/DATA/beam3d.msh"
    reader = GMSHReader( mesh_path )
    reader.open()
    reader.read()
    
