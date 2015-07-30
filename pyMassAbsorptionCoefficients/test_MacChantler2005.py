#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2940 $"
__svnDate__ = "$Date: 2014-11-26 19:25:19 -0500 (Wed, 26 Nov 2014) $"
__svnId__ = "$Id: test_Chantler2005.py 2940 2014-11-27 00:25:19Z hdemers $"

# Standard library modules.
import unittest
import os.path

# Third party modules.

# Local modules.
import pyMassAbsorptionCoefficients.MacChantler2005 as Chantler2005
import pyHendrixDemersTools.Files as Files

# Globals and constants variables.

class TestChantler2005(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.configurationPath = Files.getCurrentModulePath(__file__, "../testData/macTests.cfg")
        self.mac = Chantler2005.Chantler2005(self.configurationPath)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test_readConfigurationFile(self):
        self.configurationPath = Files.getCurrentModulePath(__file__, "../testData/macTests.cfg")
        self.assertTrue(os.path.isfile(self.configurationPath))

        self.assertTrue(os.path.isfile(self.mac._filepath))

        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test_readFile(self):
        self.mac._readFile()

        self.assertEquals(92, len(self.mac._experimentalData))

        atomicNumber = 1
        energies_eV = self.mac._experimentalData[atomicNumber][Chantler2005.ENERGIES_eV]
        mac_cm2_g = self.mac._experimentalData[atomicNumber][Chantler2005.MAC_cm2_g]

        self.assertAlmostEquals(0.013668*1.0e3, energies_eV[0])
        self.assertAlmostEquals(2907600.0, mac_cm2_g[0])

        self.assertAlmostEquals(432.9451*1.0e3, energies_eV[-1])
        self.assertAlmostEquals(0.0000000088048, mac_cm2_g[-1])

        atomicNumber = 92
        energies_eV = self.mac._experimentalData[atomicNumber][Chantler2005.ENERGIES_eV]
        mac_cm2_g = self.mac._experimentalData[atomicNumber][Chantler2005.MAC_cm2_g]

        self.assertAlmostEquals(0.0324615*1.0e3, energies_eV[0])
        self.assertAlmostEquals(43925.0, mac_cm2_g[0])

        self.assertAlmostEquals(432.9451*1.0e3, energies_eV[-1])
        self.assertAlmostEquals(0.15459, mac_cm2_g[-1])

        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test_readFileNISTMonte2(self):
        self.mac._filename = "FFastMAC_nistMonte2.csv"
        self.mac._energyUnit = Chantler2005.ENERGY_UNIT_eV
        self.mac._createFilepath()

        self.mac._readFile()

        self.assertEquals(92, len(self.mac._experimentalData))

        atomicNumber = 1
        energies_eV = self.mac._experimentalData[atomicNumber][Chantler2005.ENERGIES_eV]
        mac_cm2_g = self.mac._experimentalData[atomicNumber][Chantler2005.MAC_cm2_g]

        self.assertAlmostEquals(10.69, energies_eV[0])
        self.assertAlmostEquals(0.22129, mac_cm2_g[0])

        self.assertAlmostEquals(432945.1, energies_eV[-1])
        self.assertAlmostEquals(0.1753, mac_cm2_g[-1])

        atomicNumber = 92
        energies_eV = self.mac._experimentalData[atomicNumber][Chantler2005.ENERGIES_eV]
        mac_cm2_g = self.mac._experimentalData[atomicNumber][Chantler2005.MAC_cm2_g]

        self.assertAlmostEquals(10.69, energies_eV[0])
        self.assertAlmostEquals(0.00012189, mac_cm2_g[0])

        self.assertAlmostEquals(432945.1, energies_eV[-1])
        self.assertAlmostEquals(0.23698, mac_cm2_g[-1])

        #self.fail("Test if the testcase is working.")
        self.assert_(True)

if __name__ == '__main__':    #pragma: no cover
    import nose
    nose.runmodule()
