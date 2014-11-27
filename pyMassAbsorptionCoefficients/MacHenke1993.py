#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2007 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2922 $"
__svnDate__ = "$Date: 2013-10-13 21:15:14 -0400 (Sun, 13 Oct 2013) $"
__svnId__ = "$Id: MacHenke1993.py 2922 2013-10-14 01:15:14Z hdemers $"

# Standard library modules.
import logging

# Third party modules.
import numpy

# Local modules.
import pyMassAbsorptionCoefficients.MassAbsorptionCoefficientEnergy as MassAbsorptionCoefficientEnergy
import DatabasesTools.Mac.Henke.MacHenkeWinxray as MacHenkeWinxray
import DatabasesTools.Mac.Henke.MacHenke as MacHenke
import pyNumericalMethodsTools.Interpolation.Interpolation1D as Interpolation1D

# Globals and constants variables.

class MacHenke1993(MassAbsorptionCoefficientEnergy.MassAbsorptionCoefficientEnergy):
    def __init__(self, configurationFile, model='Henke'):
        if model == 'HenkeWinxray':
            self.macModel = MacHenkeWinxray.MacHenkeWinxray(configurationFile)
        else:
            self.macModel = MacHenke.MacHenke(configurationFile)

        self.minimumEnergy_eV = 0.0

        self.minimumMAC_cm2_g = 0.0

        self.macData = {}

        self._vec_computeMac_cm2_g = numpy.vectorize(self._computeMac_cm2_g)

    def computeMac_cm2_g(self, energyEmitter_eV, atomicNumberAbsorber):
        if isinstance(energyEmitter_eV, numpy.ndarray):
            return self._vec_computeMac_cm2_g(energyEmitter_eV, atomicNumberAbsorber)
        else:
            return self._computeMac_cm2_g(energyEmitter_eV, atomicNumberAbsorber)

    def _computeMac_cm2_g(self, energyEmitter_eV, atomicNumberAbsorber):
        if not atomicNumberAbsorber in self.macData:
            energies_eV, macs_cm2_g = self.macModel.readData(atomicNumberAbsorber)

            if len(energies_eV) > 0:
                self.macData.setdefault(atomicNumberAbsorber, {})

                self.minimumEnergy_eV = energies_eV[0]

                self.minimumMAC_cm2_g = macs_cm2_g[0]

                self.maximumEnergy_eV = energies_eV[-1]

                self.maximumMAC_cm2_g = macs_cm2_g[-1]

                self.macData[atomicNumberAbsorber] = Interpolation1D.Interpolation1D(energies_eV, macs_cm2_g)

            else:
                logging.error("No mac for %i and %0.1f", atomicNumberAbsorber, energyEmitter_eV)
                return 0.0

        if energyEmitter_eV <= self.minimumEnergy_eV:
            return self.minimumMAC_cm2_g

        if energyEmitter_eV >= self.maximumEnergy_eV:
            return self.maximumMAC_cm2_g

        if atomicNumberAbsorber in self.macData:
            return self.macData[atomicNumberAbsorber](energyEmitter_eV)
        else:
            logging.error("No mac for %i and %0.1f", atomicNumberAbsorber, energyEmitter_eV)
            return 0.0


def run():
    macHenke1993 = MacHenke1993("MassAbsorptionCoefficient.cfg")
    xrayKaLines = {'Cr': 5414.0, 'Mn': 5898.0, 'Ni': 7477.0}

    atomicNumberAbsorber = 26

    for element in xrayKaLines:
        energyEmitter_eV = xrayKaLines[element]
        mac_cm2_g = macHenke1993.computeMac_cm2_g(energyEmitter_eV, atomicNumberAbsorber)
        print("%s: %f" % (element, mac_cm2_g))

def runAl():
    macHenke1993 = MacHenke1993("MassAbsorptionCoefficient.cfg")
    xrayKaLines = {'Al': 1487.0}

    atomicNumberAbsorber = 13

    for element in xrayKaLines:
        energyEmitter_eV = xrayKaLines[element]
        mac_cm2_g = macHenke1993.computeMac_cm2_g(energyEmitter_eV, atomicNumberAbsorber)
        print("%s: %f" % (element, mac_cm2_g))

if __name__ == '__main__': #pragma: no cover
    import pyHendrixDemersTools.Runner as Runner
    Runner.Runner().run(runFunction=runAl)
