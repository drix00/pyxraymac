#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: xray.mac.models.henke
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

MAC Henke model.
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
import tarfile
import os.path
import math

# Third party modules.

# Local modules.

# Project modules.
from xray.mac.models.elements import ElementProperties
from xray.mac import create_root_path

# Globals and constants variables.
g_coefficient = [41746.75,
                 10512.72,
                 6062.27,
                 4669.04,
                 3892.17,
                 3503.31,
                 3004.14,
                 2629.99,
                 2214.83,
                 2085.18,
                 1830.3,
                 1731.26,
                 1559.52,
                 1498.22,
                 1358.51,
                 1312.24,
                 1186.88,
                 1053.32,
                 1076.22,
                 1049.91,
                 935.99,
                 878.83,
                 826.01,
                 809.26,
                 765.92,
                 753.46,
                 714,
                 716.92,
                 662.17,
                 643.5,
                 603.51,
                 579.51,
                 561.63,
                 532.91,
                 526.61,
                 502.13,
                 492.33,
                 480.24,
                 473.29,
                 461.26,
                 452.91,
                 438.59,
                 425.44,
                 416.33,
                 408.9,
                 395.4,
                 390.09,
                 374.32,
                 366.47,
                 354.46,
                 345.59,
                 329.77,
                 331.57,
                 320.5,
                 316.6,
                 306.41,
                 302.93,
                 300.31,
                 298.62,
                 291.72,
                 286.4,
                 279.85,
                 276.89,
                 267.59,
                 264.77,
                 258.94,
                 255.13,
                 251.57,
                 249.08,
                 243.17,
                 240.49,
                 235.75,
                 232.54,
                 228.87,
                 225.98,
                 221.23,
                 218.91,
                 215.7,
                 213.63,
                 209.77,
                 205.88,
                 203.08,
                 201.35,
                 200.39,
                 200.38,
                 189.52,
                 188.67,
                 186.16,
                 185.35,
                 181.34,
                 182.13,
                 176.78]


def get_coefficient(atomic_number):
    index = atomic_number - 1

    return g_coefficient[index]


def wavelength_electron_nm(energy_eV):  # noqa
    h_Nms = 6.626E-34  # noqa
    m0_kg = 9.109E-31
    e_C = 1.602E-19  # noqa

    arg_sqrt = 2.0 * m0_kg * e_C * energy_eV

    value_m = h_Nms / math.sqrt(arg_sqrt)

    value_nm = value_m * 1.0E9

    return value_nm


def wavelength_electron_relativistic_nm(energy_eV):  # noqa
    h_Nms = 6.626E-34  # noqa
    m0_kg = 9.109E-31
    e_C = 1.602E-19  # noqa
    c_m_s = 2.998E8

    factor = 2.0 * m0_kg * e_C * energy_eV

    ratio = e_C * energy_eV / (2.0 * m0_kg * c_m_s ** 2)

    term = 1.0 + ratio

    arg_sqrt = factor * term

    value_m = h_Nms / math.sqrt(arg_sqrt)

    value_nm = value_m * 1.0E9

    return value_nm


def wavelength_photon_nm(energy_eV):  # noqa
    h_Nms = 6.626E-34  # noqa
    c_m_s = 2.998E8
    e_C = 1.602E-19  # noqa

    value_m = h_Nms * c_m_s / (e_C * energy_eV)

    value_nm = value_m * 1.0E9

    return value_nm


class MacHenke(object):
    def __init__(self, data_path):
        self.data_path = data_path

        self._filename = "sf.tar.gz"

    def compute_coefficient_keVcm2_g(self, atomic_number):  # noqa
        r0_m = 2.817938e-15
        h_Js = 6.62618E-34  # noqa
        c_m_s = 2.99792458E8

        C_1_Jm2 = 1.0 / (math.pi * r0_m * h_Js * c_m_s)  # noqa

        J_eV = 1.602189E-19  # noqa

        N0_atom_mol = 6.02205E23  # noqa

        element_properties = ElementProperties()
        A_g_mol = element_properties.atomic_mass_g_mol(atomic_number)  # noqa

        K_atomJm2_g = 2.0 * N0_atom_mol / (math.pi * C_1_Jm2 * A_g_mol)  # noqa

        K_keVcm2_g = K_atomJm2_g / (J_eV * 1.0E3 * 1.0E-4)  # noqa

        return K_keVcm2_g

    def get_elements(self):
        elements = []

        gz_filename = os.path.join(self.data_path, self._filename)

        tar_file = tarfile.TarFile.gzopen(gz_filename, mode='r')

        files = tar_file.getnames()

        for file in files:
            if '.nff' in file:
                element = os.path.splitext(os.path.basename(file))[0]
                elements.append(element)

        return elements

    def read_data(self, atomic_number):
        gz_filename = os.path.join(self.data_path, self._filename)

        tar_file = tarfile.TarFile.gzopen(gz_filename, mode='r')

        files = tar_file.getnames()

        element_properties = ElementProperties()
        symbol = element_properties.symbol(atomic_number).lower()

        filename = symbol + '.nff'

        energies_eV = []  # noqa
        macs_cm2_g = []

        if filename in files:
            lines = tar_file.extractfile(filename).readlines()

            f1s = []
            f2s = []

            for line in lines[1:]:
                values = line.split(b'\t')

                energy_eV = float(values[0])  # noqa

                energies_eV.append(energy_eV)

                f1s.append(float(values[1]))

                f2 = float(values[2])

                f2s.append(f2)

                mac_cm2_g = self.compute_mac_cm2_g(atomic_number, energy_eV, f2)

                macs_cm2_g.append(mac_cm2_g)

        tar_file.close()

        return energies_eV, macs_cm2_g

    def write_mac(self, results_path):
        create_root_path(results_path)

        elements = self.get_elements()

        for element in elements:

            element_properties = ElementProperties()
            atomic_number = element_properties.atomic_number(element)

            energies_eV, macs_cm2_g = self.read_data(atomic_number)  # noqa

            assert len(energies_eV) == len(macs_cm2_g)

            filename = str(element) + ".dat"
            filename = os.path.join(results_path, filename)

            mac_file = open(filename, 'w')

            for index in range(len(energies_eV)):
                line = str(energies_eV[index]) + "\t" + str(macs_cm2_g[index]) + "\n"
                mac_file.write(line)

            mac_file.close()

    def compute_mac_cm2_g(self, atomic_number, energy_eV, f2):  # noqa

        factor = self.compute_coefficient_keVcm2_g(atomic_number) / 1.0E-3

        mac_cm2_g = f2 * factor / energy_eV

        return mac_cm2_g
