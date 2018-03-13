

import os
import logging
import numpy as np

# Corrispondence dictionnary between GMSH and PARAVIEW elements
elem_paraview = {1 : 3,    # SEG2
                      2 : 5,    # TRI3
                      3 : 9,    # QUA4
                      "TET4" : 10,   # TET4
                      5 : 12,   # HEX8
                      6 : 13,   # PRI6
                      7 : 14,   # PYR5
                      15: 1,    # VERTEX
                      8 : 21,   # SEG3
                      9 : 22,   # TRI6
                      11 : 24,  # TET10
                      16 : 23}  # QUA8 

# Paraview offset for each elements type
offset_paraview = {3 : 2, 
                   5 : 3, 
                   9 : 4, 
                   "TET4" : 4, 
                   12 : 8, 
                   13 : 6, 
                   14 : 5,
                   21 : 3,
                   22 : 6,
                   24 : 10,
                   23 : 8}

class ExportResults(object):
    def __init__(self, sol, nodal_fields, integ_fields, time, out_format, fname):
        self._sol = sol
        self._nodal_fields = nodal_fields
        self._integ_fields = integ_fields
        self._time = time
        self._out_format = out_format
        self.__fname = fname

    def execute(self):
        # Create directory to store result
        if not os.path.exists(self.__fname):
            os.makedirs(self.__fname)

        # Write data
        self.__write_collection()        

    def __write_collection(self):
        # Create pvd file 
        self.__write_pvd(self._time)
        # For each time step write vtu file
        for (i,t) in enumerate(self._time):
            self.__write_vtu(i)

    def __write_pvd(self,list_iter):
        ext = '.pvd'
        head = '<?xml version ="1.0"?>\n<VTKFile type="Collection" version="0.1" byte_order="LittleEndian">\n'
        bCol = '<Collection>\n'
        eCol = '</Collection>\n </VTKFile>'
        # Delete files if exists
        if os.path.exists(self.__fname + os.path.sep + self.__fname+ext):
            os.remove(self.__fname+ os.path.sep +self.__fname+ext)
        fid = open(self.__fname+ os.path.sep +self.__fname+ext,"a")
        fid.write(head)
        fid.write(bCol)
        for (step,t) in enumerate(list_iter):
            vtu_id = self.__fname+'_step_{}.vtu'.format(step)
            line = '  <DataSet timestep="{}" group="" part="0" file="{}"/>\n'.format(t,vtu_id)
            fid.write(line)
        fid.write(eCol)
        fid.close()

    def __write_vtu(self,step):
        ext = '.vtu'
        head = '<?xml version="1.0"?>\n<VTKFile type="UnstructuredGrid" version="0.1" byte_order="LittleEndian">\n'
        vtu_name = self.__fname +'/'+ self.__fname + '_step_{}.vtu'.format(step)
        if os.path.exists(vtu_name):
            os.remove(vtu_name)
        fid = open(vtu_name,"a")
        fid.write(head)
        # 1 - write mesh data
        self.__write_mesh(fid)
        # 2 - write nodal fields
        self.__write_nodal_fields(fid,step)
        # 3 - write element field
        self.__write_elem_fields(fid,step)
        # 4 - close file        
        fid.write('</Piece>\n')
        fid.write('</UnstructuredGrid>\n')
        fid.write('</VTKFile>\n')
        fid.close()



    def _extractPhysicalElements(self):
        phy_ele_rk = []
        for mat in self._sol._materials:
            grp = self._sol._mesh.getGroup("elem", mat.getGroup())
            phy_ele_rk += grp._entities_rk
        return phy_ele_rk


    def __write_mesh(self,fid):

        elements_rk = self._extractPhysicalElements()
        NN = self._sol._mesh.nbNode()
        NE = len(elements_rk)


        # Elements number to write
        fid.write('<UnstructuredGrid>\n')
        fid.write('<Piece NumberOfPoints="{}" NumberOfCells="{}">\n'.format(NN,NE))
        fid.write('<Points>\n')
        fid.write('<DataArray type="Float64" Name="Array" NumberOfComponents="3" format="ascii">\n')
        lstCoor = self._sol._mesh.getCoordinates()
        line = ""
        for node in lstCoor:
            line +="%f %f %f\n" %(node[0],node[1],node[2])
        fid.write(line)
        fid.write('</DataArray>\n')
        fid.write('</Points>\n')

        fid.write('<Cells>\n')
        fid.write('<DataArray type="Int32" Name="connectivity" format="ascii">\n')
        line = ""
        for ele_rk in elements_rk:
            elem = self._sol._mesh.getElement( ele_rk )
            for node in elem._connec:
                line += "%d " %( node )
            line += "\n"

        fid.write(line)
        fid.write('</DataArray>\n')
        
        fid.write('<DataArray type="Int32" Name="offsets" format="ascii">\n')
        offset = 0
        for ele_rk in elements_rk:
            elem = self._sol._mesh.getElement( ele_rk )
            offset = offset + offset_paraview[elem.type()]
            val = "%d\n" %(offset)
            fid.write(val)
        fid.write('</DataArray>\n')
        fid.write('<DataArray type="Int32" Name="types" format="ascii">\n')
        for ele_rk in elements_rk:
            elem = self._sol._mesh.getElement( ele_rk )
            val = "%d\n" %(elem_paraview[elem.type()])
            fid.write(val)
        fid.write('</DataArray>\n')
        fid.write('</Cells>\n')

    def __write_nodal_fields(self,fid,step):
        n_nodal_field = 0.
        self.__open_nodal_section(fid)
        for field_id in self._nodal_fields:
            self.__write_node_data(fid,step,field_id)
            n_nodal_field += 1

        self.__close_nodal_section(fid)

    def __open_nodal_section(self,fid):
        fid.write('<PointData>\n')

    def __close_nodal_section(self,fid):
        fid.write('</PointData>\n')
        
    def __write_node_data(self,fid,step,field_id):        
        nb_comp = self._sol._solution._data[field_id][self._time[step]].nbComponent()
        fid.write('<DataArray type="Float64" Name="{}" NumberOfComponents="{}" format="ascii">\n'.format(field_id,nb_comp))
        data = self._sol._solution._data[field_id][self._time[step]]._data
        for val in data:
            v = " %f" %(val)
            v = v + "\n"
            fid.write(v)
        fid.write('</DataArray>\n')


    def __write_elem_fields(self,fid,step):
        n_elem_field = 0
        self.__open_elem_section(fid)
        for field in self._integ_fields:                
                self.__write_elem_data(fid,step,field)
                n_elem_field += 1
        if n_elem_field != 0:
            self.__close_elem_section(fid)

    def __open_elem_section(self,fid):
        fid.write('<CellData>')

    def __close_elem_section(self,fid):
        fid.write('</CellData>\n')

    def __write_elem_data(self, fid, step, field_id):
        elements_rk = self._extractPhysicalElements()
        nb_comp = self._sol._solution._data[field_id][self._time[step]].nbComponent()
        fid.write('<DataArray type="Float64" Name="{}" NumberOfComponents="{}" format="ascii">\n'.format(field_id,nb_comp))
        for erk in elements_rk:
            elem = self._sol._mesh.getElement( erk )
            mean_val = np.zeros((nb_comp,1))
            for i in range(elem.nbIntegPts()):
                mean_val += self._sol._solution._data[field_id][self._time[step]].getField(erk, i)
            mean_val /= elem.nbIntegPts()
            v = ""
            for x in mean_val.ravel():
                v += "%f " %(x)
            v+= "\n"
            fid.write(v)
        fid.write("</DataArray>\n")
            
            
