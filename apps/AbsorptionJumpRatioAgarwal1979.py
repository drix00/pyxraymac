#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: AbsorptionJumpRatioAgarwal1979
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Compute the absorption jump factor from the model of Agarwal (1979).
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
import math

# Third party modules.

# Local modules.

# Project modules.

# Globals and constants variables.


def getRKJonsson1928(lambdaLI, lambdaK):
    """
    Value of $r_{K}$ from Jonsson (1928).

    Reference: E. J\"{o}nsson, Thesis, Upsala (1928).

    \f[
        r_{K} = \frac{\lambda_{L_{I}}}{\lambda_{L_{K}}}
    \f]

    Mandatory arguments:


    Optional arguments:


    Extra arguments:


    Return parameters:

    """
    rK = lambdaLI*lambdaK

    return rK


def getRKRindfleisch1937(atomic_number):
    """
    Value of $r_{K}$ from Rindfleisch (1937).

    Reference: H. Rindfleisch, Ann. Phys. 28, 409 (1937)

    \f[
        r_{K} = a \cdot Z^{b}
    \f]
    where $\log_{10} a = 1.805283$ and $b = -0.6207$

    Mandatory arguments:


    Optional arguments:


    Extra arguments:


    Return parameters:

    """
    log10A = 1.805283

    b = -0.6207

    a = math.pow(10.0, log10A)

    rK = a*math.pow(atomic_number, b)

    return rK


def getRKLaubert1941(lambdaK):
    """
    Value of $r_{K}$ from Laubert (1941).

    Reference: S. Laubert, Ann. Phys. 40, 553 (1941)

    \f[
        r_{K} = a \cdot \lambda_{L_{K}}^{b}
    \f]
    where $\log_{10} a = 0.857652$ and $b = 0.0843$

    Mandatory arguments:


    Optional arguments:


    Extra arguments:


    Return parameters:

    """
    log10A = 0.857652

    b = 0.0843

    a = math.pow(10.0, log10A)

    rK = a*math.pow(lambdaK, b)

    return rK


def getRKTellezPlasencia1949(atomic_number):
    """
    Value of $r_{K}$ from Tellez-Plasencia (1949).

    Reference: H. Tellez-Plasencia, J. Phys. Radium. 10, 14 (1949)

    \f[
        r_{K} = \frac{1}{a + b Z}
    \f]
    where $a = 0.051167$ and $b = 0.0024882$

    Mandatory arguments:


    Optional arguments:


    Extra arguments:


    Return parameters:

    """
    a = 0.051167

    b = 0.0024882


    rK = 1.0/(a + b * atomic_number)

    return rK
