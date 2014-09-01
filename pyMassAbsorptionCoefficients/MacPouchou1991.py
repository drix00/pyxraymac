#!/usr/bin/env python
"""
Mass absorption coefficients tables from Pouchou and Pichoir (1991).
"""

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2007 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2293 $"
__svnDate__ = "$Date: 2011-03-21 14:39:25 -0400 (Mon, 21 Mar 2011) $"
__svnId__ = "$Id: MacPouchou1991.py 2293 2011-03-21 18:39:25Z hdemers $"

# Standard library modules.

# Third party modules.

# Local modules.
import MassAbsorptionCoefficientEmitter

# Globals and constants variables.
LINE_Ka = 'Ka'
LINE_Lb = 'Lb'
LINE_La = 'La'
LINE_Mb = 'Mb'

class MacPouchou1991(MassAbsorptionCoefficientEmitter.MassAbsorptionCoefficientEmitter):
    def __init__(self):
        self.mac_cm2_g = {}

        self.mac_cm2_g[LINE_Ka] = {}

        atomicNumberEmitter = 5
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter] = {}

        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][5] = 3500.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][6] = 6750.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][7] = 11000.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][8] = 16500.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][13] = 64000.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][14] = 80000.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][22] = 15000.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][23] = 18000.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][24] = 20700.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][26] = 27800.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][27] = 32000.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][28] = 37000.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][40] = 4400.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][41] = 4500.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][42] = 4600.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][57] = 2500.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][73] = 23000.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][74] = 21000.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][92] = 7400.0

        atomicNumberEmitter = 6
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter] = {}

        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][5] = 39000.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][6] = 2170.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][14] = 35000.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][22] = 8100.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][23] = 8850.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][24] = 10700.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][26] = 13500.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][40] = 25000.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][41] = 24000.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][42] = 20500.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][72] = 18000.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][73] = 17000.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][74] = 18000.0

        atomicNumberEmitter = 7
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter] = {}

        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][5] = 15800.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][7] = 1640.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][13] = 13800.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][14] = 17000.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][22] = 4270.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][23] = 4950.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][24] = 5650.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][26] = 7190.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][40] = 24000.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][41] = 25000.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][42] = 25800.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][72] = 14000.0
        self.mac_cm2_g[LINE_Ka][atomicNumberEmitter][73] = 15500.0

        self.mac_cm2_g[LINE_Ka][14] = {}
        self.mac_cm2_g[LINE_Ka][14][73] = 1490.0

        self.mac_cm2_g[LINE_Ka][16] = {}
        self.mac_cm2_g[LINE_Ka][16][79] = 2200.0

        self.mac_cm2_g[LINE_Lb] = {}

        self.mac_cm2_g[LINE_Lb][29] = {}
        self.mac_cm2_g[LINE_Lb][29][29] = 6750.0

        self.mac_cm2_g[LINE_La] = {}
        self.mac_cm2_g[LINE_La][33] = {}
        self.mac_cm2_g[LINE_La][33][31] = 7000.0

        self.mac_cm2_g[LINE_La][42] = {}
        self.mac_cm2_g[LINE_La][42][79] = 2200.0

        self.mac_cm2_g[LINE_Mb] = {}

        self.mac_cm2_g[LINE_Mb][64] = {}
        self.mac_cm2_g[LINE_Mb][64][64] = 4700.0

        self.mac_cm2_g[LINE_Mb][72] = {}
        self.mac_cm2_g[LINE_Mb][72][72] = 3000.0

        self.mac_cm2_g[LINE_Mb][73] = {}
        self.mac_cm2_g[LINE_Mb][73][73] = 2500.0

        self.mac_cm2_g[LINE_Mb][74] = {}
        self.mac_cm2_g[LINE_Mb][74][74] = 2080.0

        self.mac_cm2_g[LINE_Mb][79] = {}
        self.mac_cm2_g[LINE_Mb][79][78] = 2550.0

        self.mac_cm2_g[LINE_Mb][80] = {}
        self.mac_cm2_g[LINE_Mb][80][79] = 2170.0

        self.mac_cm2_g[LINE_La][21] = {}
        self.mac_cm2_g[LINE_La][21][21] = 4750.0

        self.mac_cm2_g[LINE_La][22] = {}
        self.mac_cm2_g[LINE_La][22][22] = 4550.0

        self.mac_cm2_g[LINE_La][23] = {}
        self.mac_cm2_g[LINE_La][23][23] = 4370.0

        self.mac_cm2_g[LINE_La][24] = {}
        self.mac_cm2_g[LINE_La][24][24] = 3850.0

        self.mac_cm2_g[LINE_La][25] = {}
        self.mac_cm2_g[LINE_La][25][25] = 3340.0

        self.mac_cm2_g[LINE_La][26] = {}
        self.mac_cm2_g[LINE_La][26][26] = 3350.0

        self.mac_cm2_g[LINE_La][27] = {}
        self.mac_cm2_g[LINE_La][27][27] = 3260.0

        self.mac_cm2_g[LINE_La][28] = {}
        self.mac_cm2_g[LINE_La][28][28] = 3560.0

        self.mac_cm2_g[LINE_La][29] = {}
        self.mac_cm2_g[LINE_La][29][29] = 1755.0


    def extractTransitionKey(self, lineEmitter):
        xrayTransitionKeys = self.mac_cm2_g.keys()
        xrayTransitionKeys.sort()

        for xrayTransitionKey in xrayTransitionKeys:
            if lineEmitter in xrayTransitionKey:
                return xrayTransitionKey

            if len(lineEmitter) > len(xrayTransitionKey):
                if lineEmitter[:len(xrayTransitionKey)] in xrayTransitionKey:
                    return xrayTransitionKey

        return lineEmitter

if __name__ == '__main__': #pragma: no cover
    import DrixUtilities.Runner as Runner
    Runner.Runner().run(runFunction=None)
