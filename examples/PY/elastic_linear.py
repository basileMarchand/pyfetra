from pyfetra import LOGGER, MESSAGE, INTERACT
from pyfetra.fem import readMesh
from pyfetra.tools import Time
from pyfetra.behavior import LinearElastic
from pyfetra.problem import Dirichlet, ProblemMechanical
from pyfetra.output  import ExportResults

LOGGER(job="elastic_linear", display='INFO', logfile='DEBUG')

# 1-Define finite element mesh

mesh = readMesh("../DATA/beam3d.msh", "GMSH", "mechanical")
mesh.nodeGroupFromElemGroup("3", "dbc1")
mesh.nodeGroupFromElemGroup("4", "dbc2")
mesh.renameElemGroup("5", "ALL")

mesh.finalize()

# 2-Define behavior
mat1 = LinearElastic()
mat1.setGroup("ALL")
mat1.setCoefficients({"elasticity":{"hypothesis": "isotrope",
                                    "young":200000.,
                                    "poisson":0.3}
                      })



materials = (mat1,)

# 3-Define Boundary conditions

ud_x = lambda t: 0.
ud_y = lambda t: 0.
ud_z = lambda t: 0.

load_1 = Dirichlet(group="dbc1", 
                   dofs=[0,1,2], 
                   values=[ud_x,ud_y,ud_z])

ud_z2 = lambda t: t

load_2 = Dirichlet(group="dbc2", 
                   dofs=[0], 
                   values=[ud_z2])

boundary_conditions={"dirichlet" : load_1 + load_2,
                     "neumann"   : []}

# 4-Define time evolution 

sequence = Time(time      = [0.,1.],
                increment = [2])

# 5-Set problem resolution

opt = {"algorithm":"newton",
       "iterations" :2,
       "ratio"    : 0.01,
       "linear_solver": "scipy.sparse", 
       "bc_method":"elimination",
       "init_incr":False}


sol = ProblemMechanical(mesh, 
                        boundary_conditions,
                        materials,
                        sequence,
                        options=opt)

# 6-Solve problem 
sol.solve()

# 7-Export results
out = ExportResults(sol,
                    nodal_fields=["U",],
                    integ_fields=[],
                    time = [1,2],
                    out_format="vtk",
                    fname="test")
out.execute()






