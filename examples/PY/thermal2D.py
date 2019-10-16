from pyfetra import LOGGER, MESSAGE, INTERACT
from pyfetra.fem import readMesh
from pyfetra.tools import Time
from pyfetra.behavior import Thermal
from pyfetra.problem import Dirichlet, ProblemThermal
from pyfetra.output  import ExportResults

LOGGER(job="thermal", display='INFO', logfile='DEBUG')

# 1-Define finite element mesh

mesh = readMesh("../DATA/rectangle_fine.msh", "GMSH", "Thermal")
mesh.setDimension(2)
mesh.nodeGroupFromElemGroup("1", "dbc1")
mesh.nodeGroupFromElemGroup("2", "dbc2")
mesh.renameElemGroup("0", "ALL")
mesh.finalize()

# 2-Define behavior
mat1 = Thermal()
mat1.setGroup("ALL")
mat1.setCoefficients({"conductivity":{"hypothesis": ["isotrope", "plane"],
                                      "kappa":20.}
                      })


materials = (mat1,)

# 3-Define Boundary conditions

ud_z0 = lambda t: 0.

load_1 = Dirichlet(group="dbc1", 
                   dofs=[0], 
                   values=[ud_z0])

ud_z1 = lambda t: 1200*t

load_2 = Dirichlet(group="dbc2", 
                   dofs=[0], 
                   values=[ud_z1])

boundary_conditions={"dirichlet" : load_1 + load_2,
                     "neumann"   : []}

# 4-Define time evolution 

sequence = Time(time      = [0.,1.],
                increment = [10])

# 5-Set problem resolution

opt = {"algorithm":"newton",
       "iterations" :2,
       "ratio"    : 0.01,
       "linear_solver": "scipy.sparse", 
       "bc_method":"elimination",
       "init_incr":False}


sol = ProblemThermal(mesh, 
                     boundary_conditions,
                     materials,
                     sequence,
                     options=opt)

# 6-Solve problem 
sol.solve()

# 7-Export results
out = ExportResults(sol,
                    nodal_fields=["T",],
                    integ_fields=["gradT"],
                    time = [1,2,3,4,5,6,7,8,9],
                    out_format="vtk",
                    fname="test")
out.execute()






