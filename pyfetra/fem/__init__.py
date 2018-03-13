__all__=["readMesh"]


from .SEG2 import Seg2MechSmallStrain
from .TRI3 import Tri3MechSmallStrain
from .TET4 import Tet4MechSmallStrain



from .Mesh import FemMesh, Group, ElemGroup
from .MeshReader import MeshReader, GMSHReader


def readMesh( mesh_path, mesh_format, mesh_hypothesis):
    reader = GMSHReader( mesh_path )
    reader.open()
    reader.read()
    return reader._mesh_object


