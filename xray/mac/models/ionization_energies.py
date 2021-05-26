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

CONVERT_SUBSHELLS = {
    "K": "K",
    "K1": "K",
    "L1": "L1",
    "L2": "L2",
    "L3": "L3",
    "M1": "M1",
    "M2": "M2",
    "M3": "M3",
    "M4": "M4",
    "M5": "M5",
    "N1": "N1",
    "N2": "N2",
    "N3": "N3",
    "N4": "N4",
    "N5": "N5",
    "N6": "N6",
    "N7": "N7",
    "O1": "O1",
    "O2": "O2",
    "O3": "O3",
    "O4": "O4",
    "O5": "O5",
    "O6": "O6",
    "O7": "O7",
    "P1": "P1",
    "KI": "K",
    "LI": "L1",
    "LII": "L2",
    "LIII": "L3",
    "MI": "M1",
    "MII": "M2",
    "MIII": "M3",
    "MIV": "M4",
    "MV": "M5",
    "NI": "N1",
    "NII": "N2",
    "NIII": "N3",
    "NIV": "N4",
    "NV": "N5",
    "NVI": "N6",
    "NVII": "N7",
    "OI": "O1",
}


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
                subshell = CONVERT_SUBSHELLS[subshell]
                self.edge_energies_eV[atomic_number][subshell] = edge_energy_eV

    def ionization_energy_eV(self, atomic_number, subshell):
        if self.edge_energies_eV is None:
            self.read_edge_data()

        subshell = CONVERT_SUBSHELLS[subshell]

        return self.edge_energies_eV[atomic_number][subshell]


class IonizationEnergiesDtsa:
    def __init__(self):
        self.edge_energies_eV = None

    def read_edge_data(self, file_path=None):
        if file_path is None:
            file_path = get_current_module_path(__file__, "../../../data/dtsa/XrayDataEdge.csv")

        input_file = csv.reader(open(file_path))

        # Extract header
        row = next(input_file)

        keys = []
        for value in row:
            if value[0] == '#':
                value = value[1:]

            value = value.strip()
            value = value.replace(' ', '_')
            value = value.replace('(', '')
            value = value.replace(')', '')

            keys.append(value)

        self.edge_energies_eV = {}

        for row in input_file:
            try:
                atomic_number = int(row[0])
                edge_energies_eV = float(row[1])
                subshell = row[2]

                subshell = subshell.replace('edge', '')
                subshell = CONVERT_SUBSHELLS[subshell]

                if len(subshell) > 4:
                    print(atomic_number, subshell)

                self.edge_energies_eV.setdefault(atomic_number, {})

                self.edge_energies_eV[atomic_number].setdefault(subshell, edge_energies_eV)
            except ValueError:
                print(row)

    def ionization_energy_eV(self, atomic_number, subshell):
        if self.edge_energies_eV is None:
            self.read_edge_data()

        subshell = CONVERT_SUBSHELLS[subshell]

        energy_eV = 0.0
        if atomic_number in self.edge_energies_eV:
            if subshell in self.edge_energies_eV[atomic_number]:
                energy_eV = self.edge_energies_eV[atomic_number][subshell]

        return energy_eV
