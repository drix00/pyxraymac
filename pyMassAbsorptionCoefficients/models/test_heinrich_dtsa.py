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
import pyMassAbsorptionCoefficients.models.heinrich_dtsa as MacHeinrichDTSA
from nose import SkipTest


# Globals and constants variables.

class TestMacHeinrichDTSA(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        configurationFile = Files.getCurrentModulePath(__file__, "../MassAbsorptionCoefficient.cfg")
        if not os.path.isfile(configurationFile):
            raise SkipTest

        self.macModel = MacHeinrichDTSA.MacHeinrichDTSA(configurationFile=configurationFile)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testComputeMAC_cm2_g(self):
        value = self.macModel.computeMac_cm2_g(1041.0, 79)

        #print value
        self.assertAlmostEqual(4698.6, value, 1)

        #self.fail("Test if the TestCase is working.")

if __name__ == '__main__':    #pragma: no cover
    import nose
    nose.runmodule()
