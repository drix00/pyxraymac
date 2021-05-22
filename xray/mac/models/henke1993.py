#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: module_name
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Description
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
import logging

# Third party modules.
import numpy
from scipy.interpolate import interp1d

# Local modules.

# Project modules.
import xray.mac.models.MacHenke as MacHenke
import xray.mac.models.MacHenkeWinxray as MacHenkeWinxray

# Globals and constants variables.
LINEAR = 'linear'
NEAREST = 'nearest'
ZERO = 'zero'
SLINEAR = 'slinear'
QUADRATIC = 'quadratic'
CUBIC = 'cubic'


class Interpolation1D(object):
    def __init__(self, x, y, kind=LINEAR):
        self._interpolateFunc = interp1d(x, y, kind=kind)

        self._compute = self._computeV07

    def __call__(self, x_new):
        return self._compute(x_new)

    def _computeV07(self, xNew):
        return self._interpolateFunc(xNew)

    def _computeV06(self, xNew):
        return self._interpolateFunc(xNew)[0]


class MacHenke1993:
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

                self.macData[atomicNumberAbsorber] = Interpolation1D(energies_eV, macs_cm2_g)

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


def run_al():
    macHenke1993 = MacHenke1993("MassAbsorptionCoefficient.cfg")
    xrayKaLines = {'Al': 1487.0}

    atomicNumberAbsorber = 13

    for element in xrayKaLines:
        energyEmitter_eV = xrayKaLines[element]
        mac_cm2_g = macHenke1993.computeMac_cm2_g(energyEmitter_eV, atomicNumberAbsorber)
        print("%s: %f" % (element, mac_cm2_g))


if __name__ == '__main__':  # pragma: no cover
    run_al()
