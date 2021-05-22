#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.mac.models.test_ionization_energies
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`xray.mac.models.ionization_energies` module.
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
from xray.mac import get_current_module_path
from xray.mac.models.ionization_energies import IonizationEnergies, SUBSHELLS

# Globals and constants variables.


class TestIonizationEnergies(unittest.TestCase):
    """
    TestCase class for the module `ionization_energies`.
    """

    def setUp(self):
        """
        Setup method.
        """

        unittest.TestCase.setUp(self)

    def tearDown(self):
        """
        Teardown method.
        """

        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        """
        First test to check if the testcase is working with the testing framework.
        """

        # self.fail("Test if the testcase is working.")

    def test_read_edge_data(self):
        file_path = get_current_module_path(__file__, "../../../data/chantler2005/FFastEdgeDB.csv")

        ionization_energies = IonizationEnergies()
        self.assertEqual(None, ionization_energies.edge_energies_eV)
        ionization_energies.read_edge_data(file_path)
        self.assertEqual(92, len(ionization_energies.edge_energies_eV))
        self.assertEqual(24, len(ionization_energies.edge_energies_eV[1]))
        self.assertEqual(len(SUBSHELLS), len(ionization_energies.edge_energies_eV[1]))

        self.assertAlmostEquals(13.6, ionization_energies.edge_energies_eV[1]["K"])
        self.assertAlmostEquals(0.0, ionization_energies.edge_energies_eV[1]["L1"])
        self.assertAlmostEquals(0.0, ionization_energies.edge_energies_eV[1]["P1"])

        self.assertAlmostEquals(115606, ionization_energies.edge_energies_eV[92]["K"])
        self.assertAlmostEquals(21757.4, ionization_energies.edge_energies_eV[92]["L1"])
        self.assertAlmostEquals(32.3, ionization_energies.edge_energies_eV[92]["P1"])

    def test_ionization_energy_eV(self):
        """
        Tests for method :py:meth:`ionization_energy_eV`.
        """
        ionization_energies = IonizationEnergies()

        self.assertAlmostEquals(13.6, ionization_energies.ionization_energy_eV(1, "K"))
        self.assertAlmostEquals(0.0, ionization_energies.ionization_energy_eV(1, "L1"))
        self.assertAlmostEquals(0.0, ionization_energies.ionization_energy_eV(1, "P1"))

        self.assertAlmostEquals(115606, ionization_energies.ionization_energy_eV(92, "K"))
        self.assertAlmostEquals(21757.4, ionization_energies.ionization_energy_eV(92, "L1"))
        self.assertAlmostEquals(32.3, ionization_energies.ionization_energy_eV(92, "P1"))

    def test_default_data_files(self):
        ionization_energies = IonizationEnergies()
        self.assertEqual(None, ionization_energies.edge_energies_eV)

        self.assertAlmostEquals(13.6, ionization_energies.ionization_energy_eV(1, "K"))
        self.assertAlmostEquals(0.0, ionization_energies.ionization_energy_eV(1, "L1"))
        self.assertAlmostEquals(0.0, ionization_energies.ionization_energy_eV(1, "P1"))

        self.assertAlmostEquals(115606, ionization_energies.ionization_energy_eV(92, "K"))
        self.assertAlmostEquals(21757.4, ionization_energies.ionization_energy_eV(92, "L1"))
        self.assertAlmostEquals(32.3, ionization_energies.ionization_energy_eV(92, "P1"))
