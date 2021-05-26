#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: xray.mac.models.MacHenkeWinxray
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

MAC Henke model from Winxray program.
"""

###############################################################################
# Copyright 2021 Hendrix Demers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

# Standard library modules.
from configparser import ConfigParser
import os.path
import struct

# Third party modules.

# Local modules.

# Project modules.
from xray.mac.models.elements import ElementProperties

# Globals and constants variables.


class MacHenkeWinxray(object):
    def __init__(self, data_path):
        self.data_path = data_path
        self.pathnameBinary = os.path.join(data_path, "binary")
        self.pathnameText = os.path.join(data_path, "text")

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

        # energyMinimum, energyMaximum = struct.unpack('f'*2, data[start:stop])

        start, stop = stop, stop + struct.calcsize('if')

        numberPoints = struct.unpack('if', data[start:stop])[0]

        energies_eV = [0.0]*numberPoints
        mac_cm2_g = [0.0]*numberPoints

        for index in range(numberPoints):
            start, stop = stop, stop + struct.calcsize('ff')

            values = struct.unpack('ff', data[start:stop])

            # energies_eV.append(values[0])
            # mac_cm2_g.append(values[1])

            energies_eV[index] = values[0]
            mac_cm2_g[index] = values[1]

        return energies_eV, mac_cm2_g
