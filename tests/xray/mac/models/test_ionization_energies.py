#!/usr/bin/env python
"""
.. py:currentmodule:: test_ionization_energies
   :synopsis: Tests for the module :py:mod:`ionization_energies`
   
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the module :py:mod:`ionization_energies`.
"""

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = "0.1"
__date__ = "2016-10-27"
__copyright__ = "Copyright (c) 2016 Hendrix Demers"
__license__ = "Apache License Version 2.0"

# Standard library modules.
import unittest

# Third party modules.

# Local modules.

# Project modules
from xray import get_current_module_path
from xray.mac.models.ionization_energies import IonizationEnergies, SUBSHELLS

# Globals and constants variables.

class Test_ionization_energies(unittest.TestCase):
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

        #self.fail("Test if the testcase is working.")

    def test_read_edge_data(self):
        file_path = get_current_module_path(__file__, "../../../../data/chantler2005/FFastEdgeDB.csv")

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

        #self.fail("Test if the testcase is working.")

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

        #self.fail("Test if the testcase is working.")

    def test_default_data_files(self):
        ionization_energies = IonizationEnergies()
        self.assertEqual(None, ionization_energies.edge_energies_eV)

        self.assertAlmostEquals(13.6, ionization_energies.ionization_energy_eV(1, "K"))
        self.assertAlmostEquals(0.0, ionization_energies.ionization_energy_eV(1, "L1"))
        self.assertAlmostEquals(0.0, ionization_energies.ionization_energy_eV(1, "P1"))

        self.assertAlmostEquals(115606, ionization_energies.ionization_energy_eV(92, "K"))
        self.assertAlmostEquals(21757.4, ionization_energies.ionization_energy_eV(92, "L1"))
        self.assertAlmostEquals(32.3, ionization_energies.ionization_energy_eV(92, "P1"))

        #self.fail("Test if the testcase is working.")


if __name__ == '__main__':  #pragma: no cover
    import nose
    nose.runmodule()
    