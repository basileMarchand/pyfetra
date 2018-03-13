import numpy as np


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
        self._nb_component = NodeComponent(field_name, mesh.dimension())

    def initialize( self ):
        self._data = np.zeros( self._mesh.nbDof() )

    def getField(self, elem_rk):
        dofs = self._mesh._elements[elem_rk].getDofs()
        return self._data[dofs].reshape((-1,1))

    def getFieldOnElem(self, elem ):
        pass

    def reset(self):
        self._data = np.zeros_like(self._data)



def IntegComponent(fname, dim):
    if( fname in ["eto", "sig"] ):
        if (dim==3):
            return 6



class IntegField(Field):
    def __init__(self, field_name, mesh):
        Field.__init__(self, field_name, mesh)


    def initialize(self ):
        self._nb_component = IntegComponent(self._name, self._mesh.dimension())
        self._data = np.zeros( self._mesh.nbIntegPoints()*self._nb_component )

    def getField(self, elem_rk, ip):
        global_ip = self._mesh.getGlobalIp(elem_rk) + ip
        return self._data[global_ip:(global_ip+self._nb_component)].reshape((-1,1))

    def setField(self, elem_rk, ip, val):
        global_ip = self._mesh.getGlobalIp(elem_rk) + ip
        self._data[global_ip:(global_ip+self._nb_component)] = val.ravel()


    def getFieldReference(self, elem_rk, ip, out):
        global_ip = self._mesh.getGlobalIp(elem_rk) + ip
        out[:,:] = self._data[global_ip:(global_ip+self._nb_component)].reshape((-1,1))



    
