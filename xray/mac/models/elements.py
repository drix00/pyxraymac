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
import csv
import logging

# Third party modules.

# Local modules.

# Project modules.
from xray.mac import get_current_module_path

# Globals and constants variables.
ATOMIC_NUMBER = "atomic number"
SYMBOL = "symbol"
NAME = "name"
MASS_DENSITY_g_cm3 = "mass density (g/cm3)"
ATOMIC_MASS_g_mol = "atomic mass (g/mol)"
FERMI_ENERGY_eV = "Fermi energy (eV)"
K_FERMI = "k Fermi (eV)"
PLASMON_ENERGY_eV = "plasmon energy (eV)"


class AtomicNumberError(KeyError):
    pass


class SymbolError(KeyError):
    pass


class ElementProperties():
    def __init__(self):
        self.data = None

    def read_data(self, file_path=None):
        if file_path is None:
            file_path = get_current_module_path(__file__, "../../../data/element_properties.csv")

        fieldnames = [ATOMIC_NUMBER, SYMBOL, NAME, MASS_DENSITY_g_cm3, ATOMIC_MASS_g_mol, FERMI_ENERGY_eV, K_FERMI,
                      PLASMON_ENERGY_eV]
        input_file = csv.DictReader(open(file_path), fieldnames=fieldnames)

        # Read the header row.
        next(input_file)

        self.data = {}
        for field_name in fieldnames:
            self.data[field_name] = {}

        for items in input_file:
            atomic_number = int(items[ATOMIC_NUMBER])
            for field_name, value in items.items():
                if value != "":
                    self.data[field_name][atomic_number] = value

    def symbol(self, atomic_number):
        if self.data is None:
            self.read_data()

        try:
            value = str(self.data[SYMBOL][atomic_number])
        except KeyError as message:
            logging.error("%s for %i", message, atomic_number)
            raise AtomicNumberError("No data for atomic number %i." % (atomic_number))

        return value

    def name(self, atomic_number):
        if self.data is None:
            self.read_data()

        try:
            value =  str(self.data[NAME][atomic_number])
        except KeyError as message:
            logging.error("%s for %i", message, atomic_number)
            raise AtomicNumberError("No data for atomic number %i." % (atomic_number))

        return value

    def mass_density_g_cm3(self, atomic_number):
        if self.data is None:
            self.read_data()

        try:
            value = float(self.data[MASS_DENSITY_g_cm3][atomic_number])
        except KeyError as message:
            logging.error("%s for %i", message, atomic_number)
            raise AtomicNumberError("No data for atomic number %i." % (atomic_number))

        return value

    def atomic_mass_g_mol(self, atomic_number):
        if self.data is None:
            self.read_data()

        try:
            value = float(self.data[ATOMIC_MASS_g_mol][atomic_number])
        except KeyError as message:
            logging.error("%s for %i", message, atomic_number)
            raise AtomicNumberError("No data for atomic number %i." % (atomic_number))

        return value

    def atomic_number(self, symbol):
        if self.data is None:
            self.read_data()

        for temp_atomic_number, temp_symbol in self.data[SYMBOL].items():
            if symbol == temp_symbol:
                return temp_atomic_number

        message = "No atomic number for symbol %s" % (symbol)
        logging.error(message)
        raise SymbolError(message)
