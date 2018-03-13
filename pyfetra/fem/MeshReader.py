import numpy as np
from operator import itemgetter

from pyfetra.fem import FemMesh, ElemGroup

import logging
module_logger = logging.getLogger("pyfetra")


class MeshReader:
    def __init__(self, mesh_path):
        self._mesh_path = mesh_path
        self._mesh_object = FemMesh( mesh_path )



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

class GMSHReader(MeshReader):
    def __init__(self, mesh_path):
        MeshReader.__init__(self, mesh_path)
        self._index = 0
        
    def open(self):
        try:
            filePath = open(self._mesh_path, 'rt')
            module_logger.info("mesh file {} succesfully opened".format(self._mesh_path))
        except IOError:
            module_logger.error("mesh file {} doesn't exist".format(self._mesh_path))
            sys.exit()
            
        self._content = filePath.read().split('\n')
        filePath.close()        

    def read(self):
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
        
        group_dic = {}
        # Store element id group by group
        for group_id in tmp:
            grp = ElemGroup(group_id)
            self._mesh_object.addGroup( grp )
            e_rk_list = [ int(x) for x in group_elem_array[group_elem_array[:,0]==group_id][:,1] ]
            ##grp.setElements( group_elem_array[group_elem_array[:,0]==group_id][:,1].tolist() )
            grp.setElements( e_rk_list )
            ##group_dic[str(group_id)] = group_elem_array[group_elem_array[:,0]==group_id][:,1].tolist()
            
 

if __name__ == '__main__':
    mesh_path = "../../TESTS/MESH_FILES/beam3d.msh"
    reader = GMSHReader( mesh_path )
    reader.open()
    reader.read()
    
