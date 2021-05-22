#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: xray.mac.models.heinrich_dtsa
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

MAC Heinrich model from DTSA program.
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
import math
import configparser

# Third party modules.

# Local modules.

# Project modules.
from xray.mac.models.ionization_energies import IonizationEnergies
from xray.mac.models.element_properties import get_atomic_mass_g_mol

# Globals and constants variables.


class MacHeinrichDTSA:
    def __init__(self, configuration_file=None):
        self.ionization_energies = IonizationEnergies()

        if configuration_file:
            self.readConfiguration(configuration_file)

    def readConfiguration(self, configuration_file):
        """ Read the configuration file for options."""
        config = configparser.ConfigParser()

        config.read_file(open(configuration_file))

        if config.has_section("MacHeinrichDTSA"):
            if config.has_option("MacHeinrichDTSA", "path"):
                self.dataPath = config.get("MacHeinrichDTSA", "path")

    def computeMac_cm2_g(self, energy_eV, atomicNumber):
        if energy_eV <= 10.0:
            return 1e6

        if atomicNumber < 3 or atomicNumber > 95:
            return 0.001

        bias = 0

        eeK = self.ionization_energies.ionization_energy_eV(atomicNumber, 'K1')

        try:
            eeNI = self.ionization_energies.ionization_energy_eV(atomicNumber, 'N1')
        except:
            eeNI = 0.0

        # energy is above the K edge.
        if energy_eV > eeK:
            if atomicNumber < 6:
                cc = 1.808599e-3 * atomicNumber - 2.87536e-4
                az = (-14.15422 * atomicNumber + 155.6055) * atomicNumber + 24.4545
                bias = 18.2 * atomicNumber - 103.0
                nm = (-0.01273815 * atomicNumber + 0.02652873) * atomicNumber + 3.34745
            else:
                cc = 5.253e-3 + atomicNumber * (1.33257e-3 + atomicNumber * (-7.5937e-5 + atomicNumber * (1.69357e-6 + -1.3975e-8 * atomicNumber)))
                az = ((-0.152624 * atomicNumber + 6.52) * atomicNumber + 47.0) * atomicNumber
                nm = 3.112 - 0.0121 * atomicNumber

                # These special conditions are not mentioned in the IXCOM 11
                # article but are implemented in DTSA
                assert(energy_eV > eeK)

                if atomicNumber >= 50:
                    az = ((-0.015 * atomicNumber + 3.52) * atomicNumber + 47) * atomicNumber

                if atomicNumber >= 57:
                    cc = 2.0e-4 + (1.0e-4 - atomicNumber) * atomicNumber
        else:
            try:
                eeLIII = self.ionization_energies.ionization_energy_eV(atomicNumber, 'L3')
            except:
                eeLIII = 0.0

            # energy is below K-edge & above L3-edge.
            if energy_eV > eeLIII:
                cc = -0.0924e-3 + atomicNumber * (0.141478e-3 + atomicNumber * (-0.00524999e-3 + atomicNumber * (9.85296E-8 + atomicNumber * (-9.07306E-10 + atomicNumber * 3.19245E-12))))
                az = (((-1.16286e-4 * atomicNumber + 0.01253775) * atomicNumber + 0.067429) * atomicNumber + 17.8096) * atomicNumber
                nm = (-4.982E-5 * atomicNumber + 1.889e-3) * atomicNumber + 2.7575

                try:
                    eeLII = self.ionization_energies.ionization_energy_eV(atomicNumber, 'L2')
                except:
                    eeLII = 0.0

                try:
                    eeLI = self.ionization_energies.ionization_energy_eV(atomicNumber, 'L1')
                except:
                    eeLI = 0.0

                if energy_eV < eeLI and energy_eV > eeLII:
                    cc *= 0.858

                if energy_eV < eeLII:
                    cc *= (0.8933 + atomicNumber * (-8.29e-3 + 6.38E-5 * atomicNumber))

            else:
                try:
                    eeMI = self.ionization_energies.ionization_energy_eV(atomicNumber, 'M1')
                except:
                    eeMI = 0.0

                if energy_eV <= eeLIII and energy_eV > eeMI:
                    nm = ((4.4509E-6 * atomicNumber - 1.08246e-3) * atomicNumber + 0.084597) * atomicNumber + 0.5385

                    if atomicNumber < 30:
                        cc = (((7.2773258e-9 * atomicNumber - 1.1641145e-6) * atomicNumber + 6.9602789e-5) * atomicNumber - 1.8517159e-3) * atomicNumber + 1.889757e-2
                    else:
                        cc = (((1.497763e-10 * atomicNumber - 4.0585911e-8) * atomicNumber + 4.0424792e-6) * atomicNumber - 1.73663566e-4) * atomicNumber + 3.0039e-3

                    az = (((-1.8641019e-4 * atomicNumber + 2.63199611e-2) * atomicNumber - 0.822863477) * atomicNumber + 10.2575657) * atomicNumber

                    if atomicNumber < 61:
                        bias = (((-1.683474e-4 * atomicNumber + 0.018972278) * atomicNumber - 0.536839169) * atomicNumber + 5.654) * atomicNumber
                    else:
                        bias = (((3.1779619e-3 * atomicNumber - 0.699473097) * atomicNumber + 51.114164) * atomicNumber - 1232.4022) * atomicNumber
                else:
                    eeMV = self.ionization_energies.ionization_energy_eV(atomicNumber, 'M5')

                    if energy_eV >= eeMV:
                        eeMIV = self.ionization_energies.ionization_energy_eV(atomicNumber, 'M4')

                        az = (4.62 - 0.04 * atomicNumber) * atomicNumber
                        cc = ((-1.29086e-9 * atomicNumber + 2.209365e-7) * atomicNumber - 7.83544e-6) * atomicNumber + 7.7708e-5
                        cc *= ((4.865E-6 * atomicNumber - 0.0006561) * atomicNumber + 0.0162) * atomicNumber + 1.406
                        bias = ((3.78e-4 * atomicNumber - 0.052) * atomicNumber + 2.51) * eeMIV
                        nm = 3.0 - 0.004 * atomicNumber

                        eeMII = self.ionization_energies.ionization_energy_eV(atomicNumber, 'M2')
                        eeMIII = self.ionization_energies.ionization_energy_eV(atomicNumber, 'M3')

                        if energy_eV >= eeMII:
                            assert(energy_eV <= eeMI)

                            cc *= ((-0.0001285 * atomicNumber + 0.01955) * atomicNumber + 0.584)
                        elif energy_eV >= eeMIII:
                            assert(energy_eV < eeMII)

                            cc *= 0.001366 * atomicNumber + 1.082
                        elif energy_eV >= eeMIV:
                            assert(energy_eV < eeMIII)

                            cc *= 0.95
                        else:
                            assert(energy_eV < eeMIV)
                            assert(energy_eV >= eeMV)

                            cc *= (4.0664e-4 * atomicNumber - 4.8e-2) * atomicNumber + 1.6442
                    else:
                        assert(energy_eV < eeMV)

                        cc = 1.08 * (((-6.69827e-9 * atomicNumber + 1.707073e-6) * atomicNumber - 1.4653e-4) * atomicNumber + 4.3156e-3)
                        az = ((5.39309e-3 * atomicNumber - 0.61239) * atomicNumber + 19.64) * atomicNumber
                        bias = 4.5 * atomicNumber - 113.0
                        nm = 0.3736 + 0.02401 * atomicNumber

        atomicWeight = get_atomic_mass_g_mol(atomicNumber)

        if energy_eV > eeNI:
            mu = cc * math.pow(12397.0 / energy_eV, nm) * atomicNumber * atomicNumber * atomicNumber * atomicNumber / atomicWeight
            mu = mu * (1 - math.exp((bias - energy_eV) / az))
        else:
            mu = cc * math.pow(12397.0 / energy_eV, nm) * atomicNumber * atomicNumber * atomicNumber * atomicNumber / atomicWeight * (1 - math.exp((bias - eeNI) / az))

            cutoff = self.getCutOff(atomicNumber)

            mu = 1.02 * mu * (energy_eV - cutoff) / (eeNI - cutoff)

        mu_cm2_g = mu

        return mu_cm2_g

    def getCutOff(self, atomicNumber):
        """
        Compute the cut off value.

        \param[in] atomicNumber
        """
        return 10.0
