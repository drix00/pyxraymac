#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2007 Hendrix Demers"
__license__ = ""

# Standard library modules.
import math

# Third party modules.

# Local modules.

# Globals and constants variables.

def getRKJonsson1928(lambdaLI, lambdaK):
    """
    Value of $r_{K}$ from Jonsson (1928).

    Reference: E. J\"{o}nsson, Thesis, Upsala (1928).

    \f[
        r_{K} = \frac{\lambda_{L_{I}}}{\lambda_{L_{K}}}
    \f]

    Mandatory arguments:


    Optional arguments:


    Extra arguments:


    Return parameters:

    """
    rK = lambdaLI*lambdaK

    return rK

def getRKRindfleisch1937(atomicNumber):
    """
    Value of $r_{K}$ from Rindfleisch (1937).

    Reference: H. Rindfleisch, Ann. Phys. 28, 409 (1937)

    \f[
        r_{K} = a \cdot Z^{b}
    \f]
    where $\log_{10} a = 1.805283$ and $b = -0.6207$

    Mandatory arguments:


    Optional arguments:


    Extra arguments:


    Return parameters:

    """
    log10A = 1.805283

    b = -0.6207

    a = math.pow(10.0, log10A)

    rK = a*math.pow(atomicNumber, b)

    return rK

def getRKLaubert1941(lambdaK):
    """
    Value of $r_{K}$ from Laubert (1941).

    Reference: S. Laubert, Ann. Phys. 40, 553 (1941)

    \f[
        r_{K} = a \cdot \lambda_{L_{K}}^{b}
    \f]
    where $\log_{10} a = 0.857652$ and $b = 0.0843$

    Mandatory arguments:


    Optional arguments:


    Extra arguments:


    Return parameters:

    """
    log10A = 0.857652

    b = 0.0843

    a = math.pow(10.0, log10A)

    rK = a*math.pow(lambdaK, b)

    return rK

def getRKTellezPlasencia1949(atomicNumber):
    """
    Value of $r_{K}$ from Tellez-Plasencia (1949).

    Reference: H. Tellez-Plasencia, J. Phys. Radium. 10, 14 (1949)

    \f[
        r_{K} = \frac{1}{a + b Z}
    \f]
    where $a = 0.051167$ and $b = 0.0024882$

    Mandatory arguments:


    Optional arguments:


    Extra arguments:


    Return parameters:

    """
    a = 0.051167

    b = 0.0024882


    rK = 1.0/(a + b*atomicNumber)

    return rK

if __name__ == '__main__': #pragma: no cover
    import pyHendrixDemersTools.Runner as Runner
    Runner.Runner().run(runFunction=None)
