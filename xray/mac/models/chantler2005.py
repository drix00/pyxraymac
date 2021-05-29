#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: xray.mac.models.chantler2005
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Chantler 2005 MAC model.
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
import logging

# Third party modules.
from scipy.interpolate import interp1d

# Local modules.
from xray.mac import get_current_module_path

# Globals and constants variables.
SECTION_NAME = "Chantler2005"
OPTION_PATHNAME = "pathname"
OPTION_FILENAME = "filename"
OPTION_ENERGY_UNIT = "energyUnit"

ENERGIES_eV = "energies_eV"
MAC_cm2_g = "mac_cm2_g"

ENERGY_UNIT_eV = "eV"
ENERGY_UNIT_keV = "keV"


class Chantler2005():
    def __init__(self):
        self.minimum_energy_eV = 0.0
        self.minimum_mac_cm2_g = 0.0

        self.mac_data = {}
        self.edge_energies_eV = {}

        self.experimental_data = {}

    def read_mac_data(self, file_path=None, energy_unit=ENERGY_UNIT_keV):
        if file_path is None:
            file_path = get_current_module_path(__file__, "../../../data/chantler2005/FFastMAC.csv")
        self.reset_data()
        input_file = csv.reader(open(file_path))

        for items in input_file:
            self.extract_data_from_items_line(items, energy_unit)

    def reset_data(self):
        self.experimental_data = {}

    def extract_data_from_items_line(self, items, energy_unit):
        index = 0
        maximum_index = len(items)
        atomic_number = 1

        while index < maximum_index:
            try:
                if items[index] != '':
                    if energy_unit == ENERGY_UNIT_keV:
                        energy_keV = float(items[index])
                        energy_eV = energy_keV*1.0e3
                    else:
                        energy_eV = float(items[index])

                    mac_cm2_g = float(items[index+1])

                    if energy_eV > 0.0:
                        self.experimental_data.setdefault(atomic_number, {})
                        self.experimental_data[atomic_number].setdefault(ENERGIES_eV, []).append(energy_eV)
                        self.experimental_data[atomic_number].setdefault(MAC_cm2_g, []).append(mac_cm2_g)
            except ValueError as status:
                logging.error(status)
                logging.info(items)

            atomic_number += 1
            index += 2

    def compute_mac_cm2_g(self, energy_emitter_eV, atomic_number_absorber):
        return self._compute_mac_cm2_g(energy_emitter_eV, atomic_number_absorber)

    def _compute_mac_cm2_g(self, energyEmitter_eV, atomic_number_absorber):
        if atomic_number_absorber not in self.mac_data:
            self.read_mac_data()

            energies_eV = self.experimental_data[atomic_number_absorber][ENERGIES_eV]
            macs_cm2_g = self.experimental_data[atomic_number_absorber][MAC_cm2_g]

            if len(energies_eV) > 0:
                self.mac_data.setdefault(atomic_number_absorber, {})

                self.minimum_energy_eV = energies_eV[0]

                self.minimum_mac_cm2_g = macs_cm2_g[0]

                self.maximum_energy_eV = energies_eV[-1]

                self.maximum_mac_cm2_g = macs_cm2_g[-1]

                self.mac_data[atomic_number_absorber] = interp1d(energies_eV, macs_cm2_g)

            else:
                logging.error("No mac for %i and %0.1f", atomic_number_absorber, energyEmitter_eV)
                return 0.0

        if energyEmitter_eV <= self.minimum_energy_eV:
            return self.minimum_mac_cm2_g

        if energyEmitter_eV >= self.maximum_energy_eV:
            return self.maximum_mac_cm2_g

        if atomic_number_absorber in self.mac_data:
            try:
                mac_value = self.mac_data[atomic_number_absorber](energyEmitter_eV)
            except ValueError:
                print(atomic_number_absorber, energyEmitter_eV)
                mac_value = self.minimum_mac_cm2_g
            return mac_value
        else:
            logging.error("No mac for %i and %0.1f", atomic_number_absorber, energyEmitter_eV)
            return 0.0


def compare_all_versions():
    import matplotlib.pyplot as plt
    from xray.mac.models.ionization_energies import IonizationEnergies, SUBSHELLS

    mac = Chantler2005()

    atomic_numbers = [1, 6, 22, 92]
    filenames = {"Default": "FFastMAC.csv", "NISTMonte2": "FFastMAC_nistMonte2.csv", "DTSA2": "FFastMAC_DTSA2.csv"}

    for atomic_number in atomic_numbers:
        plt.figure()
        for filename_key in filenames:
            filename = filenames[filename_key]

            if filename_key == "NISTMonte2":
                file_path = get_current_module_path(__file__, "../../data/chantler2005/%s" % (filename))
                mac.read_mac_data(file_path, ENERGY_UNIT_eV)
            else:
                file_path = get_current_module_path(__file__, "../../data/chantler2005/%s" % (filename))
                mac.read_mac_data(file_path)

            energies_eV = mac.experimental_data[atomic_number][ENERGIES_eV]
            mac_cm2_g = mac.experimental_data[atomic_number][MAC_cm2_g]

            if filename_key == "Default":
                plt.loglog(energies_eV, mac_cm2_g, '.', label=filename_key)
            else:
                plt.loglog(energies_eV, mac_cm2_g, label=filename_key)

        plt.legend()
        plt.title(atomic_number)

        ionization_energies = IonizationEnergies()

        for subshell in SUBSHELLS:
            edge_energy_eV = ionization_energies.ionization_energy_eV(atomic_number, subshell)
            if edge_energy_eV > 0.0:
                plt.axvline(edge_energy_eV, zorder=-10)
    plt.show()


def create_hdf5_file():
    import h5py
    import numpy as np

    filename = "chantler2005.hdf5"
    file_path = get_current_module_path(__file__, "../../data/chantler2005/%s" % filename)

    with h5py.File(file_path, "w") as hdf5_file:
        mac = Chantler2005()
        mac.read_mac_data()

        group_elements = hdf5_file.require_group("elements")

        for atomic_number in sorted(mac.experimental_data.keys()):
            group_name = "{:02d}".format(atomic_number)
            group_atomic_number = group_elements.require_group(group_name)
            energies_eV = np.array(mac.experimental_data[atomic_number][ENERGIES_eV])
            macs_cm2_g = np.array(mac.experimental_data[atomic_number][MAC_cm2_g])

            group_atomic_number.create_dataset(ENERGIES_eV, data=energies_eV)
            group_atomic_number.create_dataset(MAC_cm2_g, data=macs_cm2_g)
