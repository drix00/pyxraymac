#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: xray_mac.mac.models.penelope
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

PENELOPE MAC model.

mu = sigma * n
mu in 1/m
sigma cross section in barn
n number of atoms par volume
n = N_A * rho / M
M molar mass kg/mol

mu / rho = sigma N_A / M
mu / rho in cm2/g
N_A = 6.02214076e23 1/mol

barn = 10−28 m2

factor_cm2_g = 10-24 * 6.02214076e23 / M
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
import zipfile

# Third party modules.

# Local modules.

# Project modules.
from xray_mac.mac.models.elements import ElementProperties

# Globals and constants variables.
import numpy as np

SHELL_NAMES = {
    1: "K",
    2: "L1",
    3: "L2",
    4: "L3",
    5: "M1",
    6: "M2",
    7: "M3",
    8: "M4",
    9: "M5",
    10: "N1",
    11: "N2",
    12: "N3",
    13: "N4",
    14: "N5",
    15: "N6",
    16: "N7",
    17: "O1",
    18: "O2",
    19: "O3",
    20: "O4",
    21: "O5",
    22: "O6",
    23: "O7",
    24: "P1",
    25: "P2",
    26: "P3",
    27: "P4",
    28: "P5",
    29: "Q1",
    30: "outer shells",
}


class PhotoElectric:
    def __init__(self):
        self.atomic_number = 0
        self.number_shells = 0
        self.number_grid_energies = 0
        self.shell_ids = []
        self.ionization_energies_eV = []

        self.energies_eV = []
        self.totals_barn = []
        self.partials_barn = []

        self.element_properties = ElementProperties()
        self.element_properties.read_data()

    def read_data(self, data_file_path, atomic_number, with_normalization=True):
        file_path = "pendbase/pdfiles/pdgph{:02d}.p18".format(int(atomic_number))
        with zipfile.ZipFile(data_file_path, "r") as zip_file:
            if with_normalization:
               data = zip_file.read(file_path)
            else:
                with zip_file.open("pendbase/pdfiles/pdgph-photacs.zip") as data_zip:
                    with zipfile.ZipFile(data_zip, "r") as zip_file2:
                        file_path = "pdgph-photacs/pdgph{:02d}.p18".format(int(atomic_number))
                        data = zip_file2.read(file_path)

            lines = data.decode("UTF-8")
            lines = lines.split("\r\n")

            row_id = 0
            for line in lines:
                if line.startswith("# IZ, NS, NGE:"):
                    items = line.split(":")[-1]
                    z, ns, nge = items.split()
                    self.atomic_number = int(z)
                    self.number_shells = int(ns)
                    self.number_grid_energies = int(nge)
                    self.energies_eV = np.zeros(self.number_grid_energies)
                    self.totals_barn = np.zeros(self.number_grid_energies)
                    self.partials_barn = np.zeros((self.number_grid_energies, self.number_shells))
                elif line.startswith("# Shell:"):
                    items = line.split(":")[-1]
                    shell_ids = [int(shell_id) for shell_id in items.split()]
                    self.shell_ids = shell_ids
                elif line.startswith("# Eion (eV)"):
                    ionization_energies_eV = [float(energy_eV) for energy_eV in line.split()[3:]]
                    self.ionization_energies_eV = ionization_energies_eV
                else:
                    items = line.split()
                    if len(items) > 2:
                        self.energies_eV[row_id] = float(items[0])
                        self.totals_barn[row_id] = float(items[1])
                        self.partials_barn[row_id] = [float(item) for item in items[2:]]
                        row_id += 1

    @property
    def totals_cm2_g(self):
        molar_mass_g_mol = self.element_properties.atomic_mass_g_mol(self.atomic_number)
        factor_cm2_g = 1e-24 * 6.02214076e23 / molar_mass_g_mol
        totals_cm2_g = self.totals_barn * factor_cm2_g
        return totals_cm2_g

    @property
    def partials_cm2_g(self):
        molar_mass_g_mol = self.element_properties.atomic_mass_g_mol(self.atomic_number)
        factor_cm2_g = 1e-24 * 6.02214076e23 / molar_mass_g_mol
        partials_cm2_g = self.partials_barn * factor_cm2_g
        return partials_cm2_g


def list_files(data_file_path):
    with zipfile.ZipFile(data_file_path, "r") as zip_file:
        file_names = zip_file.namelist()

    return file_names
