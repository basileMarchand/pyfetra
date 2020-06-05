
import numpy as np
import pyfetra
import pyfetra.fem 

nodes = np.array([[1., 0., 0.],
                  [1., 1., 0.],
                  [0., 0., 0.],
                  [0., 1., 0.]])


def test_grad1():
    elem = pyfetra.fem.Triangle3MechSmallStrain()
    elem.setRank( 0 )
    elem.setConnectivity( [0,1,2], nodes)
    elem.grad(0)
    grad = np.array([[1, 0., 0., 0., -1., 0.],
                      [0., -1., 0., 1., 0., 0.],
                      [-1., 1., 1., 0., 0., -1.]])
    
    assert np.all(np.isclose( elem.grad(0), grad ))

def test_grad2():
    elem = pyfetra.fem.Triangle3MechSmallStrain()
    elem.setRank( 0 )
    elem.setConnectivity( [3,2,1], nodes)
    
    grad = np.array([[-1, 0., 0., 0., 1., 0.],
                      [0., 1., 0., -1., 0., 0.],
                      [1., -1., -1., 0., 0., 1.]])
    
    assert np.all(np.isclose( elem.grad(0), grad))
