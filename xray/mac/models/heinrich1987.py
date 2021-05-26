#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: xray.mac.models.heinrich1987
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

MAC Heinrich 1987 model.
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
import warnings
import logging

# Third party modules.
import numpy

# Local modules.

# Project modules.
from xray.mac.models.element_properties import get_atomic_mass_g_mol
from xray.mac.models.ionization_energies import IonizationEnergiesDtsa


# Globals and constants variables.


class MacHeinrich1987:
    def __init__(self):
        self.ionization_energies = IonizationEnergiesDtsa()

        self.coefficient_C = {
            1: self.compute_C_region1,
            2: self.compute_C_region2,
            3: self.compute_C_region3,
            4: self.compute_C_region4,
            5: self.compute_C_region5,
            6: self.compute_C_region6,
            7: self.compute_C_region7,
            8: self.compute_C_region8,
            9: self.compute_C_region9,
            10: self.compute_C_region10,
            11: self.compute_C_region11}

        self.coefficient_n = {
            1: self.compute_n_region1,
            2: self.compute_n_region2_4,
            3: self.compute_n_region2_4,
            4: self.compute_n_region2_4,
            5: self.compute_n_region5,
            6: self.compute_n_region6_9,
            7: self.compute_n_region6_9,
            8: self.compute_n_region6_9,
            9: self.compute_n_region6_9,
            10: self.compute_n_region10,
            11: self.compute_n_region11}

        self.coefficient_b_eV = {
            1: self.compute_b_region1,
            2: self.compute_b_region2_4,
            3: self.compute_b_region2_4,
            4: self.compute_b_region2_4,
            5: self.compute_b_region5,
            6: self.compute_b_region6_9,
            7: self.compute_b_region6_9,
            8: self.compute_b_region6_9,
            9: self.compute_b_region6_9,
            10: self.compute_b_region10}

        self.coefficient_a = {
            1: self.compute_a_region1,
            2: self.compute_a_region2_4,
            3: self.compute_a_region2_4,
            4: self.compute_a_region2_4,
            5: self.compute_a_region5,
            6: self.compute_a_region6_9,
            7: self.compute_a_region6_9,
            8: self.compute_a_region6_9,
            9: self.compute_a_region6_9,
            10: self.compute_a_region10,
            11: self.compute_a_region10}

        self._vec_computeMac_cm2_g = numpy.vectorize(self._compute_mac_cm2_g)

    @staticmethod
    def check_xray_energy_close_edge_energy(xray_energy_eV, edge_energy_eV):  # noqa
        """Warning -5 eV or + 20 eV from edge energy."""
        difference_energy_eV = xray_energy_eV - edge_energy_eV  # noqa

        if -5.0 <= difference_energy_eV <= 20.0:
            args = (xray_energy_eV, edge_energy_eV, difference_energy_eV)
            message = "X-ray emitted (%0.1f eV) is near the energy edge (%0.1f eV) by %0.1f eV." % args
            warnings.warn(message)
            logging.warning(message)

    @staticmethod
    def check_very_low_energy_eV(energy_emitter_eV, energy_limit_eV=180.0):  # noqa
        """Warning for energy below 180 eV or below 1.1*cutoff."""
        if energy_emitter_eV <= energy_limit_eV:
            args = (energy_emitter_eV, energy_limit_eV)
            message = "X-ray emitted (%0.1f eV) is very low, less than limit (%0.1f)." % args
            warnings.warn(message)
            logging.warning(message)

    @staticmethod
    def check_energy_between_m4_m5_z(region, atomic_number):
        """Warning for energy between M4 and M5 for elements of Z < 70."""
        if region == 9 and atomic_number < 70:
            message = "X-ray emitted between M4 and M5 for element %i." % atomic_number
            warnings.warn(message)
            logging.warning(message)

    @staticmethod
    def check_energy_below_m5(region):
        """Warning if the energy is below the edge M5 of the absorber."""
        if region >= 10:
            message = "X-ray emitted below M5."
            warnings.warn(message)
            logging.warning(message)

    def compute_mac_cm2_g(self, energy_emitter_eV, atomic_number_absorber):  # noqa
        if isinstance(energy_emitter_eV, numpy.ndarray):
            return self._vec_computeMac_cm2_g(energy_emitter_eV, atomic_number_absorber)
        else:
            return self._compute_mac_cm2_g(energy_emitter_eV, atomic_number_absorber)

    def _compute_mac_cm2_g(self, energy_emitter_eV, atomic_number_absorber):  # noqa
        if energy_emitter_eV <= 0.0:
            return 1.0E6

        self.check_very_low_energy_eV(energy_emitter_eV)

        region = self.get_region(atomic_number_absorber, energy_emitter_eV)
        self.check_energy_below_m5(region)

        self.check_energy_between_m4_m5_z(region, atomic_number_absorber)

        C = self.coefficient_C[region](atomic_number_absorber)  # noqa

        n = self.coefficient_n[region](atomic_number_absorber)  # noqa

        atomic_mass_g_mol = get_atomic_mass_g_mol(atomic_number_absorber)

        if region == 11:
            cutoff_eV = self.compute_cutoff_eV(atomic_number_absorber)  # noqa

            self.check_very_low_energy_eV(energy_emitter_eV, energy_limit_eV=cutoff_eV * 1.1)

            mac_cm2_g = self.compute_model2(atomic_number_absorber, atomic_mass_g_mol, energy_emitter_eV, C, n,
                                            cutoff_eV)

            # mac_cm2_g = self.compute_model2b(atomic_numberAbsorber, atomic_mass_g_mol, energyEmitter_eV, C, n,
            #                                  cutoff_eV)

            if mac_cm2_g < 0.0:
                return 1.0E6

            return mac_cm2_g
        else:
            b_eV = self.coefficient_b_eV[region](atomic_number_absorber)  # noqa

            a = self.coefficient_a[region](atomic_number_absorber)  # noqa

            mac_cm2_g = self.compute_model1(atomic_number_absorber, atomic_mass_g_mol, energy_emitter_eV, C, n, b_eV, a)

            if mac_cm2_g < 0.0:
                return 1.0E6

            return mac_cm2_g

    def compute_model1(self, atomic_number, atomic_mass_g_mol, xray_energy_eV, C, n, b_eV, a):  # noqa
        factor1 = C * math.pow(atomic_number, 4) / atomic_mass_g_mol

        factor2 = math.pow(12397.0 / xray_energy_eV, n)

        arg_exp = (-xray_energy_eV + b_eV) / a

        factor3 = 1.0 - math.exp(arg_exp)

        mac_cm2_g = factor1 * factor2 * factor3

        return mac_cm2_g

    def compute_model2(self, atomic_number, atomic_mass_g_mol, xray_energy_eV, C, n, cutoff_eV):  # noqa
        # Typo in equation (4) : 1.02 C should be 1.02, C is twice in the equation.
        # factor1 = 1.02 * C
        factor1 = 1.02

        factor2 = math.pow(12397.0 / xray_energy_eV, n)

        factor3 = C * math.pow(atomic_number, 4) / atomic_mass_g_mol

        nominator = xray_energy_eV - cutoff_eV

        edge_energy_n1_eV = self.ionization_energies.ionization_energy_eV(atomic_number, 'N1')  # noqa

        denominator = edge_energy_n1_eV - cutoff_eV

        factor4 = nominator / denominator

        mac_cm2_g = factor1 * factor2 * factor3 * factor4

        return mac_cm2_g

    def compute_model2b(self, atomic_number, atomic_mass_g_mol, xray_energy_eV, C, n, cutoff_eV):  # noqa

        edge_energy_n1_eV = self.ionization_energies.ionization_energy_eV(atomic_number, 'N1')  # noqa

        b_eV = self.coefficient_b_eV[10](atomic_number)  # noqa

        a = self.coefficient_a[10](atomic_number)  # noqa

        factor1 = self.compute_model1(atomic_number, atomic_mass_g_mol, edge_energy_n1_eV, C, n, b_eV, a)

        nominator = xray_energy_eV - cutoff_eV

        denominator = edge_energy_n1_eV - cutoff_eV

        factor4 = nominator / denominator

        mac_cm2_g = 1.02 * factor1 * factor4

        return mac_cm2_g

    def get_region(self, atomic_number, xray_energy_eV):  # noqa
        # Region 1
        edge_energy_K_eV = self.ionization_energies.ionization_energy_eV(atomic_number, 'K')  # noqa

        self.check_xray_energy_close_edge_energy(xray_energy_eV, edge_energy_K_eV)

        if xray_energy_eV >= edge_energy_K_eV:
            return 1

        # Region 2
        edge_energy_L1_eV = self.ionization_energies.ionization_energy_eV(atomic_number, 'L1')  # noqa

        self.check_xray_energy_close_edge_energy(xray_energy_eV, edge_energy_L1_eV)

        if edge_energy_K_eV >= xray_energy_eV > edge_energy_L1_eV:
            return 2

        # Region 3
        edge_energy_L2_eV = self.ionization_energies.ionization_energy_eV(atomic_number, 'L2')  # noqa

        self.check_xray_energy_close_edge_energy(xray_energy_eV, edge_energy_L2_eV)

        if edge_energy_L1_eV >= xray_energy_eV > edge_energy_L2_eV:
            return 3

        # Region 4
        edge_energy_L3_eV = self.ionization_energies.ionization_energy_eV(atomic_number, 'L3')  # noqa

        self.check_xray_energy_close_edge_energy(xray_energy_eV, edge_energy_L3_eV)

        if edge_energy_L2_eV >= xray_energy_eV > edge_energy_L3_eV:
            return 4

        # Region 5
        edge_energy_M1_eV = self.ionization_energies.ionization_energy_eV(atomic_number, 'M1')  # noqa

        self.check_xray_energy_close_edge_energy(xray_energy_eV, edge_energy_M1_eV)

        if edge_energy_L3_eV >= xray_energy_eV > edge_energy_M1_eV:
            return 5

        # Region 6
        edge_energy_M2_eV = self.ionization_energies.ionization_energy_eV(atomic_number, 'M2')  # noqa

        self.check_xray_energy_close_edge_energy(xray_energy_eV, edge_energy_M2_eV)

        if edge_energy_M1_eV >= xray_energy_eV > edge_energy_M2_eV:
            return 6

        # Region 7
        edge_energy_M3_eV = self.ionization_energies.ionization_energy_eV(atomic_number, 'M3')  # noqa

        self.check_xray_energy_close_edge_energy(xray_energy_eV, edge_energy_M3_eV)

        if edge_energy_M2_eV >= xray_energy_eV > edge_energy_M3_eV:
            return 7

        # Region 8
        edge_energy_M4_eV = self.ionization_energies.ionization_energy_eV(atomic_number, 'M4')  # noqa

        self.check_xray_energy_close_edge_energy(xray_energy_eV, edge_energy_M4_eV)

        if edge_energy_M3_eV >= xray_energy_eV > edge_energy_M4_eV:
            return 8

        # Region 9
        edge_energy_M5_eV = self.ionization_energies.ionization_energy_eV(atomic_number, 'M5')  # noqa

        self.check_xray_energy_close_edge_energy(xray_energy_eV, edge_energy_M5_eV)

        if edge_energy_M4_eV >= xray_energy_eV > edge_energy_M5_eV:
            return 9

        # Region 10
        edge_energy_N1_eV = self.ionization_energies.ionization_energy_eV(atomic_number, 'N1')  # noqa

        self.check_xray_energy_close_edge_energy(xray_energy_eV, edge_energy_N1_eV)

        if edge_energy_M5_eV >= xray_energy_eV > edge_energy_N1_eV:
            return 10

        # Region 11
        if edge_energy_N1_eV >= xray_energy_eV:
            return 11

        raise RuntimeError("Region not found for Z={}, E_X={}, E_N1={}".format(atomic_number, xray_energy_eV,
                                                                               edge_energy_N1_eV))

    @staticmethod
    def compute_coefficient(atomic_number, coefficients):
        r"""
        Compute the value of the coefficient C, n, a, or b:

        $C = \sum C_{i} \cdot Z^{i}$
        $n = \sum n_{i} \cdot Z^{i}$
        $a = \sum a_{i} \cdot Z^{i}$
        $b = \sum b_{i} \cdot Z^{i}$

        """
        sum_coefficient = 0.0

        for index, value in enumerate(coefficients):
            sum_coefficient += value * math.pow(atomic_number, index)

        return sum_coefficient

    def compute_C_region1(self, atomic_number):  # noqa
        if atomic_number < 6:
            ci = [-2.87536E-4, 1.808599E-3]

            c = self.compute_coefficient(atomic_number, ci)

            return c
        else:
            ci = [5.253E-3, 1.33257E-3, -7.5937E-5, 1.69357E-6, -1.3975E-8]

            c = self.compute_coefficient(atomic_number, ci)

            return c

    def compute_C_region2(self, atomic_number):  # noqa
        ci = [-9.24E-5, 1.41478E-4, -5.24999E-6, 9.85296E-8, -9.07306E-10, 3.19254E-12]

        c = self.compute_coefficient(atomic_number, ci)

        return c

    def compute_C_region3(self, atomic_number):  # noqa
        c = self.compute_C_region2(atomic_number)

        factor = 0.858

        return c * factor

    def compute_C_region4(self, atomic_number):  # noqa
        c = self.compute_C_region2(atomic_number)

        term1 = 0.8933

        term2 = -atomic_number * 8.29E-3

        term3 = atomic_number * atomic_number * 6.38E-5

        factor = term1 + term2 + term3

        return c * factor

    def compute_C_region5(self, atomic_number):  # noqa
        if atomic_number < 30:
            ci = [1.889757E-2, -1.8517159E-3, 6.9602789E-5, -1.1641145E-6, 7.2773258E-9]

            c = self.compute_coefficient(atomic_number, ci)

            return c
        else:
            ci = [3.0039E-3, -1.73663566E-4, 4.0424792E-6, -4.0585911E-8, 1.497763E-10]

            c = self.compute_coefficient(atomic_number, ci)

            return c

    def compute_C1(self, atomic_number):  # noqa
        c1i = [7.7708E-5, -7.83544E-6, 2.209365E-7, -1.29086E-9]

        c1 = self.compute_coefficient(atomic_number, c1i)

        return c1

    def compute_C2(self, atomic_number):  # noqa
        c2i = [1.406, 0.0162, -6.561E-4, 4.865E-6]

        c2 = self.compute_coefficient(atomic_number, c2i)

        return c2

    def compute_C3(self, atomic_number):  # noqa
        c3i = [0.584, 0.01955, -1.285E-4]

        c3 = self.compute_coefficient(atomic_number, c3i)

        return c3

    def compute_C4(self, atomic_number):  # noqa
        c4i = [1.082, 1.366E-3]

        c4 = self.compute_coefficient(atomic_number, c4i)

        return c4

    def compute_C5(self, atomic_number):  # noqa
        c5i = [1.6442, -0.0480, 4.0664E-4]

        c5 = self.compute_coefficient(atomic_number, c5i)

        return c5

    def compute_C_region6(self, atomic_number):  # noqa
        c1 = self.compute_C1(atomic_number)

        c2 = self.compute_C2(atomic_number)

        c3 = self.compute_C3(atomic_number)

        c = c1 * c2 * c3

        return c

    def compute_C_region7(self, atomic_number):  # noqa
        c1 = self.compute_C1(atomic_number)

        c2 = self.compute_C2(atomic_number)

        c4 = self.compute_C4(atomic_number)

        c = c1 * c2 * c4

        return c

    def compute_C_region8(self, atomic_number):  # noqa
        c1 = self.compute_C1(atomic_number)

        c2 = self.compute_C2(atomic_number)

        c = c1 * c2 * 0.95

        return c

    def compute_C_region9(self, atomic_number):  # noqa
        c1 = self.compute_C1(atomic_number)

        c2 = self.compute_C2(atomic_number)

        c5 = self.compute_C5(atomic_number)

        c = c1 * c2 * c5

        return c

    def compute_C_region10(self, atomic_number):  # noqa
        ci = [4.3156E-3, -1.4653E-4, 1.707073E-6, -6.69827E-9]

        c = self.compute_coefficient(atomic_number, ci)

        return c * 1.08

    def compute_C_region11(self, atomic_number):  # noqa
        c = self.compute_C_region10(atomic_number)

        return c

    def compute_cutoff_eV(self, atomic_number):  # noqa
        factor1 = 0.252 * atomic_number - 31.1812

        term1 = factor1 * atomic_number

        cutoff = term1 + 1042.0

        return cutoff

    def compute_n_region1(self, atomic_number):
        if atomic_number < 6:
            bi = [3.34745, 0.02652873, -0.01273815]

            b = self.compute_coefficient(atomic_number, bi)

            return b
        else:
            bi = [3.112, -0.0121]

            b = self.compute_coefficient(atomic_number, bi)

            return b

    def compute_n_region2_4(self, atomic_number):
        bi = [2.7575, 1.889E-3, -4.982E-5]

        b = self.compute_coefficient(atomic_number, bi)

        return b

    def compute_n_region5(self, atomic_number):
        bi = [0.5385, 0.084597, -1.08246E-3, 4.4509E-6]

        b = self.compute_coefficient(atomic_number, bi)

        return b

    def compute_n_region6_9(self, atomic_number):
        bi = [3.0, -0.004]

        b = self.compute_coefficient(atomic_number, bi)

        return b

    def compute_n_region10(self, atomic_number):
        bi = [0.3736, 0.02401]

        b = self.compute_coefficient(atomic_number, bi)

        return b

    def compute_n_region11(self, atomic_number):
        n = self.compute_n_region10(atomic_number)

        return n

    def compute_a_region1(self, atomic_number):
        if atomic_number < 6:
            bi = [24.4545, 155.6055, -14.15422]

            b = self.compute_coefficient(atomic_number, bi)

            return b
        else:
            bi = [0.0, 47.0, 6.52, -0.152624]

            b = self.compute_coefficient(atomic_number, bi)

            return b

    def compute_a_region2_4(self, atomic_number):
        bi = [0.0, 17.8096, 0.067429, 0.01253775, -1.16286E-4]

        b = self.compute_coefficient(atomic_number, bi)

        return b

    def compute_a_region5(self, atomic_number):
        bi = [0.0, 10.2575657, -0.822863477, 2.63199611E-2, -1.8641019E-4]

        b = self.compute_coefficient(atomic_number, bi)

        return b

    def compute_a_region6_9(self, atomic_number):
        bi = [0.0, 4.62, -0.04]

        b = self.compute_coefficient(atomic_number, bi)

        return b

    def compute_a_region10(self, atomic_number):
        bi = [0.0, 19.64, -0.61239, 5.39309E-3]

        b = self.compute_coefficient(atomic_number, bi)

        return b

    def compute_b_region1(self, atomic_number):
        if atomic_number < 6:
            bi = [-103.0, 18.2]

            b = self.compute_coefficient(atomic_number, bi)

            return b
        else:
            return 0.0

    @staticmethod
    def compute_b_region2_4(atomic_number):  # noqa
        return 0.0

    def compute_b_region5(self, atomic_number):
        if atomic_number < 61:
            bi = [0.0, 5.654, -0.536839169, 0.018972278, -1.683474E-4]

            b = self.compute_coefficient(atomic_number, bi)

            return b
        else:
            bi = [0.0, -1232.4022, 51.114164, -0.699473097, 3.1779619E-3]

            b = self.compute_coefficient(atomic_number, bi)

            return b

    def compute_b_region6_9(self, atomic_number):
        bi = [2.51, -0.052, 3.78E-4]

        b = self.compute_coefficient(atomic_number, bi)

        edge_energy_M4_eV = self.ionization_energies.ionization_energy_eV(atomic_number, 'M4')  # noqa

        return b * edge_energy_M4_eV

    def compute_b_region10(self, atomic_number):
        bi = [-113.0, 4.5]

        b = self.compute_coefficient(atomic_number, bi)

        return b
