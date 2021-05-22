#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: XRayRange
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Compute x-ray range.
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
import pySpecimenTools.SampleRegion as SampleRegion
import pydtsadata.XRayTransitionData as XRayTransitionData

# Project modules.
import xray.MacHeinrich1987 as MacHeinrich1987
import xray.mac.models.MassAbsorptionCoefficient as MassAbsorptionCoefficient

# Globals and constants variables.


class XRayRange(object):
    def __init__(self, configuration_file):
        xray_transition_data = XRayTransitionData.XRayTransitionData(configuration_file)

        mac_energy = MacHeinrich1987.MacHeinrich1987(xray_transition_data)

        self.macModel = MassAbsorptionCoefficient.MassAbsorptionCoefficient(macEnergy=mac_energy
                                                                            , xrayTransitionData=xray_transition_data
                                                                            , configurationFile=configuration_file)

    def set_specimen(self, specimen):
        self.specimen = specimen

    def get_charateristic_absorption_length_cm(self, photon_energy_eV):
        mass_density_g_cm3 = self.specimen.computeMeanMassDensity_g_cm3()

        mac_cm2_g = self.macModel.computeMacTotal_cm2_g(self.specimen.elementList, energyEmitter_eV=photon_energy_eV)

        mean_free_path_1_cm = mac_cm2_g*mass_density_g_cm3

        charateristic_absorption_length_cm = 1.0/mean_free_path_1_cm

        return charateristic_absorption_length_cm

    def get_range_by_energy_nm(self, photon_energy_eV, limit=0.01):
        mac_cm2_g = self.macModel.computeMacTotal_cm2_g(self.specimen.elementList, energyEmitter_eV=photon_energy_eV)

        mass_density_g_cm3 = self.specimen.computeMeanMassDensity_g_cm3()

        nominator = -math.log(limit)

        denominator = mac_cm2_g*mass_density_g_cm3

        range_cm = nominator/denominator

        range_nm = range_cm*1.0E7

        return range_nm

    def get_range_nm(self, atomic_number, line, limit=0.01):
        mac_cm2_g = self.macModel.computeMacTotal_cm2_g(self.specimen.elementList, atomicNumberEmitter=atomic_number,
                                                        lineEmitter=line)

        mass_density_g_cm3 = self.specimen.computeMeanMassDensity_g_cm3()

        nominator = -math.log(limit)

        denominator = mac_cm2_g*mass_density_g_cm3

        range_cm = nominator/denominator

        range_nm = range_cm*1.0E7

        return range_nm


def run():
    xray_range = XRayRange("MassAbsorptionCoefficient.cfg")

    specimen = SampleRegion.SampleRegion(atomicNumber=24)

    xray_range.set_specimen(specimen)

    range_nm = xray_range.get_range_nm(24, 'Ka')

    print("%0.0f nm" % range_nm)


if __name__ == '__main__':  # pragma: no cover
    run()
