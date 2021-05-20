#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2007 Hendrix Demers"
__license__ = ""

# Standard library modules.
import unittest

# Third party modules.

# Local modules.
import xray.mac.models.MacHenkeWinxray as MacHenkeWinxray
import pyHendrixDemersTools.Files as Files

# Globals and constants variables.

class TestMacHenkeWinxray(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        configurationFile = Files.getCurrentModulePath(__file__, "../MassAbsorptionCoefficient.cfg")

        self.macData = MacHenkeWinxray.MacHenkeWinxray(configurationFile)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testConstructor(self):
        configurationFile = Files.getCurrentModulePath(__file__, "../MassAbsorptionCoefficient.cfg")

        macData = MacHenkeWinxray.MacHenkeWinxray(configurationFile)

        self.assertTrue(macData.pathnameBinary != "")

        self.assertTrue(macData.pathnameText != "")

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testReadTextData(self):
        enegies_eV, mac_cm2_g = self.macData.readTextData(28)

        self.assertEquals(500, len(enegies_eV))

        self.assertEquals(500, len(mac_cm2_g))

        self.assertEquals(10.0, enegies_eV[0])

        self.assertEquals(98739.2, mac_cm2_g[0])

        self.assertEquals(30000.0, enegies_eV[-1])

        self.assertEquals(9.77398, mac_cm2_g[-1])

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testReadBinaryData(self):
        enegies_eV, mac_cm2_g = self.macData.readBinaryData(28)

        self.assertEquals(500, len(enegies_eV))

        self.assertEquals(500, len(mac_cm2_g))

        self.assertAlmostEquals(10.0, enegies_eV[0], 1)

        self.assertAlmostEquals(98739.2, mac_cm2_g[0], 1)

        self.assertAlmostEquals(30000.0, enegies_eV[-1], 1)

        self.assertAlmostEquals(9.77398, mac_cm2_g[-1], 1)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
