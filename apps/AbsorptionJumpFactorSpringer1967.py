#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: AbsorptionJumpFactorSpringer1967
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Compute the absorption jump factor from the model of Springer (1967).
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

# Third party modules.

# Local modules.

# Project modules.

# Globals and constants variables.


class AbsorptionJumpFactorSpringer1967(object):
    """
    Compute the absorption jump factor from the model of Springer (1967).

    Reference: springer1967
        Sagel K. (1959): Tabellen zur Rontgenemissions- und -absorptionsanalyse
        (Berlin-Gottingen-Heidelberg: Springer).


    Fit of the values from Sagel (1959) for the K and L3 subshell only.


    """
    def get_factor(self, atomic_number, line, xray_energy_eV=None):
        if line == 'Ka':
            factor = self.compute_factor_K(atomic_number)

            return factor

        if line == 'La':
            factor = self.compute_factor_LIII(atomic_number)

            return factor

    def compute_factor_K(self, atomic_number):
        """
        Compute the absorption jump factor for the K subshell

        \f[
            \frac{r_{K} - 1}{r_{K}} = 0.924 -0.00144 \cdot Z
        \f]

        Mandatory arguments:


        Optional arguments:


        Extra arguments:


        Return parameters:

        """
        factor = 0.924 - 0.00144 * atomic_number

        return factor

    def compute_factor_LIII(self, atomic_number):
        """
        Compute the absorption jump factor for the L3 subshell

        \f[
            \frac{r_{L_{III}} - 1}{r_{L_{III}} \cdot r_{L_{II}} \cdot r_{L_{I}}} = 0.548 - 0.00231 \cdot Z
        \f]

        Mandatory arguments:


        Optional arguments:


        Extra arguments:


        Return parameters:

        """
        factor = 0.548 - 0.00231 * atomic_number

        return factor
