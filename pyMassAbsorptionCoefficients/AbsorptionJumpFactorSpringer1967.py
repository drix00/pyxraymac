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
__svnId__ = "$Id: AbsorptionJumpFactorSpringer1967.py 2293 2011-03-21 18:39:25Z hdemers $"

# Standard library modules.

# Third party modules.

# Local modules.

# Globals and constants variables.

class AbsorptionJumpFactorSpringer1967(object):
    """
    Compute the absorption jump factor from the model of Springer (1967).

    Reference: springer1967
        Sagel K. (1959): Tabellen zur Rontgenemissions- und -absorptionsanalyse
        (Berlin-Gottingen-Heidelberg: Springer).


    Fit of the values from Sagel (1959) for the K and L3 subshell only.


    """
    def getFactor(self, atomicNumber, line, xrayEnergy_eV=None):
        if line == 'Ka':
            factor = self.computeFactorK(atomicNumber)

            return factor

        if line == 'La':
            factor = self.computeFactorLIII(atomicNumber)

            return factor

    def computeFactorK(self, atomicNumber):
        """
        Compute the absorption jump factor for the K subshell

        \f[
            \frac{r_{K} - 1}{r_{K}} = 0.924 -0.00144 \cdot Z
        \f]

        Mandatory arguments:


        Optional arguments:


        Extra arguments:


        Return parameters:

        """
        factor = 0.924 - 0.00144*atomicNumber

        return factor

    def computeFactorLIII(self, atomicNumber):
        """
        Compute the absorption jump factor for the L3 subshell

        \f[
            \frac{r_{L_{III}} - 1}{r_{L_{III}} \cdot r_{L_{II}} \cdot r_{L_{I}}} = 0.548 - 0.00231 \cdot Z
        \f]

        Mandatory arguments:


        Optional arguments:


        Extra arguments:


        Return parameters:

        """
        factor = 0.548 - 0.00231*atomicNumber

        return factor

if __name__ == '__main__': #pragma: no cover
    import pyHendrixDemersTools.Runner as Runner
    Runner.Runner().run(runFunction=None)
