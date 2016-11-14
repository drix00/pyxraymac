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
import logging

# Third party modules.

# Local modules.
import pyMassAbsorptionCoefficients.AbsorptionJumpFactorSpringer1967 as AbsorptionJumpFactorSpringer1967

# Globals and constants variables.

class TestAbsorptionJumpFactorSpringer1967(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.modelSpringer1967 = AbsorptionJumpFactorSpringer1967.AbsorptionJumpFactorSpringer1967()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testComputeFactorK(self):
        factorKReferences = {20: 0.90, 40: 0.866, 60: 0.837, 80: 0.808}

        for atomicNumber in factorKReferences:
            factor = self.modelSpringer1967.computeFactorK(atomicNumber)

            self.assertAlmostEquals(factorKReferences[atomicNumber], factor, 2)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testComputeFactorLIII(self):
        factorLIIIReferences = {40: 0.455, 60: 0.410, 80: 0.363}

        for atomicNumber in factorLIIIReferences:
            factor = self.modelSpringer1967.computeFactorLIII(atomicNumber)

            self.assertAlmostEquals(factorLIIIReferences[atomicNumber], factor, 2)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
