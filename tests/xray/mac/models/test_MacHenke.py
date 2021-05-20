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
import xray.mac.models.MacHenke as MacHenke
import pyHendrixDemersTools.Files as Files

# Globals and constants variables.

class TestMacHenke(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        configurationFile = Files.getCurrentModulePath(__file__, "../MassAbsorptionCoefficient.cfg")

        self.macData = MacHenke.MacHenke(configurationFile)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testConstructor(self):
        configurationFile = Files.getCurrentModulePath(__file__, "../MassAbsorptionCoefficient.cfg")

        macData = MacHenke.MacHenke(configurationFile)

        self.assertTrue(macData._pathname != "")

        self.assertEquals("sf.tar.gz", macData._filename)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testReadData(self):
        enegies_eV, macs_cm2_g = self.macData.readData(28)

        self.assertAlmostEquals(10.0, enegies_eV[0])

        self.assertAlmostEquals(30000.0, enegies_eV[-1])

        self.assertAlmostEquals((9.87), macs_cm2_g[0]*1.0E-4, 2)

        self.assertAlmostEquals((9.77), macs_cm2_g[-1], 2)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testWavelenght(self):
        wavelengthsElectronNonRelativisticWilliams1996_nm = {100.0E3: 0.00386
                                                                                                 , 120.0E3: 0.00352
                                                                                                 , 200.0E3: 0.00273
                                                                                                 , 300.0E3: 0.00223
                                                                                                 , 400.0E3: 0.00193
                                                                                                 , 1000.0E3: 0.00122}

        wavelengthsElectronRelativisticWilliams1996_nm = {100.0E3: 0.00370
                                                                                                 , 120.0E3: 0.00335
                                                                                                 , 200.0E3: 0.00251
                                                                                                 , 300.0E3: 0.00197
                                                                                                 , 400.0E3: 0.00164
                                                                                                 , 1000.0E3: 0.00087}

        wavelengthsPhoton_A = {10.2: 1215.6, 91.5: 135.5, 14988.0: 0.8}

        for energy_eV in wavelengthsElectronNonRelativisticWilliams1996_nm:
            self.assertAlmostEquals(wavelengthsElectronNonRelativisticWilliams1996_nm[energy_eV], MacHenke.WavelenghtElectron_nm(energy_eV), 4)

            self.assertAlmostEquals(wavelengthsElectronRelativisticWilliams1996_nm[energy_eV], MacHenke.WavelenghtElectronRelativistic_nm(energy_eV), 4)

        for energy_eV in wavelengthsPhoton_A:
            self.assertAlmostEquals(wavelengthsPhoton_A[energy_eV] / 10.0, MacHenke.WavelenghtPhoton_nm(energy_eV), 1)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testComputeMac_cm2_g(self):
        mac_cm2_g = self.macData.compute_mac_cm2_g(28, 10.2, 1.14)

        self.assertAlmostEquals((8.01), mac_cm2_g*1.0E-4, 2)

        mac_cm2_g = self.macData.compute_mac_cm2_g(28, 1486.7, 8.88)

        self.assertAlmostEquals((4.28), mac_cm2_g*1.0E-3, 2)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

if __name__ == '__main__': #pragma: no cover
    import nose
    nose.runmodule()
