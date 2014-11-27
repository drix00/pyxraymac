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
__svnId__ = "$Id: test_AbsorptionJumpRatio.py 2293 2011-03-21 18:39:25Z hdemers $"

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
import pyMassAbsorptionCoefficients.AbsorptionJumpRatio as AbsorptionJumpRatio
import pyHendrixDemersTools.Files as Files

# Globals and constants variables.

class TestAbsorptionJumpRatio(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        configurationFile = Files.getCurrentModulePath(__file__, "AbsorptionJumpRatio.cfg")

        self.absorptionJumpRatio = AbsorptionJumpRatio.AbsorptionJumpRatio(configurationFile)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testReadConfigurationFile(self):
        configurationFile = Files.getCurrentModulePath(__file__, "AbsorptionJumpRatio.cfg")

        AbsorptionJumpRatio.AbsorptionJumpRatio(configurationFile)

        #self.assertEquals("pathname", absorptionJumpRatio.pathname)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testCopper(self):
        jumpFactorLI = 0.1174

        jumpFactorLIK = 0.1743

        jumpFactor = self.absorptionJumpRatio.getAbsorptionJumpFactor(29, 'LI', 1200.0)

        self.assertAlmostEquals(jumpFactorLI, jumpFactor, 3)

        jumpFactor = self.absorptionJumpRatio.getAbsorptionJumpFactor(29, 'LI', 12000.0)

        self.assertAlmostEquals(jumpFactorLIK, jumpFactor, 3)

    def testFEL3Al(self):
        jumpFactorReference = 0.49363

        jumpFactor = self.absorptionJumpRatio.getAbsorptionJumpFactor(26, 'L3', 1486.9)

        self.assertAlmostEquals(jumpFactorReference, jumpFactor, 3)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
