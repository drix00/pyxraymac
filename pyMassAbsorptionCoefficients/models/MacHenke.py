#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2007 Hendrix Demers"
__license__ = ""

# Standard library modules.
from configparser import ConfigParser
import tarfile
import os.path
import math

# Third party modules.

# Local modules.
from pyMassAbsorptionCoefficients.models.elements import ElementProperties
import pyHendrixDemersTools.Files as Files

# Globals and constants variables.
g_coefficient = [41746.75
                                 , 10512.72
                                 , 6062.27
                                 , 4669.04
                                 , 3892.17
                                 , 3503.31
                                 , 3004.14
                                 , 2629.99
                                 , 2214.83
                                 , 2085.18
                                 , 1830.3
                                 , 1731.26
                                 , 1559.52
                                 , 1498.22
                                 , 1358.51
                                 , 1312.24
                                 , 1186.88
                                 , 1053.32
                                 , 1076.22
                                 , 1049.91
                                 , 935.99
                                 , 878.83
                                 , 826.01
                                 , 809.26
                                 , 765.92
                                 , 753.46
                                 , 714
                                 , 716.92
                                 , 662.17
                                 , 643.5
                                 , 603.51
                                 , 579.51
                                 , 561.63
                                 , 532.91
                                 , 526.61
                                 , 502.13
                                 , 492.33
                                 , 480.24
                                 , 473.29
                                 , 461.26
                                 , 452.91
                                 , 438.59
                                 , 425.44
                                 , 416.33
                                 , 408.9
                                 , 395.4
                                 , 390.09
                                 , 374.32
                                 , 366.47
                                 , 354.46
                                 , 345.59
                                 , 329.77
                                 , 331.57
                                 , 320.5
                                 , 316.6
                                 , 306.41
                                 , 302.93
                                 , 300.31
                                 , 298.62
                                 , 291.72
                                 , 286.4
                                 , 279.85
                                 , 276.89
                                 , 267.59
                                 , 264.77
                                 , 258.94
                                 , 255.13
                                 , 251.57
                                 , 249.08
                                 , 243.17
                                 , 240.49
                                 , 235.75
                                 , 232.54
                                 , 228.87
                                 , 225.98
                                 , 221.23
                                 , 218.91
                                 , 215.7
                                 , 213.63
                                 , 209.77
                                 , 205.88
                                 , 203.08
                                 , 201.35
                                 , 200.39
                                 , 200.38
                                 , 189.52
                                 , 188.67
                                 , 186.16
                                 , 185.35
                                 , 181.34
                                 , 182.13
                                 , 176.78]

def getCoefficient(atomicNumber):
    index = atomicNumber - 1

    return g_coefficient[index]

def WavelenghtElectron_nm(energy_eV):
    h_Nms = 6.626E-34
    m0_kg = 9.109E-31
    e_C = 1.602E-19

    argSqrt = 2.0*m0_kg*e_C*energy_eV

    value_m = h_Nms/math.sqrt(argSqrt)

    value_nm = value_m*1.0E9

    return value_nm

def WavelenghtElectronRelativistic_nm(energy_eV):
    h_Nms = 6.626E-34
    m0_kg = 9.109E-31
    e_C = 1.602E-19
    c_m_s = 2.998E8

    factor = 2.0*m0_kg*e_C*energy_eV

    ratio = e_C*energy_eV/(2.0*m0_kg*c_m_s**2)

    term = 1.0 + ratio

    argSqrt = factor*term

    value_m = h_Nms/math.sqrt(argSqrt)

    value_nm = value_m*1.0E9

    return value_nm

def WavelenghtPhoton_nm(energy_eV):
    h_Nms = 6.626E-34
    c_m_s = 2.998E8
    e_C = 1.602E-19

    value_m = h_Nms*c_m_s/(e_C*energy_eV)

    value_nm = value_m*1.0E9

    return value_nm

class MacHenke(object):
    def __init__(self, configurationFile):
        self.readConfigurationFile(configurationFile)

    def computeCoefficient_keVcm2_g(self, atomicNumber):
        r0_m = 2.817938e-15
        h_Js = 6.62618E-34
        c_m_s = 2.99792458E8

        C_1_Jm2 = 1.0/(math.pi*r0_m*h_Js*c_m_s)

        J_eV = 1.602189E-19

        N0_atom_mol = 6.02205E23

        element_properties = ElementProperties()
        A_g_mol = element_properties.atomic_mass_g_mol(atomicNumber)

        K_atomJm2_g = 2.0*N0_atom_mol/(math.pi*C_1_Jm2*A_g_mol)

        K_keVcm2_g = K_atomJm2_g/(J_eV*1.0E3*1.0E-4)

        return K_keVcm2_g

    def readConfigurationFile(self, configurationFile):
        """ Read the configuration file for options."""
        config = ConfigParser()

        config.read_file(open(configurationFile))

        if config.has_section("MacHenke"):
            if config.has_option("MacHenke", "pathname"):
                self._pathname = config.get("MacHenke", "pathname")

            if config.has_option("MacHenke", "filename"):
                self._filename = config.get("MacHenke", "filename")

            if config.has_option("MacHenke", "resultspath"):
                self.resultspath = config.get("MacHenke", "resultspath")

    def getElements(self):
        elements = []

        gzFilename = os.path.join(self._pathname, self._filename)

        tarFile = tarfile.TarFile.gzopen(gzFilename, mode='r')

        files = tarFile.getnames()

        for file in files:
            if '.nff' in file:
                element = os.path.splitext(os.path.basename(file))[0]
                elements.append(element)

        return elements

    def readData(self, atomicNumber):
        gzFilename = os.path.join(self._pathname, self._filename)

        tarFile = tarfile.TarFile.gzopen(gzFilename, mode='r')

        files = tarFile.getnames()

        element_properties = ElementProperties()
        symbol = element_properties.symbol(atomicNumber).lower()

        filename = symbol + '.nff'

        energies_eV = []
        macs_cm2_g = []

        if filename in files:
            lines = tarFile.extractfile(filename).readlines()

            f1s = []
            f2s = []

            for line in lines[1:]:
                values = line.split(b'\t')

                energy_eV = float(values[0])

                energies_eV.append(energy_eV)

                f1s.append(float(values[1]))

                f2 = float(values[2])

                f2s.append(f2)

                mac_cm2_g = self.compute_mac_cm2_g(atomicNumber, energy_eV, f2)

                macs_cm2_g.append(mac_cm2_g)

        tarFile.close()

        return energies_eV, macs_cm2_g

    def writeMAC(self):
        Files.createPath(self.resultspath)

        elements = self.getElements()

        for element in elements:

            element_properties = ElementProperties()
            atomicNumber = element_properties.atomic_number(element)

            energies_eV, macs_cm2_g = self.readData(atomicNumber)

            assert len(energies_eV) == len(macs_cm2_g)

            filename = str(element) + ".dat"
            filename = os.path.join(self.resultspath, filename)

            macFile = open(filename, 'w')

            for index in range(len(energies_eV)):
                line = str(energies_eV[index]) + "\t" + str(macs_cm2_g[index]) + "\n"
                macFile.write(line)

            macFile.close()

    def compute_mac_cm2_g(self, atomicNumber, energy_eV, f2):

        factor = self.computeCoefficient_keVcm2_g(atomicNumber)/1.0E-3

        mac_cm2_g = f2*factor/energy_eV

        return mac_cm2_g

def run():
    macHenke = MacHenke("../../Databases.cfg")
    macHenke.writeMAC()

if __name__ == '__main__': #pragma: no cover
    run()
