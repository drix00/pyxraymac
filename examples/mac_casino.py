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

# Third party modules.
import numpy as np

# Local modules.

# Project modules.

# Globals and constants variables.
from xray_mac.mac.models.casino import efficiency, mac_zaluzec_cm2_g, macs_heinrich, macs_henke_ebisu, macs_total


if __name__ == '__main__':  # pragma: no cover
    import matplotlib.pyplot as plt

    energies_keV = np.linspace(0.001, 30.0, 500)

    plt.figure()
    efficiencies = [efficiency(energy_keV) for energy_keV in energies_keV]
    plt.plot(energies_keV, efficiencies)
    plt.close()

    energies_keV = np.linspace(0.1, 30.0, 500)
    plt.figure()
    for atomic_number in [1, 6, 8, 13, 14, 79]:
        macs_cm2_g = [mac_zaluzec_cm2_g(12.3981 / energy_keV, atomic_number) for energy_keV in energies_keV]
        plt.semilogy(energies_keV, macs_cm2_g, label=atomic_number)
    plt.legend()
    plt.close()

    energies_keV = np.linspace(0.01, 2.0, 100)
    plt.figure()
    atomic_number = 6
    macs_cm2_g = [mac_zaluzec_cm2_g(12.3981 / energy_keV, atomic_number) for energy_keV in energies_keV]
    plt.semilogy(energies_keV, macs_cm2_g, label="Zaluzec")
    macs_cm2_g = [macs_heinrich(12.3981 / energy_keV, atomic_number) for energy_keV in energies_keV]
    plt.semilogy(energies_keV, macs_cm2_g, label="Heinrich")
    macs_cm2_g = [macs_henke_ebisu(energy_keV, atomic_number) for energy_keV in energies_keV]
    plt.semilogy(energies_keV, macs_cm2_g, label="Henke")
    macs_cm2_g = [macs_total(energy_keV, atomic_number) for energy_keV in energies_keV]
    plt.semilogy(energies_keV, macs_cm2_g, '.', label="Total")

    plt.legend()

    plt.show()
