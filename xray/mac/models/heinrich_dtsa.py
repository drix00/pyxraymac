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

# Third party modules.

# Local modules.

# Project modules.
from xray.mac.models.ionization_energies import IonizationEnergies
from xray.mac.models.element_properties import get_atomic_mass_g_mol

# Globals and constants variables.


class MacHeinrichDTSA:
    def __init__(self):
        self.ionization_energies = IonizationEnergies()

    def compute_mac_cm2_g(self, energy_eV, atomic_number):  # noqa
        if energy_eV <= 10.0:
            return 1e6

        if atomic_number < 3 or atomic_number > 95:
            return 0.001

        z = atomic_number
        bias = 0

        ee_K = self.ionization_energies.ionization_energy_eV(z, 'K')  # noqa

        try:
            ee_NI = self.ionization_energies.ionization_energy_eV(z, 'N1')  # noqa
        except KeyError:
            ee_NI = 0.0  # noqa

        # energy is above the K edge.
        if energy_eV > ee_K:
            if z < 6:
                cc = 1.808599e-3 * z - 2.87536e-4
                az = (-14.15422 * z + 155.6055) * z + 24.4545
                bias = 18.2 * z - 103.0
                nm = (-0.01273815 * z + 0.02652873) * z + 3.34745
            else:
                cc = 5.253e-3 + z * (1.33257e-3 + z * (-7.5937e-5 + z * (1.69357e-6 + -1.3975e-8 * z)))
                az = ((-0.152624 * z + 6.52) * z + 47.0) * z
                nm = 3.112 - 0.0121 * z

                # These special conditions are not mentioned in the IXCOM 11
                # article but are implemented in DTSA
                assert(energy_eV > ee_K)

                if z >= 50:
                    az = ((-0.015 * z + 3.52) * z + 47) * z

                if z >= 57:
                    cc = 2.0e-4 + (1.0e-4 - z) * z
        else:
            try:
                ee_LIII = self.ionization_energies.ionization_energy_eV(z, 'L3')  # noqa
            except KeyError:
                ee_LIII = 0.0  # noqa

            # energy is below K-edge & above L3-edge.
            if energy_eV > ee_LIII:
                factor1 = -9.07306E-10 + z * 3.19245E-12
                cc = -0.0924e-3 + z * (0.141478e-3 + z * (-0.00524999e-3 + z * (9.85296E-8 + z * factor1)))
                az = (((-1.16286e-4 * z + 0.01253775) * z + 0.067429) * z + 17.8096) * z
                nm = (-4.982E-5 * z + 1.889e-3) * z + 2.7575

                try:
                    ee_LII = self.ionization_energies.ionization_energy_eV(z, 'L2')  # noqa
                except KeyError:
                    ee_LII = 0.0  # noqa

                try:
                    eeLI = self.ionization_energies.ionization_energy_eV(z, 'L1')  # noqa
                except KeyError:
                    eeLI = 0.0  # noqa

                if eeLI > energy_eV > ee_LII:
                    cc *= 0.858

                if energy_eV < ee_LII:
                    cc *= (0.8933 + z * (-8.29e-3 + 6.38E-5 * z))

            else:
                try:
                    ee_MI = self.ionization_energies.ionization_energy_eV(z, 'M1')  # noqa
                except KeyError:
                    ee_MI = 0.0  # noqa

                if ee_LIII >= energy_eV > ee_MI:
                    nm = ((4.4509E-6 * z - 1.08246e-3) * z + 0.084597) * z + 0.5385

                    if z < 30:
                        factor1 = z + 1.889757e-2
                        cc = (((7.2773258e-9 * z - 1.1641145e-6) * z + 6.9602789e-5) * z - 1.8517159e-3) * factor1
                    else:
                        factor1 = z + 3.0039e-3
                        cc = (((1.497763e-10 * z - 4.0585911e-8) * z + 4.0424792e-6) * z - 1.73663566e-4) * factor1

                    az = (((-1.8641019e-4 * z + 2.63199611e-2) * z - 0.822863477) * z + 10.2575657) * z

                    if z < 61:
                        bias = (((-1.683474e-4 * z + 0.018972278) * z - 0.536839169) * z + 5.654) * z
                    else:
                        bias = (((3.1779619e-3 * z - 0.699473097) * z + 51.114164) * z - 1232.4022) * z
                else:
                    ee_MV = self.ionization_energies.ionization_energy_eV(z, 'M5')  # noqa

                    if energy_eV >= ee_MV:
                        ee_MIV = self.ionization_energies.ionization_energy_eV(z, 'M4')  # noqa

                        az = (4.62 - 0.04 * z) * z
                        cc = ((-1.29086e-9 * z + 2.209365e-7) * z - 7.83544e-6) * z + 7.7708e-5
                        cc *= ((4.865E-6 * z - 0.0006561) * z + 0.0162) * z + 1.406
                        bias = ((3.78e-4 * z - 0.052) * z + 2.51) * ee_MIV
                        nm = 3.0 - 0.004 * z

                        ee_MII = self.ionization_energies.ionization_energy_eV(z, 'M2')  # noqa
                        ee_MIII = self.ionization_energies.ionization_energy_eV(z, 'M3')  # noqa

                        if energy_eV >= ee_MII:
                            assert(energy_eV <= ee_MI)

                            cc *= ((-0.0001285 * z + 0.01955) * z + 0.584)
                        elif energy_eV >= ee_MIII:
                            assert(energy_eV < ee_MII)

                            cc *= 0.001366 * z + 1.082
                        elif energy_eV >= ee_MIV:
                            assert(energy_eV < ee_MIII)

                            cc *= 0.95
                        else:
                            assert(energy_eV < ee_MIV)
                            assert(energy_eV >= ee_MV)

                            cc *= (4.0664e-4 * z - 4.8e-2) * z + 1.6442
                    else:
                        assert(energy_eV < ee_MV)

                        cc = 1.08 * (((-6.69827e-9 * z + 1.707073e-6) * z - 1.4653e-4) * z + 4.3156e-3)
                        az = ((5.39309e-3 * z - 0.61239) * z + 19.64) * z
                        bias = 4.5 * z - 113.0
                        nm = 0.3736 + 0.02401 * z

        atomic_weight = get_atomic_mass_g_mol(z)

        if energy_eV > ee_NI:
            mu = cc * math.pow(12397.0 / energy_eV, nm) * z * z * z * z / atomic_weight
            mu = mu * (1 - math.exp((bias - energy_eV) / az))
        else:
            factor1 = 1 - math.exp((bias - ee_NI) / az)
            mu = cc * math.pow(12397.0 / energy_eV, nm) * z * z * z * z / atomic_weight * factor1

            cutoff = self.get_cutoff(z)

            mu = 1.02 * mu * (energy_eV - cutoff) / (ee_NI - cutoff)

        mu_cm2_g = mu

        return mu_cm2_g

    @staticmethod
    def get_cutoff(atomic_number):  # noqa
        r"""
        Compute the cut off value.

        \param[in] atomic_number
        """
        return 10.0
