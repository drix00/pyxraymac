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
__svnId__ = "$Id: test_MacPouchou1991.py 2293 2011-03-21 18:39:25Z hdemers $"

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
import MacPouchou1991

# Globals and constants variables.

class TestMacPouchou1991(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.mac = MacPouchou1991.MacPouchou1991()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testIsAvailable(self):
        self.assertEquals(True, self.mac.isAvailable(73, 14, 'Ka'))

        self.assertEquals(False, self.mac.isAvailable(73, 14, 'La'))

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testComputeMac_cm2_g(self):
        self.assertEquals(1490.0, self.mac.computeMac_cm2_g(73, 14, 'Ka'))

        self.assertEquals(3500.0, self.mac.computeMac_cm2_g(5, 5, 'Ka'))

        self.assertEquals(13500.0, self.mac.computeMac_cm2_g(26, 6, 'Ka'))

        self.assertEquals(15500.0, self.mac.computeMac_cm2_g(73, 7, 'Ka'))

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testExtractTransitionKey(self):
        self.assertEquals('Ka', self.mac.extractTransitionKey('Ka'))

        self.assertEquals('Ka', self.mac.extractTransitionKey('K'))

        self.assertEquals('Ka', self.mac.extractTransitionKey('Ka1'))

        self.assertEquals('Ka', self.mac.extractTransitionKey('Ka2'))

        self.assertEquals('La', self.mac.extractTransitionKey('La'))

        self.assertEquals('La', self.mac.extractTransitionKey('L'))

        self.assertEquals('La', self.mac.extractTransitionKey('La2'))

        self.assertEquals('Lb', self.mac.extractTransitionKey('Lb'))

        self.assertEquals('La', self.mac.extractTransitionKey('L'))

        self.assertEquals('Lb', self.mac.extractTransitionKey('Lb2'))

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
