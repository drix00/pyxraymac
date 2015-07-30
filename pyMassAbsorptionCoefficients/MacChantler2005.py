#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2940 $"
__svnDate__ = "$Date: 2014-11-26 19:25:19 -0500 (Wed, 26 Nov 2014) $"
__svnId__ = "$Id: Chantler2005.py 2940 2014-11-27 00:25:19Z hdemers $"

# Standard library modules.
try:
    from configparser import SafeConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser
import os.path
import csv
import logging

# Third party modules.

# Local modules.
import pyHendrixDemersTools.Files as Files
import pyNumericalMethodsTools.Interpolation.Interpolation1D as Interpolation1D

# Globals and constants variables.
SECTION_NAME = "Chantler2005"
OPTION_PATHNAME = "pathname"
OPTION_FILENAME = "filename"
OPTION_ENERGY_UNIT = "energyUnit"

ENERGIES_eV = "energies_eV"
MAC_cm2_g = "mac_cm2_g"

ENERGY_UNIT_eV = "eV"
ENERGY_UNIT_keV = "keV"

class Chantler2005(object):
    def __init__(self, configurationPath):
        self._readConfiguration(configurationPath)
        self._createFilepath()

        self.minimumEnergy_eV = 0.0

        self.minimumMAC_cm2_g = 0.0

        self.macData = {}

    def _readConfiguration(self, configurationPath):
        """
        Read the configuration file for options.

        :param configurationPath: Configuration file path.
        """
        config = SafeConfigParser()

        config.readfp(open(configurationPath))

        if config.has_section(SECTION_NAME):
            if config.has_option(SECTION_NAME, OPTION_PATHNAME):
                self._pathname = config.get(SECTION_NAME, OPTION_PATHNAME)

            if config.has_option(SECTION_NAME, OPTION_FILENAME):
                self._filename = config.get(SECTION_NAME, OPTION_FILENAME)

            if config.has_option(SECTION_NAME, OPTION_ENERGY_UNIT):
                self._energyUnit = config.get(SECTION_NAME, OPTION_ENERGY_UNIT)

    def _createFilepath(self):
        self._filepath = os.path.join(self._pathname, self._filename)

    def _readFile(self):
        self._resetData()
        inputFile = csv.reader(open(self._filepath))

        for items in inputFile:
            self._extractDataFromItemsLine(items)

    def _resetData(self):
        self._experimentalData = {}

    def _extractDataFromItemsLine(self, items):
        index = 0
        maximumIndex = len(items)
        atomicNumber = 1

        while index < maximumIndex:
            try:
                if items[index] != '':
                    if self._energyUnit == ENERGY_UNIT_keV:
                        energy_keV = float(items[index])
                        energy_eV = energy_keV*1.0e3
                    else:
                        energy_eV = float(items[index])

                    mac_cm2_g = float(items[index+1])

                    if energy_eV > 0.0:
                        self._experimentalData.setdefault(atomicNumber, {})
                        self._experimentalData[atomicNumber].setdefault(ENERGIES_eV, []).append(energy_eV)
                        self._experimentalData[atomicNumber].setdefault(MAC_cm2_g, []).append(mac_cm2_g)
            except ValueError as status:
                logging.error(status)
                logging.info(items)

            atomicNumber += 1
            index += 2

    def computeMac_cm2_g(self, energyEmitter_eV, atomicNumberAbsorber):
        return self._computeMac_cm2_g(energyEmitter_eV, atomicNumberAbsorber)

    def _computeMac_cm2_g(self, energyEmitter_eV, atomicNumberAbsorber):
        if not atomicNumberAbsorber in self.macData:
            self._readFile()

            energies_eV = self._experimentalData[atomicNumberAbsorber][ENERGIES_eV]
            macs_cm2_g = self._experimentalData[atomicNumberAbsorber][MAC_cm2_g]

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

def compareBothVersions():
    import pylab

    configurationPath = Files.getCurrentModulePath(__file__, "../testData/DatabasesTests.cfg")
    mac = Chantler2005(configurationPath)

    atomicNumbers = [1, 6, 29, 92]
    filenames = {"NISTMonte2": "FFastMAC_nistMonte2.csv", "DTSA2": "FFastMAC_DTSA2.csv"}

    for atomicNumber in atomicNumbers:
        pylab.figure()
        for filenameKey in filenames:
            filename = filenames[filenameKey]

            mac._filename = filename
            if filenameKey == "NISTMonte2":
                mac._energyUnit = ENERGY_UNIT_eV
            elif filenameKey == "DTSA2":
                mac._energyUnit = ENERGY_UNIT_keV

            mac._createFilepath()
            mac._readFile()

            energies_eV = mac._experimentalData[atomicNumber][ENERGIES_eV]
            mac_cm2_g = mac._experimentalData[atomicNumber][MAC_cm2_g]

            pylab.loglog(energies_eV, mac_cm2_g, label=filenameKey)

        pylab.legend()
        pylab.title(atomicNumber)

    pylab.show()

if __name__ == '__main__':    #pragma: no cover
    compareBothVersions()
