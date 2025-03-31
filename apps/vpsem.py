#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: vpsem
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Script to compute absorption of x-ray by the gas in a VP-SEM.
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
import numpy as np

# Local modules.

# Project modules.
from xray_mac.mac.models.chantler2005 import Chantler2005

# Globals and constants variables.


def run_water():
    density_g_cm3 = 1.0e-5
    length_mm = 10.0
    length_cm = length_mm*1.0e-1

    cu_ka_eV = 8046.0
    cu_la_eV = 930.0

    chantler2005 = Chantler2005()

    for energy_eV in [cu_ka_eV, cu_la_eV]:
        total_mac_cm2_g = 0.0
        for atomic_number, weight_fraction in [(1, 0.111894), (8, 0.888106)]:
            atomic_number = 1
            mac_cm2_g = chantler2005.compute_mac_cm2_g(energy_eV, atomic_number)
            total_mac_cm2_g += mac_cm2_g*weight_fraction

        absorption = np.exp(-total_mac_cm2_g*density_g_cm3*length_cm)
        print(energy_eV, total_mac_cm2_g,absorption)


if __name__ == '__main__':
    run_water()
