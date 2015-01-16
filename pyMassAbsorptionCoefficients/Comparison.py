#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2007 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2922 $"
__svnDate__ = "$Date: 2013-10-13 21:15:14 -0400 (Sun, 13 Oct 2013) $"
__svnId__ = "$Id: Comparison.py 2922 2013-10-14 01:15:14Z hdemers $"

# Standard library modules.
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import os.path
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module='numpy')

# Third party modules.
import numpy
import pylab

# Local modules.
import pyMassAbsorptionCoefficients.MacHeinrich1987 as MacHeinrich1987
import pyMassAbsorptionCoefficients.MacHeinrichDTSA as MacHeinrichDTSA
import pyMassAbsorptionCoefficients.MacHenke1993 as MacHenke1993
import DatabasesTools.DTSA.XRayTransitionData as XRayTransitionData
import pyHendrixDemersTools.Colors as Colors
import pyHendrixDemersTools.Files as Files
import pyHendrixDemersTools.Graphics as Graphics

# Globals and constants variables.
#g_output = "Thesis"
g_output = "Display"

g_extensions = [".png", ".eps"]

if g_output == 'Thesis':
    Graphics.setDefaultThesis()

if g_output == 'Display':
    Graphics.setDefaultDisplay()

def readConfiguration(configurationFile):
    """Read the configuration file and set the options."""
    # pylint: disable-msg=W0201
    config = configparser.SafeConfigParser()

    config.readfp(open(configurationFile))

    if config.has_section("Thesis"):
        if config.has_option("Thesis", "thesisImagePath"):
            thesisImagePath = config.get("Thesis", "thesisImagePath")

            thesisImagePath = os.path.join(thesisImagePath, "LiteratureReview")

            thesisImagePath = Files.createPath(thesisImagePath)

    return thesisImagePath

def graphicHenkeHeinrich(thesisImagePath):
    xrayTransitionData = XRayTransitionData.XRayTransitionData("MassAbsorptionCoefficient.cfg")

    heinrich1987 = MacHeinrich1987.MacHeinrich1987(xrayTransitionData)

    heinrichDTSA = MacHeinrichDTSA.MacHeinrichDTSA(configurationFile="MassAbsorptionCoefficient.cfg")

    configurationFile = "MassAbsorptionCoefficient.cfg"

    henke1993 = MacHenke1993.MacHenke1993(configurationFile)

    atomicNumberAbsorber = 29

    xrayEnergies_eV = numpy.arange(100.0, 20.0E3, 1.0)

    macsH1987 = []
    macsHDTSA = []
    macsHenke = []

    for xrayEnergy_eV in xrayEnergies_eV:
        mac_cm2_g = heinrich1987.computeMac_cm2_g(xrayEnergy_eV, atomicNumberAbsorber)

        macsH1987.append(mac_cm2_g)

        mac_cm2_g = heinrichDTSA.computeMac_cm2_g(xrayEnergy_eV, atomicNumberAbsorber)

        macsHDTSA.append(mac_cm2_g)

        mac_cm2_g = henke1993.computeMac_cm2_g(xrayEnergy_eV, atomicNumberAbsorber)

        macsHenke.append(mac_cm2_g)

    pylab.figure()

    colors = Colors.GrayColors(3)

    pylab.loglog(xrayEnergies_eV, macsH1987, color=colors.next(), label='Heinrich (1987)')

    pylab.loglog(xrayEnergies_eV, macsHenke, color=colors.next(), label='Henke (1993)', zorder=-1)

    pylab.legend(loc="best")

    pylab.xlim(xmax=20.0E3)

    pylab.xlabel(r"X-ray energy (eV)")

    pylab.ylabel(r"$\frac{\mu}{\rho}$ $\left(\mathrm{cm}^{2}\,\mathrm{g}^{-1}\right)$")

    if g_output == "Thesis":
        for extension in g_extensions:
            args = (atomicNumberAbsorber, extension)

            filename = "MassAbsorptionCoefficients_%02i%s" % args

            filepath = os.path.join(thesisImagePath, filename)

            pylab.savefig(filepath, dpi=300)

