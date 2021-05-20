#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2007 Hendrix Demers"
__license__ = ""

# Standard library modules.
import configparser

# Third party modules.
import pylab

# Local modules.
import pybrunetti2004data.XRayLib_2_4 as XRayLib_2_4
import DatabasesTools.deboer1989.FluorescenceYields as FluorescenceYields

# Globals and constants variables.

class AbsorptionJumpRatio(object):
    def __init__(self, configurationFile):
        self.readConfigurationFile(configurationFile)

        self.xraylib = XRayLib_2_4.XRayLib_2_4(configurationFile=configurationFile)

        self.fluorescenceYieldsModel = FluorescenceYields.FluorescenceYields(configurationFile)

        self.jumpRatioModel = self.xraylib.getAbsorptionJumpRatio

    def readConfigurationFile(self, configurationFile):
        """ Read the configuration file for options."""
        # pylint: disable-msg=W0201
        config = configparser.SafeConfigParser()

        config.readfp(open(configurationFile))

#        if config.has_section("AbsorptionJumpRatio"):
#            if config.has_option("AbsorptionJumpRatio", "pathname"):
#                self.pathname = config.get("AbsorptionJumpRatio", "pathname")

    def getAbsorptionJumpFactor(self, atomicNumber, subshell, xrayEnergy_eV):
        absorptionJumpFactor = 0.0

        if subshell == 'K':
            absorptionJumpFactor = self.computeKSubshellAbsorptionJumpFactor(atomicNumber, xrayEnergy_eV)

        if subshell == 'LI' or subshell == 'L1':
            absorptionJumpFactor = self.computeLISubshellAbsorptionJumpFactor(atomicNumber, xrayEnergy_eV)

        if subshell == 'LII' or subshell == 'L2':
            absorptionJumpFactor = self.computeLIISubshellAbsorptionJumpFactor(atomicNumber, xrayEnergy_eV)

        if subshell == 'LIII' or subshell == 'L3':
            absorptionJumpFactor = self.computeLIIISubshellAbsorptionJumpFactor(atomicNumber, xrayEnergy_eV)

        if subshell == 'MI' or subshell == 'M1':
            absorptionJumpFactor = 0.0

        if subshell == 'MII' or subshell == 'M2':
            EM2_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'M2')

            if EM2_eV > 0.0:
                absorptionJumpFactor = self.computeM234SubshellAbsorptionJumpFactor(atomicNumber, xrayEnergy_eV)
            else:
                absorptionJumpFactor = 0.0

        if subshell == 'MIII' or subshell == 'M3':
            EM3_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'M3')

            if EM3_eV > 0.0:
                absorptionJumpFactor = self.computeM234SubshellAbsorptionJumpFactor(atomicNumber, xrayEnergy_eV)
            else:
                absorptionJumpFactor = 0.0

        if subshell == 'MIV' or subshell == 'M4':
            EM4_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'M4')

            if EM4_eV > 0.0:
                absorptionJumpFactor = self.computeM234SubshellAbsorptionJumpFactor(atomicNumber, xrayEnergy_eV)
            else:
                absorptionJumpFactor = 0.0

        if subshell == 'MV' or subshell == 'M5':
            absorptionJumpFactor = self.computeMVSubshellAbsorptionJumpFactor(atomicNumber, xrayEnergy_eV)

        return absorptionJumpFactor

    def computeKSubshellAbsorptionJumpFactor(self, atomicNumber, xrayEnergy_eV):
        EK_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'K')

        if xrayEnergy_eV >= EK_eV and EK_eV > 0.0:
            rK = self.jumpRatioModel(atomicNumber, 'K')

            nominator = rK - 1.0

            denominator = rK

            factor = nominator/denominator

            return factor
        else:
            return 0.0

    def computeLISubshellAbsorptionJumpFactor(self, atomicNumber, xrayEnergy_eV):
        EL1_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'L1')

        if xrayEnergy_eV >= EL1_eV and EL1_eV > 0.0:
            rL1 = self.jumpRatioModel(atomicNumber, 'L1')

            nominator = rL1 - 1.0

            denominator = rL1

            factor = nominator/denominator

            EK_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'K')

            if xrayEnergy_eV >= EK_eV and EK_eV > 0.0:
                rK = self.jumpRatioModel(atomicNumber, 'K')

                JK = self.computeKSubshellAbsorptionJumpFactor(atomicNumber, EK_eV)

                nKL1 = self.fluorescenceYieldsModel.getNKL1(atomicNumber)

                factor = factor/rK + JK*nKL1

            return factor
        else:
            return 0.0

    def computeLIISubshellAbsorptionJumpFactor(self, atomicNumber, xrayEnergy_eV):
        EL2_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'L2')

        if xrayEnergy_eV >= EL2_eV and EL2_eV > 0.0:
            rL2 = self.jumpRatioModel(atomicNumber, 'L2')

            nominator = rL2 - 1.0

            denominator = rL2

            factor = nominator/denominator

            EL1_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'L1')

            if xrayEnergy_eV >= EL1_eV and EL1_eV > 0.0:
                rL1 = self.jumpRatioModel(atomicNumber, 'L1')

                JL1 = self.computeLISubshellAbsorptionJumpFactor(atomicNumber, EL1_eV)

                f12 = self.xraylib.getCosterKronigTransitionProbability(atomicNumber, 'F12')

                factor = factor/rL1 + JL1*f12

                EK_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'K')

                if xrayEnergy_eV >= EK_eV and EK_eV > 0.0:
                    rK = self.jumpRatioModel(atomicNumber, 'K')

                    JK = self.computeKSubshellAbsorptionJumpFactor(atomicNumber, EK_eV)

                    nKL1 = self.fluorescenceYieldsModel.getNKL1(atomicNumber)

                    nKL2 = self.fluorescenceYieldsModel.getNKL2(atomicNumber)

                    factor = factor/rK + JK*(nKL2 + nKL1*f12)

            return factor
        else:
            return 0.0

    def computeLIIISubshellAbsorptionJumpFactor(self, atomicNumber, xrayEnergy_eV):
        EL3_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'L3')

        if xrayEnergy_eV >= EL3_eV and EL3_eV > 0.0:
            rL3 = self.jumpRatioModel(atomicNumber, 'L3')

            nominator = rL3 - 1.0

            denominator = rL3

            factor = nominator/denominator

            EL2_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'L2')

            if xrayEnergy_eV >= EL2_eV and EL2_eV > 0.0:
                rL2 = self.jumpRatioModel(atomicNumber, 'L2')

                JL2 = self.computeLIISubshellAbsorptionJumpFactor(atomicNumber, EL2_eV)

                f23 = self.xraylib.getCosterKronigTransitionProbability(atomicNumber, 'F23')

                factor = factor/rL2 + JL2*f23

                EL1_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'L1')

                if xrayEnergy_eV >= EL1_eV and EL1_eV > 0.0:
                    rL1 = self.jumpRatioModel(atomicNumber, 'L1')

                    JL1 = self.computeLISubshellAbsorptionJumpFactor(atomicNumber, EL1_eV)

                    f13 = self.xraylib.getCosterKronigTransitionProbability(atomicNumber, 'F13')

                    f12 = self.xraylib.getCosterKronigTransitionProbability(atomicNumber, 'F12')

                    factor = factor/rL1 + JL1*(f13 + f12*f23)

                    EK_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'K')

                    if xrayEnergy_eV >= EK_eV and EK_eV > 0.0:
                        rK = self.jumpRatioModel(atomicNumber, 'K')

                        JK = self.computeKSubshellAbsorptionJumpFactor(atomicNumber, EK_eV)

                        nKL1 = self.fluorescenceYieldsModel.getNKL1(atomicNumber)

                        nKL2 = self.fluorescenceYieldsModel.getNKL2(atomicNumber)

                        nKL3 = self.fluorescenceYieldsModel.getNKL3(atomicNumber)

                        factor = factor/rK + JK*(nKL3 + nKL2*f23 + nKL1*f13)

            return factor
        else:
            return 0.0

    def computeM234SubshellAbsorptionJumpFactor(self, atomicNumber, xrayEnergy_eV):
        EM5_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'M5')

        if xrayEnergy_eV < EM5_eV and EM5_eV > 0.0:
            return 0.0

        EM4_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'M4')

        if xrayEnergy_eV < EM4_eV and EM4_eV > 0.0:
            return 0.0

        EM3_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'M3')

        if xrayEnergy_eV < EM3_eV and EM3_eV > 0.0:
            return 0.33

        EM2_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'M2')

        if xrayEnergy_eV < EM2_eV and EM2_eV > 0.0:
            return 0.29

        EM1_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'M1')

        if xrayEnergy_eV < EM1_eV and EM1_eV > 0.0:
            return 0.33

        EL3_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'L3')

        if xrayEnergy_eV < EL3_eV and EL3_eV > 0.0:
            return 0.30

        EL2_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'L2')

        if xrayEnergy_eV < EL2_eV and EL2_eV > 0.0:
            return 0.20

        EL1_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'L1')

        if xrayEnergy_eV < EL1_eV and EL1_eV > 0.0:
            return 0.54

        EK_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'K')

        if xrayEnergy_eV < EK_eV and EK_eV > 0.0:
            return 0.63

        if xrayEnergy_eV > EK_eV and EK_eV > 0.0:
            return 0.20

        return 0.0

    def computeMVSubshellAbsorptionJumpFactor(self, atomicNumber, xrayEnergy_eV):
        if atomicNumber >= 57 and atomicNumber <= 78:
            EM5_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'M5')

            if xrayEnergy_eV < EM5_eV and EM5_eV > 0.0:
                return 0.0

            EM4_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'M4')

            if xrayEnergy_eV < EM4_eV and EM4_eV > 0.0:
                return 0.67

            EM3_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'M3')

            if xrayEnergy_eV < EM3_eV and EM3_eV > 0.0:
                return 0.55

            EM2_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'M2')

            if xrayEnergy_eV < EM2_eV and EM2_eV > 0.0:
                return 0.59

            EM1_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'M1')

            if xrayEnergy_eV < EM1_eV and EM1_eV > 0.0:
                return 0.56

            EL3_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'L3')

            if xrayEnergy_eV < EL3_eV and EL3_eV > 0.0:
                return 0.52

            EL2_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'L2')

            if xrayEnergy_eV < EL2_eV and EL2_eV > 0.0:
                return 1.01

            EL1_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'L1')

            if xrayEnergy_eV < EL1_eV and EL1_eV > 0.0:
                return 0.86

            EK_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'K')

            if xrayEnergy_eV < EK_eV and EK_eV > 0.0:
                return 0.92

            if xrayEnergy_eV > EK_eV and EK_eV > 0.0:
                return 0.24
        elif atomicNumber >= 79 and atomicNumber <= 94:
            EM5_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'M5')

            if xrayEnergy_eV < EM5_eV and EM5_eV > 0.0:
                return 0.0

            EM4_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'M4')

            if xrayEnergy_eV < EM4_eV and EM4_eV > 0.0:
                return 0.56

            EM3_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'M3')

            if xrayEnergy_eV < EM3_eV and EM3_eV > 0.0:
                return 0.39

            EM2_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'M2')

            if xrayEnergy_eV < EM2_eV and EM2_eV > 0.0:
                return 0.45

            EM1_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'M1')

            if xrayEnergy_eV < EM1_eV and EM1_eV > 0.0:
                return 0.43

            EL3_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'L3')

            if xrayEnergy_eV < EL3_eV and EL3_eV > 0.0:
                return 0.40

            EL2_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'L2')

            if xrayEnergy_eV < EL2_eV and EL2_eV > 0.0:
                return 0.92

            EL1_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'L1')

            if xrayEnergy_eV < EL1_eV and EL1_eV > 0.0:
                return 0.68

            EK_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomicNumber, 'K')

            if xrayEnergy_eV < EK_eV and EK_eV > 0.0:
                return 0.83

            if xrayEnergy_eV > EK_eV and EK_eV > 0.0:
                return 0.24

        return 0.0

def run(display=False):
    absorptionJumpRatio = AbsorptionJumpRatio("AbsorptionJumpRatio.cfg")

    atomicNumbers = range(5, 95, 5)

    subshells = ['K', 'LI', 'LII', 'LIII', 'MV', 'MIV']

    factors = {}

    for subshell in subshells:
        factors.setdefault(subshell, [])

        for atomicNumber in atomicNumbers:
            xrayEnergy_eV = 200.0E3

            factor = absorptionJumpRatio.getAbsorptionJumpFactor(atomicNumber, subshell, xrayEnergy_eV)

            factors[subshell].append(factor)

    if display:
        pylab.clf()

        for subshell in subshells:

            pylab.plot(atomicNumbers, factors[subshell], label=subshell)

        pylab.legend(loc='best')

        pylab.xlabel('Atomic number')

        pylab.ylabel('Absorption jump factor')

        pylab.show()

if __name__ == '__main__': #pragma: no cover
    import pyHendrixDemersTools.Runner as Runner
    Runner.Runner().run(runFunction=run)
