#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.mac.models.test_pouchou1991
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`xray.mac.models.pouchou1991` module.
"""

###############################################################################
# Copyright 2021 Hendrix Demers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

# Standard library modules.
import unittest

# Third party modules.

# Local modules.

# Project modules.
import xray.mac.models.pouchou1991 as MacPouchou1991

# Globals and constants variables.


class TestMacPouchou1991(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.mac = MacPouchou1991.MacPouchou1991()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        # self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def test_is_available(self):
        self.assertEquals(True, self.mac.is_available(73, 14, 'Ka'))

        self.assertEquals(False, self.mac.is_available(73, 14, 'La'))

    def test_mac_cm2_g(self):
        self.assertEquals(1490.0, self.mac.mac_cm2_g(73, 14, 'Ka'))

        self.assertEquals(3500.0, self.mac.mac_cm2_g(5, 5, 'Ka'))

        self.assertEquals(13500.0, self.mac.mac_cm2_g(26, 6, 'Ka'))

        self.assertEquals(15500.0, self.mac.mac_cm2_g(73, 7, 'Ka'))

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
