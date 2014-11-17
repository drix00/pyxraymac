#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2007 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2293 $"
__svnDate__ = "$Date: 2011-03-21 14:39:25 -0400 (Mon, 21 Mar 2011) $"
__svnId__ = "$Id: test_MacHeinrich1987.py 2293 2011-03-21 18:39:25Z hdemers $"

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
import MacHeinrich1987
import DatabasesTools.DTSA.XRayTransitionData as XRayTransitionData
import pyHendrixDemersTools.Files as Files

# Globals and constants variables.

class TestMacHeinrich1987(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        configurationFile = Files.getCurrentModulePath(__file__, "MassAbsorptionCoefficient.cfg")

        xrayTransitionData = XRayTransitionData.XRayTransitionData(configurationFile)

        self.heinrich1987 = MacHeinrich1987.MacHeinrich1987(xrayTransitionData)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testAbsorberBoron(self):
        """
        Test energy region 1, Z < 6.

        """
        macs_cm2_g = {183.0: 2861.0, 277.0: 39838.0}

        atomicNumberAbsorber = 5

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.computeMac_cm2_g(energy_eV, atomicNumberAbsorber)

            self.assertAlmostEquals(macs_cm2_g[energy_eV], mac_cm2_g, 0)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testAbsorberCarbon(self):
        """
        Test energy region 1, Z > 5.

        """
        macs_cm2_g = {183.0: 5945.0, 277.0: 2147.0, 392.0: 23586.0}

        atomicNumberAbsorber = 6

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.computeMac_cm2_g(energy_eV, atomicNumberAbsorber)

            self.assertAlmostEquals(macs_cm2_g[energy_eV], mac_cm2_g, 0)

#        mac_cm2_g = self.heinrich1987.computeMac_cm2_g(energy_eV, atomicNumberAbsorber)
        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testRegion2(self):
        """
        Test energy region 2.

        """
        macs_cm2_g = {2014.0: 2238.0, 8048.0: 52.4}

        atomicNumberAbsorber = 29

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.computeMac_cm2_g(energy_eV, atomicNumberAbsorber)

            self.assertAlmostEquals(macs_cm2_g[energy_eV], mac_cm2_g, 0)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testRegion3(self):
        """
        Test energy region 3.

        """
        macs_cm2_g = {3692.0: 1409.0, 3590.0: 1508.7}

        atomicNumberAbsorber = 47

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.computeMac_cm2_g(energy_eV, atomicNumberAbsorber)

            self.assertAlmostEquals(macs_cm2_g[energy_eV], mac_cm2_g, 0)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testRegion4(self):
        """
        Test energy region 4.

        """
        macs_cm2_g = {3444.0: 1254.0, 3487.0: 1217.0}

        atomicNumberAbsorber = 47

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.computeMac_cm2_g(energy_eV, atomicNumberAbsorber)

            self.assertAlmostEquals(macs_cm2_g[energy_eV], mac_cm2_g, 0)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testAbsorberCopper(self):
        """
        Test energy region 5, Z < 30.

        """
        macs_cm2_g = {183.0: 37113.3, 277.0: 19141.5, 392.0: 9925.8}

        atomicNumberAbsorber = 29

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.computeMac_cm2_g(energy_eV, atomicNumberAbsorber)

            self.assertAlmostEquals(macs_cm2_g[energy_eV], mac_cm2_g, 0)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testAbsorberZinc(self):
        """
        Test energy region 5, Z > 29.

        """
        macs_cm2_g = {183.0: 40790.1, 277.0: 21582.7, 392.0: 11317.3}

        atomicNumberAbsorber = 30

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.computeMac_cm2_g(energy_eV, atomicNumberAbsorber)

            self.assertAlmostEquals(macs_cm2_g[energy_eV], mac_cm2_g, 0)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testAbsorberNeodymium(self):
        """
        Test energy region 5, Z < 61.

        """
        macs_cm2_g = {1740.0: 4229.0, 2014.0: 3059.9, 5899.0: 204.2}

        atomicNumberAbsorber = 60

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.computeMac_cm2_g(energy_eV, atomicNumberAbsorber)

            self.assertAlmostEquals(macs_cm2_g[energy_eV], mac_cm2_g, 0)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testAbsorberPromethium(self):
        """
        Test energy region 5, Z > 60.

        """
        #macs_cm2_g = {1740.0: 4511.0, 2014.0: 3252.0, 5899.0: 219.1}
        macs_cm2_g = {1740.0: 4573.6, 2014.0: 3296.5, 5899.0: 219.1}

        atomicNumberAbsorber = 61

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.computeMac_cm2_g(energy_eV, atomicNumberAbsorber)

            self.assertAlmostEquals(macs_cm2_g[energy_eV], mac_cm2_g, 0)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testRegion6(self):
        """
        Test energy region 6.

        """
        macs_cm2_g = {2958.0: 2192.0, 3314: 1801.5, 3692.0: 1496.0}

        atomicNumberAbsorber = 79

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.computeMac_cm2_g(energy_eV, atomicNumberAbsorber)

            self.assertAlmostEquals(macs_cm2_g[energy_eV], mac_cm2_g, 0)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testRegion6M4(self):
        """
        Test energy region 6 with and wihout M4.

        """
        macs_cm2_g = {2958.0: 2192.0, 3314: 1801.5, 3692.0: 1496.0}

        atomicNumberAbsorber = 79

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.computeMac_cm2_g(energy_eV, atomicNumberAbsorber)

            self.assertAlmostEquals(macs_cm2_g[energy_eV], mac_cm2_g, 0)

        macs_cm2_g = {100.0: 100070.5, 105.0: 105933.2, 183.0: 42943.0}

        atomicNumberAbsorber = 31

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.computeMac_cm2_g(energy_eV, atomicNumberAbsorber)

            self.assertAlmostEquals(macs_cm2_g[energy_eV], mac_cm2_g, 0)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)


    def testRegion7(self):
        """
        Test energy region 7.

        """
        macs_cm2_g = {2622.0: 2418.0, 2958: 2192.0, 3314.0: 1801.5}

        atomicNumberAbsorber = 79

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.computeMac_cm2_g(energy_eV, atomicNumberAbsorber)

            self.assertAlmostEquals(macs_cm2_g[energy_eV], mac_cm2_g, 0)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testRegion8(self):
        """
        Test energy region 8.

        """
        macs_cm2_g = {2014.0: 1192.0, 2622.0: 2418.0, 2958: 2192.0}

        atomicNumberAbsorber = 79

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.computeMac_cm2_g(energy_eV, atomicNumberAbsorber)

            self.assertAlmostEquals(macs_cm2_g[energy_eV], mac_cm2_g, 0)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testRegion9(self):
        """
        Test energy region 9.

        """
        macs_cm2_g = {2014.0: 1192.0, 2257.0: 1468.0, 2395.0: 3073.9}

        atomicNumberAbsorber = 79

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.computeMac_cm2_g(energy_eV, atomicNumberAbsorber)

            self.assertAlmostEquals(macs_cm2_g[energy_eV], mac_cm2_g, 0)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testRegion10(self):
        """
        Test energy region 10.

        """
        macs_cm2_g = {849.0: 6763.5, 2014.0: 1192.0, 2257.0: 1468.0}

        atomicNumberAbsorber = 79

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.computeMac_cm2_g(energy_eV, atomicNumberAbsorber)

            self.assertAlmostEquals(macs_cm2_g[energy_eV], mac_cm2_g, 0)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

