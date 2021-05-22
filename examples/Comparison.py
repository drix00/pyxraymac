#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: module_name
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Description
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
import os.path
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module='numpy')

# Third party modules.
import numpy
import pylab

# Local modules.
import pydtsadata.XRayTransitionData as XRayTransitionData
import pyHendrixDemersTools.Colors as Colors
import pyHendrixDemersTools.Files as Files
import pyHendrixDemersTools.Graphics as Graphics

# Project modules.
import xray.mac.models.heinrich1987 as MacHeinrich1987
import xray.mac.models.heinrich_dtsa as MacHeinrichDTSA
import xray.mac.models.henke1993 as MacHenke1993

# Globals and constants variables.
# g_output = "Thesis"
g_output = "Display"

g_extensions = [".png", ".eps"]

if g_output == 'Thesis':
    Graphics.setDefaultThesis()

if g_output == 'Display':
    Graphics.setDefaultDisplay()


def readConfiguration(configuration_file):
    """Read the configuration file and set the options."""
    # pylint: disable-msg=W0201
    config = configparser.SafeConfigParser()

    config.readfp(open(configuration_file))

    thesis_image_path = os.getcwd()

    if config.has_section("Thesis"):
        if config.has_option("Thesis", "thesis_image_path"):
            thesis_image_path = config.get("Thesis", "thesis_image_path")

            thesis_image_path = os.path.join(thesis_image_path, "LiteratureReview")

            thesis_image_path = Files.createPath(thesis_image_path)

    return thesis_image_path


def graphic_henke_heinrich(thesis_image_path):
    xray_transition_data = XRayTransitionData.XRayTransitionData("MassAbsorptionCoefficient.cfg")

    heinrich1987 = MacHeinrich1987.MacHeinrich1987(xray_transition_data)

    heinrich_dtsa = MacHeinrichDTSA.MacHeinrichDTSA(configuration_file="MassAbsorptionCoefficient.cfg")

    configuration_file = "MassAbsorptionCoefficient.cfg"

    henke1993 = MacHenke1993.MacHenke1993(configuration_file)

    atomic_number_absorber = 29

    xray_energies_eV = numpy.arange(100.0, 20.0E3, 1.0)

    macsH1987 = []
    macsHDTSA = []
    macsHenke = []

    for xrayEnergy_eV in xray_energies_eV:
        mac_cm2_g = heinrich1987.computeMac_cm2_g(xrayEnergy_eV, atomic_number_absorber)

        macsH1987.append(mac_cm2_g)

        mac_cm2_g = heinrich_dtsa.computeMac_cm2_g(xrayEnergy_eV, atomic_number_absorber)

        macsHDTSA.append(mac_cm2_g)

        mac_cm2_g = henke1993.computeMac_cm2_g(xrayEnergy_eV, atomic_number_absorber)

        macsHenke.append(mac_cm2_g)

    pylab.figure()

    colors = Colors.GrayColors(3)

    pylab.loglog(xray_energies_eV, macsH1987, color=colors.next(), label='Heinrich (1987)')

    pylab.loglog(xray_energies_eV, macsHenke, color=colors.next(), label='Henke (1993)', zorder=-1)

    pylab.legend(loc="best")

    pylab.xlim(xmax=20.0E3)

    pylab.xlabel(r"X-ray energy (eV)")

    pylab.ylabel(r"$\frac{\mu}{\rho}$ $\left(\mathrm{cm}^{2}\,\mathrm{g}^{-1}\right)$")

    if g_output == "Thesis":
        for extension in g_extensions:
            args = (atomic_number_absorber, extension)

            filename = "MassAbsorptionCoefficients_%02i%s" % args

            filepath = os.path.join(thesis_image_path, filename)

            pylab.savefig(filepath, dpi=300)


def show_graphic():
    xray_transition_data = XRayTransitionData.XRayTransitionData("MassAbsorptionCoefficient.cfg")

    heinrich1987 = MacHeinrich1987.MacHeinrich1987(xray_transition_data)

    heinrich_dtsa = MacHeinrichDTSA.MacHeinrichDTSA(configuration_file="MassAbsorptionCoefficient.cfg")

    atomic_number_absorber = 79

    xray_energies_eV = numpy.arange(1.0, 100000.0, 1.0)

    macsH1987 = []
    macsHDTSA = []

    for xrayEnergy_eV in xray_energies_eV:
        mac_cm2_g = heinrich1987.computeMac_cm2_g(xrayEnergy_eV, atomic_number_absorber)

        macsH1987.append(mac_cm2_g)

        mac_cm2_g = heinrich_dtsa.computeMac_cm2_g(xrayEnergy_eV, atomic_number_absorber)

        macsHDTSA.append(mac_cm2_g)

    pylab.clf()

    pylab.loglog(xray_energies_eV, macsH1987, xray_energies_eV, macsHDTSA)
    pylab.legend(('1987', 'DTSA'))

    pylab.figure(2)
    pylab.plot(xray_energies_eV, macsH1987, xray_energies_eV, macsHDTSA)
    pylab.legend(('1987', 'DTSA'))


def test_mac():
    atomic_numbers = [1, 6, 92, 96]
    xray_energies_keV = [0.0001, 0.001, 0.04, 0.05, 1.0, 29.0, 30.0, 31.0, 35.0]
    xray_energies_eV = [xx*1.0e3 for xx in xray_energies_keV]

    xray_transition_data = XRayTransitionData.XRayTransitionData("MassAbsorptionCoefficient.cfg")

    heinrich1987 = MacHeinrich1987.MacHeinrich1987(xray_transition_data)
    heinrichDTSA = MacHeinrichDTSA.MacHeinrichDTSA(configuration_file="MassAbsorptionCoefficient.cfg")

    configuration_file = "MassAbsorptionCoefficient.cfg"
    henke1993 = MacHenke1993.MacHenke1993(configuration_file)

    for atomic_number in atomic_numbers:
        macsH1987 = []
        macsHDTSA = []
        macsHenke = []

        for xrayEnergy_eV in xray_energies_eV:
            mac_cm2_g = heinrich1987.computeMac_cm2_g(xrayEnergy_eV, atomic_number)
            macsH1987.append(mac_cm2_g)

            mac_cm2_g = heinrichDTSA.computeMac_cm2_g(xrayEnergy_eV, atomic_number)
            macsHDTSA.append(mac_cm2_g)

            mac_cm2_g = henke1993.computeMac_cm2_g(xrayEnergy_eV, atomic_number)
            macsHenke.append(mac_cm2_g)

        pylab.figure()
        title = "Z = %i" % (atomic_number)
        pylab.title(title)

        colors = Colors.GrayColors(3)

        pylab.loglog(xray_energies_eV, macsH1987, '.', color=colors.next(), label='Heinrich (1987)')
        pylab.loglog(xray_energies_eV, macsHenke, '.', color=colors.next(), label='Henke (1993)', zorder=-1)

        pylab.legend(loc="best")
        # pylab.xlim(xmax=20.0E3)
        pylab.xlabel(r"X-ray energy (eV)")
        pylab.ylabel(r"$\frac{\mu}{\rho}$ $\left(\mathrm{cm}^{2}\,\mathrm{g}^{-1}\right)$")

    pylab.show()


def run():
    g_thesis_image_path = readConfiguration("MassAbsorptionCoefficient.cfg")

    # showGraphic()

    graphic_henke_heinrich(g_thesis_image_path)

    if g_output == "Display":
        pylab.show()


if __name__ == '__main__':  # pragma: no cover
    test_mac()