def showGraphic():
    xrayTransitionData = XRayTransitionData.XRayTransitionData("MassAbsorptionCoefficient.cfg")

    heinrich1987 = MacHeinrich1987.MacHeinrich1987(xrayTransitionData)

    heinrichDTSA = MacHeinrichDTSA.MacHeinrichDTSA(configurationFile="MassAbsorptionCoefficient.cfg")

    atomicNumberAbsorber = 79

    xrayEnergies_eV = numpy.arange(1.0, 100000.0, 1.0)

    macsH1987 = []
    macsHDTSA = []

    for xrayEnergy_eV in xrayEnergies_eV:
        mac_cm2_g = heinrich1987.computeMac_cm2_g(xrayEnergy_eV, atomicNumberAbsorber)

        macsH1987.append(mac_cm2_g)

        mac_cm2_g = heinrichDTSA.computeMac_cm2_g(xrayEnergy_eV, atomicNumberAbsorber)

        macsHDTSA.append(mac_cm2_g)

    pylab.clf()

    pylab.loglog(xrayEnergies_eV, macsH1987, xrayEnergies_eV, macsHDTSA)
    pylab.legend(('1987', 'DTSA'))

    pylab.figure(2)
    pylab.plot(xrayEnergies_eV, macsH1987, xrayEnergies_eV, macsHDTSA)
    pylab.legend(('1987', 'DTSA'))

def testMac():
    atomicNumbers = [1, 6, 92, 96]
    xrayEnergies_keV = [0.0001, 0.001, 0.04, 0.05, 1.0, 29.0, 30.0, 31.0, 35.0]
    xrayEnergies_eV = [xx*1.0e3 for xx in xrayEnergies_keV]

    xrayTransitionData = XRayTransitionData.XRayTransitionData("MassAbsorptionCoefficient.cfg")

    heinrich1987 = MacHeinrich1987.MacHeinrich1987(xrayTransitionData)
    heinrichDTSA = MacHeinrichDTSA.MacHeinrichDTSA(configurationFile="MassAbsorptionCoefficient.cfg")

    configurationFile = "MassAbsorptionCoefficient.cfg"
    henke1993 = MacHenke1993.MacHenke1993(configurationFile)

    for atomicNumber in atomicNumbers:
        macsH1987 = []
        macsHDTSA = []
        macsHenke = []

        for xrayEnergy_eV in xrayEnergies_eV:
            mac_cm2_g = heinrich1987.computeMac_cm2_g(xrayEnergy_eV, atomicNumber)
            macsH1987.append(mac_cm2_g)

            mac_cm2_g = heinrichDTSA.computeMac_cm2_g(xrayEnergy_eV, atomicNumber)
            macsHDTSA.append(mac_cm2_g)

            mac_cm2_g = henke1993.computeMac_cm2_g(xrayEnergy_eV, atomicNumber)
            macsHenke.append(mac_cm2_g)

        pylab.figure()
        title = "Z = %i" % (atomicNumber)
        pylab.title(title)

        colors = Colors.GrayColors(3)

        pylab.loglog(xrayEnergies_eV, macsH1987, '.', color=colors.next(), label='Heinrich (1987)')
        pylab.loglog(xrayEnergies_eV, macsHenke, '.', color=colors.next(), label='Henke (1993)', zorder=-1)

        pylab.legend(loc="best")
        #pylab.xlim(xmax=20.0E3)
        pylab.xlabel(r"X-ray energy (eV)")
        pylab.ylabel(r"$\frac{\mu}{\rho}$ $\left(\mathrm{cm}^{2}\,\mathrm{g}^{-1}\right)$")

    pylab.show()

def run():
    g_thesisImagePath = readConfiguration("MassAbsorptionCoefficient.cfg")

    #showGraphic()

    graphicHenkeHeinrich(g_thesisImagePath)

    if g_output == "Display":
        pylab.show()

if __name__ == '__main__': #pragma: no cover
    import pyHendrixDemersTools.Runner as Runner
    Runner.Runner().run(runFunction=testMac)
