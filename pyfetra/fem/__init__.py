__all__=["readMesh"]


from .integrator import Tetra4PtInteg, Tetra1PtInteg, Tri1PtInteg, Tri3PtInteg, Seg2PtInteg

__internal_integrator = {"TETRA4PT": Tetra4PtInteg(),
                         "TETRA1PT": Tetra1PtInteg(),
                         "TRI1PT": Tri1PtInteg(),
                         "TRI3PT": Tri3PtInteg(),
                         "SEG2PT": Seg2PtInteg()}


from .interpolator import SpaceInterpolator, Tri3Interpolator, Tetra4Interpolator

__internal_interpolator = {"TRI3NODES": Tri3Interpolator(),
                           "TETRA4NODES": Tetra4Interpolator()}


def GetIntegrator( name ):
    return __internal_integrator[name]

def GetInterpolator( name ):
    return __internal_interpolator[name]


from .element import Element
from .segment import Seg2Nodes, Seg2MechSmallStrain
from .triangle import Triangle3Nodes, Triangle3Thermal, Triangle3MechSmallStrain
from .tetra import Tetra4Nodes, Tetra4Thermal, Tetra4MechSmallStrain


from .mesh import FemMesh, Group, ElemGroup, NodeGroup
from .meshReader import MeshReader, GMSHReader, GeofMeshReader

def readMesh( mesh_path, mesh_format, mesh_hypothesis):
    if mesh_format == "GMSH":
        reader = GMSHReader( mesh_path )
    elif mesh_format == "GEOF":
        reader = GeofMeshReader(mesh_path)
    reader.open()
    reader.read( mesh_hypothesis )
    return reader._mesh_object

from .utilities import computeGradMatrix, computeL2Matrix
