#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2007 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2293 $"
__svnDate__ = "$Date: 2011-03-21 14:39:25 -0400 (Mon, 21 Mar 2011) $"
__svnId__ = "$Id: MassAbsorptionCoefficientEmitter.py 2293 2011-03-21 18:39:25Z hdemers $"

# Standard library modules.

# Third party modules.

# Local modules.

# Globals and constants variables.

class MassAbsorptionCoefficientEmitter(object):
    def __init__(self):
        self.mac_cm2_g = None

    def isAvailable(self, atomicNumberAbsorber, atomicNumberEmitter, lineEmitter):
        xrayTransitionKey = self.extractTransitionKey(lineEmitter)

        if xrayTransitionKey    in self.mac_cm2_g:
            if atomicNumberEmitter in self.mac_cm2_g[xrayTransitionKey]:
                if atomicNumberAbsorber in self.mac_cm2_g[xrayTransitionKey][atomicNumberEmitter]:
                    return True

        return False

    def computeMac_cm2_g(self, atomicNumberAbsorber, atomicNumberEmitter, lineEmitter):
        if self.isAvailable(atomicNumberAbsorber, atomicNumberEmitter, lineEmitter):
            xrayTransitionKey = self.extractTransitionKey(lineEmitter)

            return self.mac_cm2_g[xrayTransitionKey][atomicNumberEmitter][atomicNumberAbsorber]

    def extractTransitionKey(self, lineEmitter):
        raise NotImplemented

if __name__ == '__main__': #pragma: no cover
    import DrixUtilities.Runner as Runner
    Runner.Runner().run(runFunction=None)
