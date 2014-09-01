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
__svnId__ = "$Id: MassAbsorptionCoefficient.py 2293 2011-03-21 18:39:25Z hdemers $"

# Standard library modules.
import ConfigParser

# Third party modules.

# Local modules.

# Globals and constants variables.

class MassAbsorptionCoefficient(object):
    def __init__(self
                             , macEnergy=None
                             , macEmitter=None
                             , xrayTransitionData=None
                             , configurationFile=None
                             ):
        if configurationFile:
            self.readConfiguration(configurationFile)

        self.macEnergy = macEnergy
        self.macEmitter = macEmitter
        self.xrayTransitionData = xrayTransitionData

    def readConfiguration(self, configurationFile):
        """ Read the configuration file for options."""
        config = ConfigParser.SafeConfigParser()

        config.readfp(open(configurationFile))

    def mac_cm2_g(self, atomicNumberAbsorber
                                , energyEmitter_eV=None
                                , atomicNumberEmitter=None
                                , lineEmitter=None
                                ):
        if atomicNumberEmitter and lineEmitter:
            if self.macEmitter and self.macEmitter.isAvailable(atomicNumberAbsorber, atomicNumberEmitter, lineEmitter):
                return self.macEmitter.computeMac_cm2_g(atomicNumberAbsorber
                                                                                        , atomicNumberEmitter
                                                                                        , lineEmitter)
            else:
                energyEmitter_eV = self.xrayTransitionData.getTransitionEnergy_eV(atomicNumberEmitter
                                                                                                                                                , lineEmitter)

        if energyEmitter_eV != None:
            if self.macEnergy:
                return self.macEnergy.computeMac_cm2_g(energyEmitter_eV, atomicNumberAbsorber)

        #print atomicNumberAbsorber, energyEmitter_eV

    def computeMacTotal_cm2_g(self, elements
                                , energyEmitter_eV=None
                                , atomicNumberEmitter=None
                                , lineEmitter=None
                                ):
        macTotal_cm2_g = 0.0

        for atomicNumberAbsorber in elements:
            element = elements[atomicNumberAbsorber]

            elementMac_cm2_g = self.mac_cm2_g(atomicNumberAbsorber, energyEmitter_eV, atomicNumberEmitter, lineEmitter)

            weightFaction = element.weightFraction

            macTotal_cm2_g += weightFaction*elementMac_cm2_g

        return macTotal_cm2_g

if __name__ == '__main__': #pragma: no cover
    import DrixUtilities.Runner as Runner
    Runner.Runner().run(runFunction=None)
