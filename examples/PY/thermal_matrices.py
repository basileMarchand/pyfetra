from pyfetra import LOGGER, MESSAGE, INTERACT
from pyfetra.fem import readMesh
from pyfetra.fem import computeGradMatrix, computeL2Matrix
from pyfetra.behavior import Thermal

from pyfetra.problem import Dirichlet, ProblemThermal

LOGGER(job="thermal", display='INFO', logfile='DEBUG')

# 1-Define finite element mesh

mesh = readMesh("calcul.geof", "GEOF", "Thermal")

mesh.setDimension(2)
mesh.finalize()

# 2-Define behavior
mat1 = Thermal()
mat1.setGroup("Couche_1")
mat1.setCoefficients({"conductivity":{"hypothesis": ["isotrope", "plane"],
                                      "kappa":1.}
                      })

mat2 = Thermal()
mat2.setGroup("Couche_2")
mat2.setCoefficients({"conductivity":{"hypothesis": ["isotrope", "plane"],
                                      "kappa":2.}
                      })


materials = (mat1,mat2)

K = computeGradMatrix(mesh, materials)
M = computeL2Matrix(mesh, ('Couche_1','Couche_2' ))







