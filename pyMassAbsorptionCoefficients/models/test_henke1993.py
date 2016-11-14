#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2007 Hendrix Demers"
__license__ = ""

# Standard library modules.
import os.path
import unittest

import pyHendrixDemersTools.Files as Files
import pyMassAbsorptionCoefficients.models.henke1993 as MacHenke1993
from nose import SkipTest


# Globals and constants variables.

class TestMacHenke1993(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        configurationFile = Files.getCurrentModulePath(__file__, "../testdata/Databases.cfg")
        if not os.path.isfile(configurationFile):
            raise SkipTest

        self.mac = MacHenke1993.MacHenke1993(configurationFile)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testConstructor(self):
        configurationFile = Files.getCurrentModulePath(__file__, "../testdata/Databases.cfg")

        mac = MacHenke1993.MacHenke1993(configurationFile)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testComputeMac_cm2_g(self):
        mac_cm2_g = self.mac.computeMac_cm2_g(10.2, 28)

        self.assertAlmostEquals((9.709), mac_cm2_g*1.0E-4, 2)

        mac_cm2_g = self.mac.computeMac_cm2_g(1486.7, 28)

        self.assertAlmostEquals((4.285), mac_cm2_g*1.0E-3, 2)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testCopperMEdges(self):
        mac1_cm2_g = self.mac.computeMac_cm2_g(130.0, 29)

        mac2_cm2_g = self.mac.computeMac_cm2_g(115.0, 29)

        mac3_cm2_g = self.mac.computeMac_cm2_g(50.0, 29)

        # Normal behavior if the M edge is present in the data.
        # For Henke data, the M edge is not present.
        #self.assertTrue(mac1_cm2_g > mac2_cm2_g)
        #self.assertTrue(mac2_cm2_g > mac3_cm2_g)
        #self.assertTrue(mac1_cm2_g > mac3_cm2_g)

        self.assertAlmostEquals((5.839230), mac1_cm2_g*1.0E-4, 2)

        self.assertAlmostEquals((6.1090), mac2_cm2_g*1.0E-4, 2)

        self.assertAlmostEquals((7.58129), mac3_cm2_g*1.0E-4, 2)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

if __name__ == '__main__':    #pragma: no cover
    import nose
    nose.runmodule()
