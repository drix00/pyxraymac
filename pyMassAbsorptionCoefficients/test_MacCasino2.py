#!/usr/bin/env python
"""
.. py:currentmodule:: test_MacCasino2
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for module `MacCasino2`.
"""

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2012 Hendrix Demers"
__license__ = ""

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.

# Project modules
import MacCasino2

# Globals and constants variables.

class TestMacCasino2(unittest.TestCase):
    """
    TestCase class for the module `MacCasino2`.
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
        self.assert_(True)

    def test_MACS_ZALUZEC(self):
        """
        Tests for method `MACS_ZALUZEC`.
        """



        #self.fail("Test if the testcase is working.")

    def test_SPECIAL_EQUATIONS(self):
        """
        Tests for method `SPECIAL_EQUATIONS`.
        """



        #self.fail("Test if the testcase is working.")

    def test_MACS_HENKE_EBISU(self):
        """
        Tests for method `MACS_HENKE_EBISU`.
        """



        #self.fail("Test if the testcase is working.")

    def test_MACSTOTAL(self):
        """
        Tests for method `MACSTOTAL`.
        """

        mac_g_cm3 = MacCasino2.MACSTOTAL(0.0, 1)
        self.assertAlmostEquals(0.0, mac_g_cm3)

        mac_g_cm3 = MacCasino2.MACSTOTAL(0.0, 2)
        self.assertAlmostEquals(-1, mac_g_cm3)

        #self.fail("Test if the testcase is working.")

    def test_MACS_HEINRICH(self):
        """
        Tests for method `MACS_HEINRICH`.
        """



        #self.fail("Test if the testcase is working.")

    def test_EFFICACITE(self):
        """
        Tests for method `EFFICACITE`.
        """



        #self.fail("Test if the testcase is working.")

if __name__ == '__main__':  #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    from DrixUtilities.Testings import runTestModuleWithCoverage
    runTestModuleWithCoverage(__file__)