# TODO: Test energy region 11.
    def testRegion11(self):
        """
        Test energy region 11.

        """
        #macs_cm2_g = {183.0: 10876.0, 277.0: 16874.0, 392.0: 14695.0, 677.0: 9285.0, 849.0: 6763.5}

        macs_cm2_g = {}

        atomicNumberAbsorber = 79

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.computeMac_cm2_g(energy_eV, atomicNumberAbsorber)

            self.assertAlmostEquals(macs_cm2_g[energy_eV], mac_cm2_g, 0)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testAbsorberPlutomium(self):
        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testGetRegion(self):
        regions = {86.4+1.0: 11
                            , 107.8+1.0: 11
                            , 333.89+1.0: 11
                            , 351.99+1.0: 11
                            , 545.38+1.0: 11
                            , 643.67+1.0: 11
                            , 758.77+1.0: 10
                            , 2205.6+1.0: 9
                            , 2291.0+1.0: 8
                            , 2742.9+1.0: 7
                            , 3147.7+1.0: 6
                            , 3424.8+1.0: 5
                            , 11918.0+1.0: 4
                            , 13733.0+1.0: 3
                            , 14352.0+1.0: 2
                            , 80722.0+1.0: 1
                            }

        atomicNumberAbsorber = 79

        for xrayEnergy_eV in regions:
            region = self.heinrich1987.getRegion(atomicNumberAbsorber, xrayEnergy_eV)

            self.assertEquals(regions[xrayEnergy_eV], region)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testLowEnergy(self):
        atomicNumberAbsorber = 14
        energy_eV = 1.0

        mac_cm2_g = self.heinrich1987.computeMac_cm2_g(energy_eV, atomicNumberAbsorber)

        self.assertAlmostEquals(1.0E6, mac_cm2_g, 0)

        atomicNumberAbsorber = 79
        energy_eV = 1.0

        mac_cm2_g = self.heinrich1987.computeMac_cm2_g(energy_eV, atomicNumberAbsorber)

        self.assertAlmostEquals(1.0E6, mac_cm2_g, 0)
        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
