#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: xray.mac.models.MassAbsorptionCoefficient
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Interface to the mass absorption coefficient models.
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
import configparser


# Third party modules.

# Local modules.

# Project modules.

# Globals and constants variables.


class MassAbsorptionCoefficient(object):
    def __init__(self, macEnergy=None, macEmitter=None, xrayTransitionData=None, configurationFile=None):
        if configurationFile:
            self.readConfiguration(configurationFile)

        self.macEnergy = macEnergy
        self.macEmitter = macEmitter
        self.xrayTransitionData = xrayTransitionData

    def readConfiguration(self, configurationFile):
        """ Read the configuration file for options."""
        config = configparser.ConfigParser()

        config.read_file(open(configurationFile))

    def mac_cm2_g(self, atomicNumberAbsorber
                  , energyEmitter_eV=None
                  , atomicNumberEmitter=None
                  , lineEmitter=None
                  ):
        if atomicNumberEmitter and lineEmitter:
            if self.macEmitter and self.macEmitter.is_available(atomicNumberAbsorber, atomicNumberEmitter, lineEmitter):
                return self.macEmitter.mac_cm2_g(atomicNumberAbsorber
                                                 , atomicNumberEmitter
                                                 , lineEmitter)
            else:
                energyEmitter_eV = self.xrayTransitionData.getTransitionEnergy_eV(atomicNumberEmitter
                                                                                  , lineEmitter)

        if energyEmitter_eV is not None:
            if self.macEnergy:
                return self.macEnergy.mac_cm2_g(energyEmitter_eV, atomicNumberAbsorber)

                # print atomicNumberAbsorber, energyEmitter_eV

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

            macTotal_cm2_g += weightFaction * elementMac_cm2_g

        return macTotal_cm2_g
