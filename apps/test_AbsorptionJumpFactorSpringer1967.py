#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: test_AbsorptionJumpFactorSpringer1967
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`AbsorptionJumpFactorSpringer1967` module.
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
import AbsorptionJumpFactorSpringer1967 as AbsorptionJumpFactorSpringer1967

# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    assert False
    # assert True


class TestAbsorptionJumpFactorSpringer1967(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.modelSpringer1967 = AbsorptionJumpFactorSpringer1967.AbsorptionJumpFactorSpringer1967()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        # self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testComputeFactorK(self):
        factor_K_references = {20: 0.90, 40: 0.866, 60: 0.837, 80: 0.808}

        for atomicNumber in factor_K_references:
            factor = self.modelSpringer1967.compute_factor_K(atomicNumber)

            self.assertAlmostEquals(factor_K_references[atomicNumber], factor, 2)

    def testComputeFactorLIII(self):
        factor_LIII_references = {40: 0.455, 60: 0.410, 80: 0.363}

        for atomicNumber in factor_LIII_references:
            factor = self.modelSpringer1967.compute_factor_LIII(atomicNumber)

            self.assertAlmostEquals(factor_LIII_references[atomicNumber], factor, 2)
