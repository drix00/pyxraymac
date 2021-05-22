#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: xray.mac.models.ionization_energy
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Container of ionization energy for each atomic number and subshell.
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
import csv

# Third party modules.

# Local modules.

# Project modules.
from xray.mac import get_current_module_path

# Globals and constants variables.
SUBSHELLS = ["K",
             "L1", "L2", "L3",
             "M1", "M2", "M3", "M4", "M5",
             "N1", "N2", "N3", "N4", "N5", "N6", "N7",
             "O1", "O2", "O3", "O4", "O5", "O6", "O7",
             "P1"]


class IonizationEnergies:
    def __init__(self):
        self.edge_energies_eV = None

    def read_edge_data(self, file_path=None):
        if file_path is None:
            file_path = get_current_module_path(__file__, "../../../data/chantler2005/FFastEdgeDB.csv")

        input_file = csv.reader(open(file_path))

        self.edge_energies_eV = {}
        atomic_number = 0
        for items in input_file:
            atomic_number += 1
            edge_energies_eV = [float(item) for item in items]
            self.edge_energies_eV[atomic_number] = {}
            for subshell, edge_energy_eV in zip(SUBSHELLS, edge_energies_eV):
                self.edge_energies_eV[atomic_number][subshell] = edge_energy_eV

    def ionization_energy_eV(self, atomic_number, subshell):
        if self.edge_energies_eV is None:
            self.read_edge_data()

        return self.edge_energies_eV[atomic_number][subshell]
