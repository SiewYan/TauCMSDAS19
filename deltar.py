'''
Copied from 
https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/HeppyCore/python/utils/deltar.py
to make this package independent from CMSSW
'''

import numpy as np

def deltaR2( e1, p1, e2=None, p2=None):
    """Take either 4 arguments (eta,phi, eta,phi) or two objects that have 'eta', 'phi' methods)"""
    if (e2 == None and p2 == None):
        return deltaR2(e1.eta(),e1.phi(), p1.eta(), p1.phi())
    de = e1 - e2
    dp = deltaPhi(p1, p2)
    return de*de + dp*dp


def deltaR( *args ):
    return np.sqrt( deltaR2(*args) )


def deltaPhi( p1, p2):
    '''Computes delta phi, handling periodic limit conditions.'''
    res = p1 - p2
    while res > np.pi:
        res -= 2*np.pi
    while res < -np.pi:
        res += 2*np.pi
    return res
