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

import xray.mac.models.pouchou1991 as MacPouchou1991


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

    def test_is_available(self):
        self.assertEquals(True, self.mac.is_available(73, 14, 'Ka'))

        self.assertEquals(False, self.mac.is_available(73, 14, 'La'))

        #self.fail("Test if the TestCase is working.")

    def test_mac_cm2_g(self):
        self.assertEquals(1490.0, self.mac.mac_cm2_g(73, 14, 'Ka'))

        self.assertEquals(3500.0, self.mac.mac_cm2_g(5, 5, 'Ka'))

        self.assertEquals(13500.0, self.mac.mac_cm2_g(26, 6, 'Ka'))

        self.assertEquals(15500.0, self.mac.mac_cm2_g(73, 7, 'Ka'))

        #self.fail("Test if the TestCase is working.")

    def test_extract_transition_key(self):
        self.assertEquals('Ka', self.mac.extract_transition_key('Ka'))

        self.assertEquals('Ka', self.mac.extract_transition_key('K'))

        self.assertEquals('Ka', self.mac.extract_transition_key('Ka1'))

        self.assertEquals('Ka', self.mac.extract_transition_key('Ka2'))

        self.assertEquals('La', self.mac.extract_transition_key('La'))

        self.assertEquals('La', self.mac.extract_transition_key('L'))

        self.assertEquals('La', self.mac.extract_transition_key('La2'))

        self.assertEquals('Lb', self.mac.extract_transition_key('Lb'))

        self.assertEquals('La', self.mac.extract_transition_key('L'))

        self.assertEquals('Lb', self.mac.extract_transition_key('Lb2'))

        self.assertEquals('Ma', self.mac.extract_transition_key('Ma'))

        #self.fail("Test if the TestCase is working.")

if __name__ == '__main__':    #pragma: no cover
    import nose
    nose.runmodule()
