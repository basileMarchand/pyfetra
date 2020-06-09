import numpy as np
from pyfetra.tools import GlobalMatrix

def computeGradMatrix(mesh, materials):
    _lhs = GlobalMatrix(mesh)

    for mat in materials:
        grp = mesh.getGroup("elem", mat.getGroup())
        for elem_rk in grp._entities_rk:
            elem = mesh.getElement(elem_rk)
            tang_elem = np.zeros((elem.nbDof(), elem.nbDof()))
            elem.computeBtCB(tang_elem,mat, mesh.dimension())
            _lhs.addContribution(elem, tang_elem)
    return _lhs


def computeL2Matrix(mesh, groups):
    _lhs = GlobalMatrix(mesh)

    for g in groups:
        grp = mesh.getGroup("elem", g)
        for elem_rk in grp._entities_rk:
            elem = mesh.getElement(elem_rk)
            tang_elem = np.zeros((elem.nbDof(), elem.nbDof()))
            elem.computeNtN(tang_elem, mesh.dimension())
            _lhs.addContribution(elem, tang_elem)
    return _lhs

