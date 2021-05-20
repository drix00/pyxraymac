#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2007 Hendrix Demers"
__license__ = ""

# Standard library modules.
import math

import xray.MacHeinrich1987 as MacHeinrich1987
import xray.mac.models.MassAbsorptionCoefficient as MassAbsorptionCoefficient
import pySpecimenTools.SampleRegion as SampleRegion
import pydtsadata.XRayTransitionData as XRayTransitionData


# Globals and constants variables.

class XRayRange(object):
    def __init__(self, configurationFile):
        xrayTransitionData = XRayTransitionData.XRayTransitionData(configurationFile)

        macEnergy = MacHeinrich1987.MacHeinrich1987(xrayTransitionData)

        self.macModel = MassAbsorptionCoefficient.MassAbsorptionCoefficient(macEnergy=macEnergy
                                                                            , xrayTransitionData=xrayTransitionData
                                                                            , configurationFile=configurationFile)

    def setSpecimen(self, specimen):
        self.specimen = specimen

    def getCharateristicAbsorptionLength_cm(self, photonEnergy_eV):
        massDensity_g_cm3 = self.specimen.computeMeanMassDensity_g_cm3()

        mac_cm2_g = self.macModel.computeMacTotal_cm2_g(self.specimen.elementList
                                                                                                        , energyEmitter_eV=photonEnergy_eV)

        meanFreePath_1_cm = mac_cm2_g*massDensity_g_cm3

        charateristicAbsorptionLength_cm = 1.0/meanFreePath_1_cm

        return charateristicAbsorptionLength_cm

    def getRangeByEnergy_nm(self, photonEnergy_eV, limit=0.01):
        mac_cm2_g = self.macModel.computeMacTotal_cm2_g(self.specimen.elementList
                                                                                                        , energyEmitter_eV=photonEnergy_eV)

        massDensity_g_cm3 = self.specimen.computeMeanMassDensity_g_cm3()

        nominator = -math.log(limit)

        denominator = mac_cm2_g*massDensity_g_cm3

        range_cm = nominator/denominator

        range_nm = range_cm*1.0E7

        return range_nm

    def getRange_nm(self, atomicNumber, line, limit=0.01):
        mac_cm2_g = self.macModel.computeMacTotal_cm2_g(self.specimen.elementList
                                                                                                        , atomicNumberEmitter=atomicNumber
                                                                                                        , lineEmitter=line)

        massDensity_g_cm3 = self.specimen.computeMeanMassDensity_g_cm3()

        nominator = -math.log(limit)

        denominator = mac_cm2_g*massDensity_g_cm3

        range_cm = nominator/denominator

        range_nm = range_cm*1.0E7

        return range_nm

def run():
    xrayRange = XRayRange("MassAbsorptionCoefficient.cfg")

    specimen = SampleRegion.SampleRegion(atomicNumber=24)

    xrayRange.setSpecimen(specimen)

    range_nm = xrayRange.getRange_nm(24, 'Ka')

    print("%0.0f nm" % range_nm)

if __name__ == '__main__': #pragma: no cover
    import pyHendrixDemersTools.Runner as Runner
    Runner.Runner().run(runFunction=run)