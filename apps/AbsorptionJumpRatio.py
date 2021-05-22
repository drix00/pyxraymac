#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: AbsorptionJumpRatio
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Compute the absorption jump ratio.
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
import configparser

# Third party modules.
import pylab

# Local modules.
import pybrunetti2004data.XRayLib_2_4 as XRayLib_2_4
import DatabasesTools.deboer1989.FluorescenceYields as FluorescenceYields

# Globals and constants variables.


class AbsorptionJumpRatio(object):
    def __init__(self, configuration_file):
        self.read_configuration_file(configuration_file)

        self.xraylib = XRayLib_2_4.XRayLib_2_4(configurationFile=configuration_file)

        self.fluorescenceYieldsModel = FluorescenceYields.FluorescenceYields(configuration_file)

        self.jumpRatioModel = self.xraylib.getAbsorptionJumpRatio

    def read_configuration_file(self, configuration_file):
        """ Read the configuration file for options."""
        # pylint: disable-msg=W0201
        config = configparser.SafeConfigParser()

        config.readfp(open(configuration_file))

#        if config.has_section("AbsorptionJumpRatio"):
#            if config.has_option("AbsorptionJumpRatio", "pathname"):
#                self.pathname = config.get("AbsorptionJumpRatio", "pathname")

    def get_absorption_jump_factor(self, atomic_number, subshell, xray_energy_eV):
        absorption_jump_factor = 0.0

        if subshell == 'K':
            absorption_jump_factor = self.compute_k_subshell_absorption_jump_factor(atomic_number, xray_energy_eV)

        if subshell == 'LI' or subshell == 'L1':
            absorption_jump_factor = self.compute_li_subshell_absorption_jump_factor(atomic_number, xray_energy_eV)

        if subshell == 'LII' or subshell == 'L2':
            absorption_jump_factor = self.compute_lii_subshell_absorption_jump_factor(atomic_number, xray_energy_eV)

        if subshell == 'LIII' or subshell == 'L3':
            absorption_jump_factor = self.compute_liii_subshell_absorption_jump_factor(atomic_number, xray_energy_eV)

        if subshell == 'MI' or subshell == 'M1':
            absorption_jump_factor = 0.0

        if subshell == 'MII' or subshell == 'M2':
            EM2_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'M2')

            if EM2_eV > 0.0:
                absorption_jump_factor = self.compute_m234_subshell_absorption_jump_factor(atomic_number, xray_energy_eV)
            else:
                absorption_jump_factor = 0.0

        if subshell == 'MIII' or subshell == 'M3':
            EM3_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'M3')

            if EM3_eV > 0.0:
                absorption_jump_factor = self.compute_m234_subshell_absorption_jump_factor(atomic_number, xray_energy_eV)
            else:
                absorption_jump_factor = 0.0

        if subshell == 'MIV' or subshell == 'M4':
            EM4_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'M4')

            if EM4_eV > 0.0:
                absorption_jump_factor = self.compute_m234_subshell_absorption_jump_factor(atomic_number, xray_energy_eV)
            else:
                absorption_jump_factor = 0.0

        if subshell == 'MV' or subshell == 'M5':
            absorption_jump_factor = self.compute_mv_subshell_absorption_jump_factor(atomic_number, xray_energy_eV)

        return absorption_jump_factor

    def compute_k_subshell_absorption_jump_factor(self, atomic_number, xray_energy_eV):
        EK_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'K')

        if xray_energy_eV >= EK_eV and EK_eV > 0.0:
            rK = self.jumpRatioModel(atomic_number, 'K')

            nominator = rK - 1.0

            denominator = rK

            factor = nominator/denominator

            return factor
        else:
            return 0.0

    def compute_li_subshell_absorption_jump_factor(self, atomic_number, xray_energy_eV):
        EL1_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'L1')

        if xray_energy_eV >= EL1_eV and EL1_eV > 0.0:
            rL1 = self.jumpRatioModel(atomic_number, 'L1')

            nominator = rL1 - 1.0

            denominator = rL1

            factor = nominator/denominator

            EK_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'K')

            if xray_energy_eV >= EK_eV and EK_eV > 0.0:
                rK = self.jumpRatioModel(atomic_number, 'K')

                JK = self.compute_k_subshell_absorption_jump_factor(atomic_number, EK_eV)

                nKL1 = self.fluorescenceYieldsModel.getNKL1(atomic_number)

                factor = factor/rK + JK*nKL1

            return factor
        else:
            return 0.0

    def compute_lii_subshell_absorption_jump_factor(self, atomic_number, xray_energy_eV):
        EL2_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'L2')

        if xray_energy_eV >= EL2_eV and EL2_eV > 0.0:
            rL2 = self.jumpRatioModel(atomic_number, 'L2')

            nominator = rL2 - 1.0

            denominator = rL2

            factor = nominator/denominator

            EL1_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'L1')

            if xray_energy_eV >= EL1_eV and EL1_eV > 0.0:
                rL1 = self.jumpRatioModel(atomic_number, 'L1')

                JL1 = self.compute_li_subshell_absorption_jump_factor(atomic_number, EL1_eV)

                f12 = self.xraylib.getCosterKronigTransitionProbability(atomic_number, 'F12')

                factor = factor/rL1 + JL1*f12

                EK_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'K')

                if xray_energy_eV >= EK_eV and EK_eV > 0.0:
                    rK = self.jumpRatioModel(atomic_number, 'K')

                    JK = self.compute_k_subshell_absorption_jump_factor(atomic_number, EK_eV)

                    nKL1 = self.fluorescenceYieldsModel.getNKL1(atomic_number)

                    nKL2 = self.fluorescenceYieldsModel.getNKL2(atomic_number)

                    factor = factor/rK + JK*(nKL2 + nKL1*f12)

            return factor
        else:
            return 0.0

    def compute_liii_subshell_absorption_jump_factor(self, atomic_number, xray_energy_eV):
        EL3_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'L3')

        if xray_energy_eV >= EL3_eV and EL3_eV > 0.0:
            rL3 = self.jumpRatioModel(atomic_number, 'L3')

            nominator = rL3 - 1.0

            denominator = rL3

            factor = nominator/denominator

            EL2_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'L2')

            if xray_energy_eV >= EL2_eV and EL2_eV > 0.0:
                rL2 = self.jumpRatioModel(atomic_number, 'L2')

                JL2 = self.compute_lii_subshell_absorption_jump_factor(atomic_number, EL2_eV)

                f23 = self.xraylib.getCosterKronigTransitionProbability(atomic_number, 'F23')

                factor = factor/rL2 + JL2*f23

                EL1_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'L1')

                if xray_energy_eV >= EL1_eV and EL1_eV > 0.0:
                    rL1 = self.jumpRatioModel(atomic_number, 'L1')

                    JL1 = self.compute_li_subshell_absorption_jump_factor(atomic_number, EL1_eV)

                    f13 = self.xraylib.getCosterKronigTransitionProbability(atomic_number, 'F13')

                    f12 = self.xraylib.getCosterKronigTransitionProbability(atomic_number, 'F12')

                    factor = factor/rL1 + JL1*(f13 + f12*f23)

                    EK_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'K')

                    if xray_energy_eV >= EK_eV and EK_eV > 0.0:
                        rK = self.jumpRatioModel(atomic_number, 'K')

                        JK = self.compute_k_subshell_absorption_jump_factor(atomic_number, EK_eV)

                        nKL1 = self.fluorescenceYieldsModel.getNKL1(atomic_number)

                        nKL2 = self.fluorescenceYieldsModel.getNKL2(atomic_number)

                        nKL3 = self.fluorescenceYieldsModel.getNKL3(atomic_number)

                        factor = factor/rK + JK*(nKL3 + nKL2*f23 + nKL1*f13)

            return factor
        else:
            return 0.0

    def compute_m234_subshell_absorption_jump_factor(self, atomic_number, xray_energy_eV):
        EM5_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'M5')

        if xray_energy_eV < EM5_eV and EM5_eV > 0.0:
            return 0.0

        EM4_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'M4')

        if xray_energy_eV < EM4_eV and EM4_eV > 0.0:
            return 0.0

        EM3_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'M3')

        if xray_energy_eV < EM3_eV and EM3_eV > 0.0:
            return 0.33

        EM2_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'M2')

        if xray_energy_eV < EM2_eV and EM2_eV > 0.0:
            return 0.29

        EM1_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'M1')

        if xray_energy_eV < EM1_eV and EM1_eV > 0.0:
            return 0.33

        EL3_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'L3')

        if xray_energy_eV < EL3_eV and EL3_eV > 0.0:
            return 0.30

        EL2_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'L2')

        if xray_energy_eV < EL2_eV and EL2_eV > 0.0:
            return 0.20

        EL1_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'L1')

        if xray_energy_eV < EL1_eV and EL1_eV > 0.0:
            return 0.54

        EK_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'K')

        if xray_energy_eV < EK_eV and EK_eV > 0.0:
            return 0.63

        if xray_energy_eV > EK_eV and EK_eV > 0.0:
            return 0.20

        return 0.0

    def compute_mv_subshell_absorption_jump_factor(self, atomic_number, xray_energy_eV):
        if atomic_number >= 57 and atomic_number <= 78:
            EM5_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'M5')

            if xray_energy_eV < EM5_eV and EM5_eV > 0.0:
                return 0.0

            EM4_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'M4')

            if xray_energy_eV < EM4_eV and EM4_eV > 0.0:
                return 0.67

            EM3_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'M3')

            if xray_energy_eV < EM3_eV and EM3_eV > 0.0:
                return 0.55

            EM2_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'M2')

            if xray_energy_eV < EM2_eV and EM2_eV > 0.0:
                return 0.59

            EM1_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'M1')

            if xray_energy_eV < EM1_eV and EM1_eV > 0.0:
                return 0.56

            EL3_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'L3')

            if xray_energy_eV < EL3_eV and EL3_eV > 0.0:
                return 0.52

            EL2_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'L2')

            if xray_energy_eV < EL2_eV and EL2_eV > 0.0:
                return 1.01

            EL1_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'L1')

            if xray_energy_eV < EL1_eV and EL1_eV > 0.0:
                return 0.86

            EK_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'K')

            if xray_energy_eV < EK_eV and EK_eV > 0.0:
                return 0.92

            if xray_energy_eV > EK_eV and EK_eV > 0.0:
                return 0.24
        elif atomic_number >= 79 and atomic_number <= 94:
            EM5_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'M5')

            if xray_energy_eV < EM5_eV and EM5_eV > 0.0:
                return 0.0

            EM4_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'M4')

            if xray_energy_eV < EM4_eV and EM4_eV > 0.0:
                return 0.56

            EM3_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'M3')

            if xray_energy_eV < EM3_eV and EM3_eV > 0.0:
                return 0.39

            EM2_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'M2')

            if xray_energy_eV < EM2_eV and EM2_eV > 0.0:
                return 0.45

            EM1_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'M1')

            if xray_energy_eV < EM1_eV and EM1_eV > 0.0:
                return 0.43

            EL3_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'L3')

            if xray_energy_eV < EL3_eV and EL3_eV > 0.0:
                return 0.40

            EL2_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'L2')

            if xray_energy_eV < EL2_eV and EL2_eV > 0.0:
                return 0.92

            EL1_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'L1')

            if xray_energy_eV < EL1_eV and EL1_eV > 0.0:
                return 0.68

            EK_eV = self.xraylib.getAbsorptionEdgeEnergy_eV(atomic_number, 'K')

            if xray_energy_eV < EK_eV and EK_eV > 0.0:
                return 0.83

            if xray_energy_eV > EK_eV and EK_eV > 0.0:
                return 0.24

        return 0.0


def run(display=False):
    absorption_jump_ratio = AbsorptionJumpRatio("AbsorptionJumpRatio.cfg")

    atomic_numbers = range(5, 95, 5)

    subshells = ['K', 'LI', 'LII', 'LIII', 'MV', 'MIV']

    factors = {}

    for subshell in subshells:
        factors.setdefault(subshell, [])

        for atomicNumber in atomic_numbers:
            xray_energy_eV = 200.0E3

            factor = absorption_jump_ratio.get_absorption_jump_factor(atomicNumber, subshell, xray_energy_eV)

            factors[subshell].append(factor)

    if display:
        pylab.clf()

        for subshell in subshells:

            pylab.plot(atomic_numbers, factors[subshell], label=subshell)

        pylab.legend(loc='best')

        pylab.xlabel('Atomic number')

        pylab.ylabel('Absorption jump factor')

        pylab.show()


if __name__ == '__main__':  # pragma: no cover
    run()
