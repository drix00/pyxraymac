#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.mac.models.test_elements
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`xray.mac.models.elements` module.
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
import unittest

# Third party modules.

# Local modules.

# Project modules.
from xray.mac.models.elements import ElementProperties, ATOMIC_NUMBER, AtomicNumberError
from xray.mac import get_current_module_path

# Globals and constants variables.


class TestElements(unittest.TestCase):
    """
    TestCase class for the module `elements`.
    """

    def setUp(self):
        """
        Setup method.
        """

        unittest.TestCase.setUp(self)

        self.properties = ElementProperties()

    def tearDown(self):
        """
        Teardown method.
        """

        unittest.TestCase.tearDown(self)

    def test_skeleton(self):
        """
        First test to check if the testcase is working with the testing framework.
        """

        # self.fail("Test if the testcase is working.")

    def test_read_data(self):
        """
        Tests for method :py:meth:`read_data`.
        """
        file_path = get_current_module_path(__file__, "../../../data/element_properties.csv")

        properties = ElementProperties()
        properties.read_data(file_path)

        self.assertEqual(106, len(properties.data[ATOMIC_NUMBER]))

    def test_get_symbol(self):
        """
        Tests for method :py:meth:`symbol`.
        """

        self.assertEqual('H', self.properties.symbol(1))
        self.assertEqual('C', self.properties.symbol(6))
        self.assertEqual('Au', self.properties.symbol(79))
        self.assertEqual('Unh', self.properties.symbol(106))

    def test_get_name(self):
        """
        Tests for method :py:meth:`symbol`.
        """

        self.assertEqual('Hydrogen', self.properties.name(1))
        self.assertEqual('Carbon', self.properties.name(6))
        self.assertEqual('Gold', self.properties.name(79))
        self.assertEqual('Unnilhexium', self.properties.name(106))

    def test_get_mass_density_g_cm3(self):
        """
        Tests for method :py:meth:`symbol`.
        """

        self.assertEqual(0.0899, self.properties.mass_density_g_cm3(1))
        self.assertEqual(2.62, self.properties.mass_density_g_cm3(6))
        self.assertEqual(19.3, self.properties.mass_density_g_cm3(79))
        self.assertRaises(AtomicNumberError, self.properties.mass_density_g_cm3, 106)

    def test_get_atomic_mass_g_mol(self):
        """
        Tests for method :py:meth:`symbol`.
        """

        self.assertEqual(1.0079, self.properties.atomic_mass_g_mol(1))
        self.assertEqual(12.011, self.properties.atomic_mass_g_mol(6))
        self.assertEqual(196.9665, self.properties.atomic_mass_g_mol(79))
        self.assertEqual(263.0, self.properties.atomic_mass_g_mol(106))

    def test_atomic_number(self):
        """
        Tests for method :py:meth:`atomic_number`.
        """

        self.assertEqual(1, self.properties.atomic_number('H'))
        self.assertEqual(6, self.properties.atomic_number('C'))
        self.assertEqual(79, self.properties.atomic_number('Au'))
        self.assertEqual(106, self.properties.atomic_number('Unh'))

# .. todo:: test get_fermi_energy_eV
# .. todo:: test get_k_fermi
# .. todo:: test get_plasmon_energy_eV
