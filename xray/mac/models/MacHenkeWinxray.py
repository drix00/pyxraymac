#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2007 Hendrix Demers"
__license__ = ""

# Standard library modules.
from configparser import ConfigParser
import os.path
import struct

# Third party modules.

# Local modules.
from xray.mac.models.elements import ElementProperties

# Globals and constants variables.

class MacHenkeWinxray(object):
    def __init__(self, configurationFile):
        self.readConfigurationFile(configurationFile)

    def readConfigurationFile(self, configurationFile):
        """ Read the configuration file for options."""
        # pylint: disable-msg=W0201
        config = ConfigParser()

        config.read_file(open(configurationFile))

        if config.has_section("MacHenkeWinxray"):
            if config.has_option("MacHenkeWinxray", "pathnameBinary"):
                self.pathnameBinary = config.get("MacHenkeWinxray", "pathnameBinary")

            if config.has_option("MacHenkeWinxray", "pathnameText"):
                self.pathnameText = config.get("MacHenkeWinxray", "pathnameText")

    def readData(self, atomicNumber):
        return self.readTextData(atomicNumber)

    def readTextData(self, atomicNumber):
        element_properties = ElementProperties()
        symbol = element_properties.symbol(atomicNumber).lower()

        filename = symbol + '.dat'

        filename = os.path.join(self.pathnameText, filename)

        lines = open(filename, 'r').readlines()

        energies_eV = []
        mac_cm2_g = []

        for line in lines:
            values = line.split('\t')

            energies_eV.append(float(values[0]))

            mac_cm2_g.append(float(values[1]))

        return energies_eV, mac_cm2_g

    def readBinaryData(self, atomicNumber):
        element_properties = ElementProperties()
        symbol = element_properties.symbol(atomicNumber).lower()

        filename = symbol + '_eV.mhb'

        filename = os.path.join(self.pathnameBinary, filename)

        data = open(filename, 'rb').read()

        dummy_start, stop = 0, struct.calcsize('f'*2)

        #energyMinimum, energyMaximum = struct.unpack('f'*2, data[start:stop])

        start, stop = stop, stop + struct.calcsize('if')

        numberPoints = struct.unpack('if', data[start:stop])[0]

        energies_eV = [0.0]*numberPoints
        mac_cm2_g = [0.0]*numberPoints

        for index in range(numberPoints):
            start, stop = stop, stop + struct.calcsize('ff')

            values = struct.unpack('ff', data[start:stop])

            #energies_eV.append(values[0])
            #mac_cm2_g.append(values[1])

            energies_eV[index] = values[0]
            mac_cm2_g[index] = values[1]

        return energies_eV, mac_cm2_g
