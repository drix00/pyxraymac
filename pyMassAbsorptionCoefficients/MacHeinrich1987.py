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
__svnId__ = "$Id: MacHeinrich1987.py 2293 2011-03-21 18:39:25Z hdemers $"

# Standard library modules.
import math
import warnings
warnings.simplefilter('ignore', UserWarning)

# Third party modules.
import numpy

# Local modules.
import pyMassAbsorptionCoefficients.MassAbsorptionCoefficientEnergy as MassAbsorptionCoefficientEnergy
import pySpecimenTools.ElementProperties as ElementProperties

# Globals and constants variables.

class MacHeinrich1987(MassAbsorptionCoefficientEnergy.MassAbsorptionCoefficientEnergy):
    def __init__(self, xrayTransitionData):
        self.xrayTransitionData = xrayTransitionData

        self.coefficientC = {1: self.computeCRegion1
                                                 , 2: self.computeCRegion2
                                                 , 3: self.computeCRegion3
                                                 , 4: self.computeCRegion4
                                                 , 5: self.computeCRegion5
                                                 , 6: self.computeCRegion6
                                                 , 7: self.computeCRegion7
                                                 , 8: self.computeCRegion8
                                                 , 9: self.computeCRegion9
                                                 , 10: self.computeCRegion10
                                                 , 11: self.computeCRegion11
                                                 }

        self.coefficientN = {1: self.computeNRegion1
                                                 , 2: self.computeNRegion2_4
                                                 , 3: self.computeNRegion2_4
                                                 , 4: self.computeNRegion2_4
                                                 , 5: self.computeNRegion5
                                                 , 6: self.computeNRegion6_9
                                                 , 7: self.computeNRegion6_9
                                                 , 8: self.computeNRegion6_9
                                                 , 9: self.computeNRegion6_9
                                                 , 10: self.computeNRegion10
                                                 , 11: self.computeNRegion11
                                                 }

        self.coefficientB_eV = {1: self.computeBRegion1
                                                 , 2: self.computeBRegion2_4
                                                 , 3: self.computeBRegion2_4
                                                 , 4: self.computeBRegion2_4
                                                 , 5: self.computeBRegion5
                                                 , 6: self.computeBRegion6_9
                                                 , 7: self.computeBRegion6_9
                                                 , 8: self.computeBRegion6_9
                                                 , 9: self.computeBRegion6_9
                                                 , 10: self.computeBRegion10
                                                 }

        self.coefficientA = {1: self.computeARegion1
                                                 , 2: self.computeARegion2_4
                                                 , 3: self.computeARegion2_4
                                                 , 4: self.computeARegion2_4
                                                 , 5: self.computeARegion5
                                                 , 6: self.computeARegion6_9
                                                 , 7: self.computeARegion6_9
                                                 , 8: self.computeARegion6_9
                                                 , 9: self.computeARegion6_9
                                                 , 10: self.computeARegion10
                                                 , 11: self.computeARegion11
                                                 }

        self._vec_computeMac_cm2_g = numpy.vectorize(self._computeMac_cm2_g)

    def checkXrayEnergyCloseEdgeEnergy(self, xrayEnergy_eV, edgeEnergy_eV):
        """Warning -5 eV or + 20 eV from edge energy."""
        differenceEnergy_eV = xrayEnergy_eV - edgeEnergy_eV

        if differenceEnergy_eV >= -5.0 and differenceEnergy_eV <= 20.0:
            message = "X-ray emitted (%0.1f eV) is near the energy edge (%0.1f eV) by %0.1f eV." % (xrayEnergy_eV, edgeEnergy_eV, differenceEnergy_eV)
            warnings.warn(message)

    def checkVeryLowEnergy_eV(self, energyEmitter_eV, energyLimit_eV=180.0):
        """Warning for energy below 180 eV or below 1.1*cutoff."""
        if energyEmitter_eV <= energyLimit_eV:
            message = "X-ray emitted (%0.1f eV) is very low, less than limit (%0.1f)." % (energyEmitter_eV, energyLimit_eV)
            warnings.warn(message)

    def checkEnergyBetweenM4M5Z(self, region, atomicNumber):
        """Warning for energy between M4 and M5 for elements of Z < 70."""
        if region == 9 and atomicNumber < 70:
            message = "X-ray emitted between M4 and M5 for element %i." % (atomicNumber)
            warnings.warn(message)

    def checkEnergyBelowM5(self, region):
        """Warning if the energy is below the edge M5 of the absorber."""
        if region >= 10:
            message = "X-ray emitted below M5."
            warnings.warn(message)

    def computeMac_cm2_g(self, energyEmitter_eV, atomicNumberAbsorber):
        if isinstance(energyEmitter_eV, numpy.ndarray):
            return self._vec_computeMac_cm2_g(energyEmitter_eV, atomicNumberAbsorber)
        else:
            return self._computeMac_cm2_g(energyEmitter_eV, atomicNumberAbsorber)

    def _computeMac_cm2_g(self, energyEmitter_eV, atomicNumberAbsorber):
        if energyEmitter_eV <= 0.0:
            return 1.0E6

        self.checkVeryLowEnergy_eV(energyEmitter_eV)

        region = self.getRegion(atomicNumberAbsorber, energyEmitter_eV)

        self.checkEnergyBetweenM4M5Z(region, atomicNumberAbsorber)

        C = self.coefficientC[region](atomicNumberAbsorber)

        n = self.coefficientN[region](atomicNumberAbsorber)

        atomicMass_g_mol = ElementProperties.getAtomicMass_g_mol(atomicNumberAbsorber)

        if region == 11:
            cutoff_eV = self.computeCutoff_eV(atomicNumberAbsorber)

            self.checkVeryLowEnergy_eV(energyEmitter_eV, energyLimit_eV=cutoff_eV*1.1)

            #print energyEmitter_eV, cutoff_eV

            mac_cm2_g = self.computeModel2(atomicNumberAbsorber, atomicMass_g_mol, energyEmitter_eV, C, n, cutoff_eV)

            #mac_cm2_g = self.computeModel2b(atomicNumberAbsorber, atomicMass_g_mol, energyEmitter_eV, C, n, cutoff_eV)

            if mac_cm2_g < 0.0:
                return 1.0E6

            return mac_cm2_g
        else:
            b_eV = self.coefficientB_eV[region](atomicNumberAbsorber)

            a = self.coefficientA[region](atomicNumberAbsorber)

            mac_cm2_g = self.computeModel1(atomicNumberAbsorber, atomicMass_g_mol, energyEmitter_eV, C, n, b_eV, a)

            if mac_cm2_g < 0.0:
                return 1.0E6

            return mac_cm2_g

    def computeModel1(self, atomicNumber, atomicMass_g_mol
                                        , xrayEnergy_eV
                                        , C
                                        , n
                                        , b_eV
                                        , a):
        factor1 = C*math.pow(atomicNumber, 4)/atomicMass_g_mol

        factor2 = math.pow(12397.0/xrayEnergy_eV, n)

        argExp = (-xrayEnergy_eV + b_eV)/a

        factor3 = 1.0 - math.exp(argExp)

        mac_cm2_g = factor1*factor2*factor3

        return mac_cm2_g

    def computeModel2(self, atomicNumber, atomicMass_g_mol
                                        , xrayEnergy_eV
                                        , C
                                        , n
                                        , cutoff_eV):
        factor1 = 1.02*C
        factor1 = 1.02

        factor2 = math.pow(12397.0/xrayEnergy_eV, n)

        factor3 = C*math.pow(atomicNumber, 4)/atomicMass_g_mol

        nominator = xrayEnergy_eV - cutoff_eV

        edgeEnergyN1_eV = self.xrayTransitionData.getIonizationEnergy_eV(atomicNumber, 'N1')

        denominator = edgeEnergyN1_eV - cutoff_eV

        factor4 = nominator/denominator

        mac_cm2_g = factor1*factor2*factor3*factor4

        return mac_cm2_g

    def computeModel2b(self, atomicNumber, atomicMass_g_mol
                                        , xrayEnergy_eV
                                        , C
                                        , n
                                        , cutoff_eV):

        edgeEnergyN1_eV = self.xrayTransitionData.getIonizationEnergy_eV(atomicNumber, 'N1')

        b_eV = self.coefficientB_eV[10](atomicNumber)

        a = self.coefficientA[10](atomicNumber)

        factor1 = self.computeModel1(atomicNumber, atomicMass_g_mol, edgeEnergyN1_eV, C, n, b_eV, a)

        nominator = xrayEnergy_eV - cutoff_eV

        denominator = edgeEnergyN1_eV - cutoff_eV

        factor4 = nominator/denominator

        mac_cm2_g = 1.02*factor1*factor4

        return mac_cm2_g


    def getRegion(self, atomicNumber, xrayEnergy_eV):
        # Region 1
        edgeEnergyK_eV = self.xrayTransitionData.getIonizationEnergy_eV(atomicNumber, 'K')

        self.checkXrayEnergyCloseEdgeEnergy(xrayEnergy_eV, edgeEnergyK_eV)

        if xrayEnergy_eV >= edgeEnergyK_eV:
            return 1

        # Region 2
        try:
            edgeEnergyL1_eV = self.xrayTransitionData.getIonizationEnergy_eV(atomicNumber, 'L1')
        except KeyError:
            edgeEnergyL1_eV = 0.0

        self.checkXrayEnergyCloseEdgeEnergy(xrayEnergy_eV, edgeEnergyL1_eV)

        if edgeEnergyK_eV >= xrayEnergy_eV and xrayEnergy_eV > edgeEnergyL1_eV:
            return 2

        # Region 3
        try:
            edgeEnergyL2_eV = self.xrayTransitionData.getIonizationEnergy_eV(atomicNumber, 'L2')
        except KeyError:
            edgeEnergyL2_eV = 0.0

        self.checkXrayEnergyCloseEdgeEnergy(xrayEnergy_eV, edgeEnergyL2_eV)

        if edgeEnergyL1_eV >= xrayEnergy_eV and xrayEnergy_eV > edgeEnergyL2_eV:
            return 3

        # Region 4
        try:
            edgeEnergyL3_eV = self.xrayTransitionData.getIonizationEnergy_eV(atomicNumber, 'L3')
        except KeyError:
            edgeEnergyL3_eV = 0.0

        self.checkXrayEnergyCloseEdgeEnergy(xrayEnergy_eV, edgeEnergyL3_eV)

        if edgeEnergyL2_eV >= xrayEnergy_eV and xrayEnergy_eV > edgeEnergyL3_eV:
            return 4

        # Region 5
        try:
            edgeEnergyM1_eV = self.xrayTransitionData.getIonizationEnergy_eV(atomicNumber, 'M1')
        except KeyError:
            edgeEnergyM1_eV = 0.0

        self.checkXrayEnergyCloseEdgeEnergy(xrayEnergy_eV, edgeEnergyM1_eV)

        if edgeEnergyL3_eV >= xrayEnergy_eV and xrayEnergy_eV > edgeEnergyM1_eV:
            return 5

        # Region 6
        try:
            edgeEnergyM2_eV = self.xrayTransitionData.getIonizationEnergy_eV(atomicNumber, 'M2')
        except KeyError:
            edgeEnergyM2_eV = 0.0

        self.checkXrayEnergyCloseEdgeEnergy(xrayEnergy_eV, edgeEnergyM2_eV)

        if edgeEnergyM1_eV >= xrayEnergy_eV and xrayEnergy_eV > edgeEnergyM2_eV:
            return 6

        # Region 7
        try:
            edgeEnergyM3_eV = self.xrayTransitionData.getIonizationEnergy_eV(atomicNumber, 'M3')
        except KeyError:
            edgeEnergyM3_eV = 0.0

        self.checkXrayEnergyCloseEdgeEnergy(xrayEnergy_eV, edgeEnergyM3_eV)

        if edgeEnergyM2_eV >= xrayEnergy_eV and xrayEnergy_eV > edgeEnergyM3_eV:
            return 7

        # Region 8
        try:
            edgeEnergyM4_eV = self.xrayTransitionData.getIonizationEnergy_eV(atomicNumber, 'M4')
        except KeyError:
            edgeEnergyM4_eV = 0.0

        self.checkXrayEnergyCloseEdgeEnergy(xrayEnergy_eV, edgeEnergyM4_eV)

        if edgeEnergyM3_eV >= xrayEnergy_eV and xrayEnergy_eV > edgeEnergyM4_eV:
            return 8

        # Region 9
        try:
            edgeEnergyM5_eV = self.xrayTransitionData.getIonizationEnergy_eV(atomicNumber, 'M5')
        except KeyError:
            edgeEnergyM5_eV = 0.0

        self.checkXrayEnergyCloseEdgeEnergy(xrayEnergy_eV, edgeEnergyM5_eV)

        if edgeEnergyM4_eV >= xrayEnergy_eV and xrayEnergy_eV > edgeEnergyM5_eV:
            return 9

        # Region 10
        try:
            edgeEnergyN1_eV = self.xrayTransitionData.getIonizationEnergy_eV(atomicNumber, 'N1')
        except KeyError:
            edgeEnergyN1_eV = 0.0

        self.checkXrayEnergyCloseEdgeEnergy(xrayEnergy_eV, edgeEnergyN1_eV)

        if edgeEnergyM5_eV >= xrayEnergy_eV and xrayEnergy_eV > edgeEnergyN1_eV:
            return 10

        # Region 11
        if edgeEnergyN1_eV >= xrayEnergy_eV:
            return 11

        print(atomicNumber, xrayEnergy_eV, edgeEnergyN1_eV)

    def computeCoefficient(self, atomicNumber, coefficients):
        """
        Compute the value of the coefficient C, n, a, or b:

        $C = \sum C_{i} \cdot Z^{i}$
        $n = \sum n_{i} \cdot Z^{i}$
        $a = \sum a_{i} \cdot Z^{i}$
        $b = \sum b_{i} \cdot Z^{i}$

        """
        sumCoefficient = 0.0

        for index, value in enumerate(coefficients):
            sumCoefficient += value*math.pow(atomicNumber, index)

        return sumCoefficient

    def computeCRegion1(self, atomicNumber):
        if atomicNumber < 6:
            ci = [-2.87536E-4, 1.808599E-3]

            c = self.computeCoefficient(atomicNumber, ci)

            return c
        else:
            ci = [5.253E-3, 1.33257E-3, -7.5937E-5, 1.69357E-6, -1.3975E-8]

            c = self.computeCoefficient(atomicNumber, ci)

            return c

    def computeCRegion2(self, atomicNumber):
        ci = [-9.24E-5, 1.41478E-4, -5.24999E-6, 9.85296E-8, -9.07306E-10, 3.19254E-12]

        c = self.computeCoefficient(atomicNumber, ci)

        return c

    def computeCRegion3(self, atomicNumber):
        c = self.computeCRegion2(atomicNumber)

        factor = 0.858

        return c*factor

    def computeCRegion4(self, atomicNumber):
        c = self.computeCRegion2(atomicNumber)

        term1 = 0.8933

        term2 = -atomicNumber*8.29E-3

        term3 = atomicNumber*atomicNumber*6.38E-5

        factor = term1 + term2 + term3

        return c*factor

    def computeCRegion5(self, atomicNumber):
        if atomicNumber < 30:
            ci = [1.889757E-2, -1.8517159E-3, 6.9602789E-5, -1.1641145E-6, 7.2773258E-9]

            c = self.computeCoefficient(atomicNumber, ci)

            return c
        else:
            ci = [3.0039E-3, -1.73663566E-4, 4.0424792E-6, -4.0585911E-8, 1.497763E-10]

            c = self.computeCoefficient(atomicNumber, ci)

            return c

    def computeC1(self, atomicNumber):
        c1i = [7.7708E-5, -7.83544E-6, 2.209365E-7, -1.29086E-9]

        c1 = self.computeCoefficient(atomicNumber, c1i)

        return c1

    def computeC2(self, atomicNumber):
        c2i = [1.406, 0.0162, -6.561E-4, 4.865E-6]

        c2 = self.computeCoefficient(atomicNumber, c2i)

        return c2

    def computeC3(self, atomicNumber):
        c3i = [0.584, 0.01955, -1.285E-4]

        c3 = self.computeCoefficient(atomicNumber, c3i)

        return c3

    def computeC4(self, atomicNumber):
        c4i = [1.082, 1.366E-3]

        c4 = self.computeCoefficient(atomicNumber, c4i)

        return c4

    def computeC5(self, atomicNumber):
        c5i = [1.6442, -0.0480, 4.0664E-4]

        c5 = self.computeCoefficient(atomicNumber, c5i)

        return c5

    def computeCRegion6(self, atomicNumber):
        c1 = self.computeC1(atomicNumber)

        c2 = self.computeC2(atomicNumber)

        c3 = self.computeC3(atomicNumber)

        c = c1*c2*c3

        return c

    def computeCRegion7(self, atomicNumber):
        c1 = self.computeC1(atomicNumber)

        c2 = self.computeC2(atomicNumber)

        c4 = self.computeC4(atomicNumber)

        c = c1*c2*c4

        return c

    def computeCRegion8(self, atomicNumber):
        c1 = self.computeC1(atomicNumber)

        c2 = self.computeC2(atomicNumber)

        c = c1*c2*0.95

        return c

    def computeCRegion9(self, atomicNumber):
        c1 = self.computeC1(atomicNumber)

        c2 = self.computeC2(atomicNumber)

        c5 = self.computeC5(atomicNumber)

        c = c1*c2*c5

        return c

    def computeCRegion10(self, atomicNumber):
        ci = [4.3156E-3, -1.4653E-4, 1.707073E-6, -6.69827E-9]

        c = self.computeCoefficient(atomicNumber, ci)

        return c*1.08

    def computeCRegion11(self, atomicNumber):
        c = self.computeCRegion10(atomicNumber)

        return c

    def computeCutoff_eV(self, atmicNumber):
        factor1 = 0.252*atmicNumber - 31.1812

        term1 = factor1*atmicNumber

        cutoff = term1 + 1042.0

        return cutoff

    def computeNRegion1(self, atomicNumber):
        if atomicNumber < 6:
            bi = [3.34745, 0.02652873, -0.01273815]

            b = self.computeCoefficient(atomicNumber, bi)

            return b
        else:
            bi = [3.112, -0.0121]

            b = self.computeCoefficient(atomicNumber, bi)

            return b

    def computeNRegion2_4(self, atomicNumber):
        bi = [2.7575, 1.889E-3, -4.982E-5]

        b = self.computeCoefficient(atomicNumber, bi)

        return b

    def computeNRegion5(self, atomicNumber):
        bi = [0.5385, 0.084597, -1.08246E-3, 4.4509E-6]

        b = self.computeCoefficient(atomicNumber, bi)

        return b

    def computeNRegion6_9(self, atomicNumber):
        bi = [3.0, -0.004]

        b = self.computeCoefficient(atomicNumber, bi)

        return b

    def computeNRegion10(self, atomicNumber):
        bi = [0.3736, 0.02401]

        b = self.computeCoefficient(atomicNumber, bi)

        return b

    def computeNRegion11(self, atomicNumber):
        n = self.computeNRegion10(atomicNumber)

        return n

    def computeARegion1(self, atomicNumber):
        if atomicNumber < 6:
            bi = [24.4545, 155.6055, -14.15422]

            b = self.computeCoefficient(atomicNumber, bi)

            return b
        else:
            bi = [0.0, 47.0, 6.52, -0.152624]

            b = self.computeCoefficient(atomicNumber, bi)

            return b

    def computeARegion2_4(self, atomicNumber):
        bi = [0.0, 17.8096, 0.067429, 0.01253775, -1.16286E-4]

        b = self.computeCoefficient(atomicNumber, bi)

        return b

    def computeARegion5(self, atomicNumber):
        bi = [0.0, 10.2575657, -0.822863477, 2.63199611E-2, -1.8641019E-4]

        b = self.computeCoefficient(atomicNumber, bi)

        return b

    def computeARegion6_9(self, atomicNumber):
        bi = [0.0, 4.62, -0.04]

        b = self.computeCoefficient(atomicNumber, bi)

        return b

    def computeARegion10(self, atomicNumber):
        bi = [0.0, 19.64, -0.61239, 5.39309E-3]

        b = self.computeCoefficient(atomicNumber, bi)

        return b

    def computeARegion11(self, atomicNumber):
        return self.computeARegion10(atomicNumber)

    def computeBRegion1(self, atomicNumber):
        if atomicNumber < 6:
            bi = [-103.0, 18.2]

            b = self.computeCoefficient(atomicNumber, bi)

            return b
        else:
            return 0.0

    def computeBRegion2_4(self, atomicNumber):
        return 0.0

    def computeBRegion5(self, atomicNumber):
        if atomicNumber < 61:
            bi = [0.0, 5.654, -0.536839169, 0.018972278, -1.683474E-4]

            b = self.computeCoefficient(atomicNumber, bi)

            return b
        else:
            bi = [0.0, -1232.4022, 51.114164, -0.699473097, 3.1779619E-3]

            b = self.computeCoefficient(atomicNumber, bi)

            return b

    def computeBRegion6_9(self, atomicNumber):
        bi = [2.51, -0.052, 3.78E-4]

        b = self.computeCoefficient(atomicNumber, bi)

        try:
            edgeEnergyM4_eV = self.xrayTransitionData.getIonizationEnergy_eV(atomicNumber, 'M4')
        except KeyError:
            print("No M4 energy edge for %i" % (atomicNumber))
            edgeEnergyM4_eV = 0.0

        return b*edgeEnergyM4_eV

    def computeBRegion10(self, atomicNumber):
        bi = [-113.0, 4.5]

        b = self.computeCoefficient(atomicNumber, bi)

        return b
