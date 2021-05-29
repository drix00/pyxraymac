#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: xray.mac.models.henke1993
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Henke 1993 MAC model.
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
from xray.mac.models.henke import MacHenke
from xray.mac.models.henke_winxray import MacHenkeWinxray

# Globals and constants variables.
LINEAR = 'linear'
NEAREST = 'nearest'
ZERO = 'zero'
SLINEAR = 'slinear'
QUADRATIC = 'quadratic'
CUBIC = 'cubic'


class Interpolation1D:
    def __init__(self, x, y, kind=LINEAR):
        self._interpolateFunc = interp1d(x, y, kind=kind)

    def __call__(self, x_new):
        return self._interpolateFunc(x_new)


class MacHenke1993:
    def __init__(self, data_path, model='Henke'):
        if model == 'HenkeWinxray':
            self.mac_model = MacHenkeWinxray(data_path)
        else:
            self.mac_model = MacHenke(data_path)

        self.minimumEnergy_eV = 0.0

        self.minimumMAC_cm2_g = 0.0

        self.mac_data = {}

        self._vec_computeMac_cm2_g = numpy.vectorize(self._compute_mac_cm2_g)

    def compute_mac_cm2_g(self, energy_emitter_eV, atomic_number_absorber):  # noqa
        if isinstance(energy_emitter_eV, numpy.ndarray):
            return self._vec_computeMac_cm2_g(energy_emitter_eV, atomic_number_absorber)
        else:
            return self._compute_mac_cm2_g(energy_emitter_eV, atomic_number_absorber)

    def _compute_mac_cm2_g(self, energy_emitter_eV, atomic_number_absorber):  # noqa
        if atomic_number_absorber not in self.mac_data:
            energies_eV, macs_cm2_g = self.mac_model.read_data(atomic_number_absorber)  # noqa

            if len(energies_eV) > 0:
                self.mac_data.setdefault(atomic_number_absorber, {})

                self.minimumEnergy_eV = energies_eV[0]

                self.minimumMAC_cm2_g = macs_cm2_g[0]

                self.maximumEnergy_eV = energies_eV[-1]

                self.maximumMAC_cm2_g = macs_cm2_g[-1]

                self.mac_data[atomic_number_absorber] = Interpolation1D(energies_eV, macs_cm2_g)

            else:
                logging.error("No mac for %i and %0.1f", atomic_number_absorber, energy_emitter_eV)
                return 0.0

        if energy_emitter_eV <= self.minimumEnergy_eV:
            return self.minimumMAC_cm2_g

        if energy_emitter_eV >= self.maximumEnergy_eV:
            return self.maximumMAC_cm2_g

        if atomic_number_absorber in self.mac_data:
            return self.mac_data[atomic_number_absorber](energy_emitter_eV)
        else:
            logging.error("No mac for %i and %0.1f", atomic_number_absorber, energy_emitter_eV)
            return 0.0
