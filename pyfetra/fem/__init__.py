__all__=["readMesh"]


from .integrator import Tetra4PtInteg, Tri1PtInteg, Seg2PtInteg

__internal_integrator = {"TETRA4PT": Tetra4PtInteg(),
                         "TRI1PT": Tri1PtInteg(),
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


from .Mesh import FemMesh, Group, ElemGroup
from .MeshReader import MeshReader, GMSHReader

def readMesh( mesh_path, mesh_format, mesh_hypothesis):
    reader = GMSHReader( mesh_path )
    reader.open()
    reader.read( mesh_hypothesis )
    return reader._mesh_object


