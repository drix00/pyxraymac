#!/usr/bin/env python
"""
.. py:currentmodule:: casino
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Compute mass absorption coefficient like in CASINO v2.
"""

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2012 Hendrix Demers"
__license__ = ""

# Standard library modules.
import math
import logging

# Third party modules.
import numpy as np

# Local modules.

# Project modules
from xray import get_current_module_path

# Globals and constants variables.

# Define used to related element name and atomic number.
HYDROGEN = 1
BERYLLIUM = 4
CARBON = 6
OXYGEN = 8
ALUMINUM = 13
SILICON = 14
GOLD = 79

# Define used to related element symbol and mass density.
MASS_DENSITY_H_g_cm3 = 1.0
MASS_DENSITY_BE_g_cm3 = 1.848
MASS_DENSITY_C_g_cm3 = 2.34
MASS_DENSITY_O_g_cm3 = 1.0
MASS_DENSITY_AL_g_cm3 = 2.7
MASS_DENSITY_SI_g_cm3 = 2.34
MASS_DENSITY_AU_g_cm3 = 19.3
MASS_DENSITY_H2O_g_cm3 = 1.0

# Define used to related element symbol and mass fraction.
# Mass fraction of H in parylene C6H6.
CH_C6H6 = 0.08
# Mass fraction of C in parylene C6H6.
CC = 0.92
CH_H2O = 0.1111
CO = 0.8889

NOISE_FWHM = 53.0
DETECTOR_FWHM = 1.61
HDV = 0.01

noz = 0

# Inner-shell ionisation energy (critical excitation energy) in keV.
transitions = [
[0.013598,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000],
[0.024586,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000],
[0.054748,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000],
[0.110996,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000],
[0.187994,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000],
[0.283790,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000],
[0.401586,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000],
[0.531982,0.023699,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000],
[0.685377,0.030999,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000],
[0.866871,0.044998,0.018299,0.018299,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000],
[1.072064,0.063298,0.031099,0.031099,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000],
[1.304956,0.089397,0.051398,0.051398,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000],
[1.559547,0.117696,0.073098,0.073098,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000],
[1.838838,0.148695,0.099197,0.099197,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000],
[2.145427,0.189294,0.132196,0.132196,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000],
[2.471916,0.229192,0.164794,0.132196,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000],
[2.822304,0.270191,0.201593,0.199993,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000],
[3.202791,0.319989,0.247292,0.245192,0.025299,0.000000,0.000000,0.000000,0.000000,0.000000],
[3.607278,0.377087,0.296290,0.293590,0.033899,0.000000,0.000000,0.000000,0.000000,0.000000],
[4.037963,0.437785,0.349988,0.346388,0.043699,0.025399,0.000000,0.000000,0.000000,0.000000],
[4.492648,0.500383,0.406686,0.402186,0.053798,0.032299,0.032299,0.000000,0.000000,0.000000],
[4.966231,0.563681,0.461484,0.455485,0.060298,0.034599,0.034599,0.000000,0.000000,0.000000],
[5.464915,0.628179,0.520482,0.512883,0.066498,0.037799,0.037799,0.000000,0.000000,0.000000],
[5.988997,0.694576,0.583680,0.574481,0.074097,0.042499,0.042499,0.000000,0.000000,0.000000],
[6.538778,0.768974,0.651378,0.640278,0.083897,0.048598,0.048598,0.000000,0.000000,0.000000],
[7.111759,0.846071,0.721076,0.708076,0.092897,0.053998,0.053998,0.000000,0.000000,0.000000],
[7.708639,0.925569,0.793573,0.778574,0.100697,0.059498,0.059498,0.000000,0.000000,0.000000],
[8.332519,1.008066,0.871870,0.854671,0.111796,0.068098,0.068098,0.000000,0.000000,0.000000],
[8.978596,1.096063,0.950968,0.931068,0.119796,0.073598,0.073598,0.000000,0.000000,0.000000],
[9.658273,1.193560,1.042765,1.019665,0.135895,0.086597,0.086597,0.000000,0.000000,0.000000],
[10.366749,1.297656,1.142261,1.115362,0.158095,0.106796,0.102897,0.000000,0.000000,0.000000],
[11.102724,1.414252,1.247758,1.216659,0.179994,0.127896,0.120796,0.000000,0.000000,0.000000],
[11.866297,1.526448,1.358554,1.323055,0.203493,0.146395,0.140495,0.041199,0.041199,0.000000],
[12.657371,1.653844,1.476150,1.435751,0.231492,0.168194,0.161895,0.056698,0.056698,0.000000],
[13.473244,1.781940,1.595946,1.549847,0.256491,0.189294,0.181494,0.070098,0.068998,0.027299],
[14.325114,1.920935,1.727141,1.674843,0.256491,0.222692,0.213793,0.088897,0.088897,0.023999],
[15.199184,2.065030,1.863837,1.804339,0.322089,0.247392,0.238492,0.111796,0.110296,0.029299],
[16.104053,2.216225,2.006732,1.939534,0.357488,0.279791,0.269091,0.134995,0.133095,0.037699],
[17.037823,2.372420,2.155427,2.079930,0.393587,0.312389,0.300290,0.159595,0.157395,0.045498],
[17.996990,2.531514,2.306622,2.222225,0.430285,0.344188,0.330489,0.182394,0.179994,0.051298],
[18.984957,2.697608,2.464617,2.370420,0.468384,0.378387,0.362988,0.207393,0.204593,0.058098],
[19.998823,2.865403,2.625011,2.520115,0.504583,0.409686,0.392287,0.230292,0.226992,0.061798],
[21.043287,3.042397,2.793105,2.676809,0.504583,0.444885,0.424986,0.256391,0.252891,0.061798],
[22.116451,3.223891,2.966799,2.837804,0.584980,0.482784,0.460584,0.283590,0.279391,0.074897],
[23.219114,3.411784,3.145993,3.003698,0.627079,0.520982,0.496183,0.311689,0.306990,0.080997],
[24.349474,3.604178,3.330187,3.173193,0.669877,0.559081,0.531482,0.339988,0.334689,0.086397],
[25.513136,3.805671,3.523581,3.350986,0.717476,0.602380,0.571381,0.372787,0.366688,0.095197],
[26.710295,4.017864,3.726874,3.537380,0.770174,0.650678,0.616479,0.410486,0.403686,0.107596],
[27.938953,4.237356,3.937867,3.729974,0.825572,0.702176,0.664277,0.450785,0.443085,0.121896],
[29.199110,4.464549,4.155960,3.928667,0.883770,0.756374,0.714376,0.493283,0.484784,0.136495],
[30.490168,4.698141,4.380251,4.132060,0.943668,0.811872,0.765574,0.536882,0.527482,0.151995],
[31.812721,4.939033,4.611844,4.341253,1.005966,0.869671,0.818672,0.582480,0.572081,0.168294],
[33.168274,5.187924,4.851935,4.556945,1.072064,0.930468,0.874570,0.631279,0.619379,0.186394],
[34.560230,5.452615,5.103527,4.782038,1.072064,0.998966,0.936968,0.631279,0.672277,0.186394],
[35.983379,5.714106,5.359218,5.011730,1.217059,1.064964,0.997566,0.739475,0.725475,0.230792],
[37.439331,5.988597,5.623410,5.246822,1.292756,1.136662,1.062164,0.796073,0.780674,0.252991],
[38.923279,6.266088,5.890400,5.482514,1.361254,1.204359,1.123362,0.848471,0.831672,0.270391],
[40.441631,6.548578,6.163991,5.723206,1.434551,1.272757,1.185360,0.901269,0.883270,0.289590],
[41.989178,6.834569,6.440182,5.964098,1.510949,1.337355,1.242158,0.951068,0.930968,0.304490],
[43.567421,7.125758,6.721272,6.207690,1.575247,1.402753,1.297356,0.999866,0.977667,0.315189],
[45.182468,7.427649,7.012562,6.459081,1.575247,1.471350,1.356854,1.051464,1.026865,0.315189],
[46.832615,7.736538,7.311552,6.715972,1.722742,1.540648,1.419752,1.105963,1.080163,0.345688],
[48.517357,8.051727,7.616842,6.976664,1.799939,1.613845,1.480550,1.160561,1.130862,0.360188],
[50.237400,8.375317,7.930032,7.242555,1.880736,1.688243,1.543948,1.217159,1.185160,0.375787],
[51.993935,8.707705,8.251320,7.513745,1.967433,1.767640,1.611245,1.274957,1.241158,0.397887],
[53.786678,9.045494,8.580309,7.789836,2.046731,1.841738,1.675543,1.332455,1.294856,0.416286],
[55.615818,9.393883,8.917499,8.070827,2.128228,1.922735,1.741141,1.391453,1.351354,0.435685],
[57.483555,9.750969,9.263987,8.357616,2.206425,2.005732,1.811739,1.453251,1.409252,0.449085],
[59.387592,10.115356,9.616574,8.647707,2.306722,2.089729,1.884436,1.514549,1.467650,0.471684],
[61.330223,10.486046,9.977862,8.943297,2.398019,2.172926,1.949734,1.576247,1.527748,0.487183],
[63.311657,10.870031,10.348249,9.243787,2.491116,2.263423,2.023531,1.639344,1.588446,0.506183],
[65.348587,11.270318,10.739036,9.560376,2.600812,2.365320,2.107529,1.716342,1.661644,0.538082],
[67.414116,11.681105,11.135722,9.880765,2.707908,2.468616,2.193926,1.793139,1.735041,0.565481],
[69.522644,12.099390,11.543609,10.206453,2.819504,2.574813,2.280923,1.871537,1.809139,0.594980],
[71.673973,12.526276,11.958294,10.534943,2.931601,2.681509,2.367220,1.948834,1.882836,0.624979],
[73.868294,12.967561,12.384581,10.870532,3.048397,2.792105,2.457117,2.030731,1.960034,0.654278],
[76.108421,13.418045,12.823666,11.214820,3.173592,2.908601,2.550614,2.116028,2.040331,0.690077],
[78.392143,13.879430,13.272150,11.563309,3.295888,3.026397,2.645310,2.201825,2.121528,0.721976],
[80.722168,14.352314,13.733134,11.918296,3.424784,3.147693,2.742907,2.291022,2.205625,0.758774],
[83.099487,14.838798,14.208219,12.283484,3.561479,3.278389,2.847003,2.384819,2.294822,0.800273],
[85.527504,15.346180,14.697402,12.657071,3.703974,3.415584,2.956500,2.485016,2.389219,0.845471],
[88.001518,15.860263,15.199485,13.034759,3.850570,3.554080,3.066296,2.585512,2.483916,0.893570],
[90.522842,16.386944,15.710567,13.418145,3.998965,3.696175,3.176792,2.687509,2.579513,0.938168],
[93.101845,16.938726,16.243750,13.813332,4.149260,3.853969,3.301788,2.797905,2.682909,0.995266],
[95.726654,17.492407,16.784130,14.213018,4.316854,4.007864,3.425884,2.908601,2.786606,1.041965],
[98.400665,18.048389,17.336514,14.618905,4.481848,4.158859,3.537880,3.021398,2.892302,1.096963],
[101.133575,18.638369,17.905893,15.030691,4.651842,4.326853,3.662876,3.136094,2.999798,1.152961],
[103.918381,19.236048,18.483675,15.443876,4.821836,4.489348,3.791671,3.248290,3.104795,1.208359],
[106.751686,19.839329,19.082554,15.870462,5.001831,4.655842,3.908868,3.370086,3.218891,1.268957],
[109.647186,20.471407,19.692532,16.299747,5.182125,4.830236,4.045963,3.490682,3.331887,1.329455],
[112.597588,21.103884,20.313011,16.732533,5.366718,5.000731,4.173659,3.611078,3.441684,1.387053],
[115.602188,21.756662,20.946892,17.165720,5.547812,5.182024,4.303254,3.727474,3.551579,1.440751],
[118.673981,22.426041,21.599770,17.609404,5.723006,5.366018,4.434550,3.850170,3.665676,1.500649],
[121.813866,23.096418,22.265446,18.056187,5.932699,5.541013,4.556446,3.972466,3.777972,1.558547],
[125.022758,23.772097,22.943224,18.503473,6.120292,5.710007,4.666842,4.091961,3.886768,1.617045],
[128.215652,24.459169,23.778194,18.929359,6.287787,5.894800,4.796837,4.226857,3.970866,1.642944],
[128.215652,24.459169,23.778194,18.929359,6.287787,5.894800,4.796837,4.226857,3.970866,1.642944],
[128.215652,24.459169,23.778194,18.929359,6.287787,5.894800,4.796837,4.226857,3.970866,1.642944],
[128.215652,24.459169,23.778194,18.929359,6.287787,5.894800,4.796837,4.226857,3.970866,1.642944]]

# Atomic weight in g/mol.
A = [0,1.008,4.003,6.941,9.012,10.81,12.01,14.01,16.00,19.00,20.18,
  22.99,24.31,26.98,28.09,30.97,32.06,35.45,39.95,39.10,40.08,44.96,47.90,50.94,
  52.00,54.94,55.85,58.93,58.71,63.55,65.37,69.72,72.59,74.92,78.96,79.90,83.80,
  85.47,87.62,88.91,91.22,92.91,95.94,98.91,101.1,102.9,106.4,107.9,112.4,114.8,
  118.7,121.8,127.6,126.9,131.3,132.9,137.3,138.9,140.1,140.9,144.2,145,150.4,
  152.0,157.3,158.9,160.5,164.9,167.3,168.9,173.0,175.5,180.9,183.9,186.2,190.2,
  192.2,195.1,197.0,200.6,204.4,209.0,210,210,222,223,226.0,227,232,231,238,237,
  244,243,247,247,251,254,257,257,254,257]

def SQR(a):
    return a * a

def mac_zaluzec_cm2_g(wavelength_A, atomic_number_absorbeur):
    """
    Compute mass absorption coefficient from Zaluzec model.

    Le domaine de validite a ete etendue pour 0<e<185 (meme parametre que e>=185).

    @todo Find the unit of the returned mass absorption coefficient.

    @param wavelength_A electron wavelength in Angstrom.
    @param atomic_number_absorbeur atomic number of the absorber element.
    @return mass absorption coefficient in ??.
    @retval -1.0 if the inputs are out of range of the model.
    """
    l = wavelength_A
    absorbeur = atomic_number_absorbeur

    E = 12398.1 / l # en ev
    energy = E
    c = 0.
    n = 0.
    c_abs = 0.0

    # Ne fonct. pas puisque pas de raie de plus faible energie que .183
    if ((energy < 185) and (absorbeur != 1)):
        # .. todo:: Bug in CASINO: wavelngth passed to MACSTOTAL.
        c_abs = MACSTOTAL(energy*1.0e-3, absorbeur)
        #c_abs = MACSTOTAL(l, absorbeur)
        return ((c_abs))

    if (energy > 1487 and absorbeur != 1):
        # .. todo:: Bug in CASINO: wavelngth passed to MACSTOTAL.
        c_abs = MACSTOTAL(energy*1.0e-3, absorbeur)
        #c_abs = MACSTOTAL(l, absorbeur)
        return ((c_abs))
    else:
        if (absorbeur == HYDROGEN):
            if (E > 1487):
                c_abs = SPECIAL_EQUATIONS(E / 1000.0, absorbeur)
                return ((c_abs))

            if (E > 679 and E <= 1487):
                c = 0.001472
                n = 3.359
            if (E > 395 and E <= 679):
                c = 0.001816
                n = 3.285
            if (E <= 395):
                c = 0.002138
                n = 3.231

            if (c == 0.0):
                logging.error("Erreur dans la fonction COEFF_ABS H")
                raise ValueError
            else:
                c_abs = c * math.pow((12398.1 / E), n)

            if (c_abs < 0.0):
                c_abs = 0.0

            return ((c_abs))

        if (absorbeur == BERYLLIUM):
            if (E > 679 and E <= 1487):
                c = 0.3102
                n = 3.001
            if (E > 285 and E <= 679):
                c = 0.5060
                n = 2.831
            if (E <= 285):
                c = 2.2480
                n = 2.419

            if (c == 0.0):
                logging.error("\n\nerreur dans la fonction COEFF_ABS Be")
                raise ValueError
            else:
                c_abs = c * math.pow((12398.1 / E), n)

            return ((c_abs))

        if (absorbeur == CARBON):
            if (E > 705 and E <= 1487):
                c = 1.966
                n = 2.788
            if (E > 285 and E <= 705):
                c = 4.1290
                n = 2.529
            if (E <= 285):
                c = 0.2572
                n = 2.404

            if (c == 0.0):
                logging.error("\n\nerreur dans la fonction COEFF_ABS C")
                raise ValueError
            else:
                c_abs = c * math.pow((12398.1 / E), n)

            return ((c_abs))

        if (absorbeur == OXYGEN):
            if (E > 532 and E <= 1487):
                c = 6.9980
                n = 2.573
            if (E <= 532):
                c = .4810
                n = 2.479

            if (c == 0.0):
                logging.error("\n\nerreur dans la fonction COEFF_ABS O")
                raise ValueError
            else:
                c_abs = c * math.pow((12398.1 / E), n)

            return ((c_abs))

        if (absorbeur == ALUMINUM):
            if (E > 556 and E <= 1487):
                c = 1.2860
                n = 2.712
                c_abs = c * math.pow((12398.1 / E), n)

                return ((c_abs))
            if (E <= 556):
                c_abs = -7.059e-4 * math.pow(l, 4) - 4.815e-2 * math.pow(l, 3) + 25.79 * SQR(l) - 3.644e2 * l + 1801.

                if (c_abs < 0.0):
                    c_abs = 0.0

                return ((c_abs))

            if (c_abs == 0.0):
                logging.error("\n\nerreur dans la fonction COEFF_ABS Al")
                raise ValueError

        if (absorbeur == SILICON):
            if (E > 637 and E <= 1487):
                c = 1.759
                n = 2.706
                c_abs = c * math.pow((12398.1 / E), n)

                return ((c_abs))

            if (E <= 637):
                c_abs = -0.2407 * math.pow(l, 3) + 39.83 * SQR(l) - 527. * l + 2278.
                if (c_abs < 0.0):
                    c_abs = 0.0

                return ((c_abs))

            if (c_abs == 0.0):
                logging.error("\n\nerreur dans la fonction COEFF_ABS Si")
                raise ValueError

        if (absorbeur == GOLD):
            if (E > 776 and E <= 1487):
                c = 41.17
                n = 1.906
                c_abs = c * math.pow((12398.1 / E), n)

                return ((c_abs))

            if (E <= 776):
                c_abs = -4.411e-4 * math.pow(l, 5) + 9.878e-2 * math.pow(l, 4) - 8.218 * math.pow(l, 3) + 302. * SQR(l) - 4.466e3 * l + 29660.
                if (c_abs < 0.0):
                    c_abs = 0.0

                return ((c_abs))

            if (c_abs == 0.0):
                logging.error("\n\nerreur dans la fonction COEFF_ABS Au")
                raise ValueError

    return -1.0

def SPECIAL_EQUATIONS(energy_keV, atomicNumber):
    """
    Equations used in mac_zaluzec_cm2_g.

    @param energy_keV
    @param atomicNumber
    @return macs
    """
    E = energy_keV
    z = atomicNumber
    
    l = 12.3981 / E
    if (z == 1):
        if (E <= 2.0 and E >= 1):
            macs = 3.0353 * math.pow(l, 0.01460)
            return macs

        if (E <= 3.5 and E >= 1):
            macs = 3.5 * math.pow(l, 0.05890)
            return macs

        if (E <= 4.0 and E >= 1):
            macs = 3.5 * math.pow(l, 0.07434)
            return macs

        if (E <= 6.0 and E >= 1):
            macs = 2.937 * math.pow(l, 0.27795)
            return macs

        if (E <= 9.2 and E >= 1):
            macs = 0.627 * math.pow(l, .4231)
            return macs

        if (E <= 40.0 and E >= 1):
            macs = 0.089 * math.pow(l, .44767)
            return macs

    if (z == 2):
        if (E >= 3.7 and E <= 6.0):
            macs = 3.7 * math.pow(l, .10107)
            return macs

        if (E <= 9.5):
            macs = 2.44950 * math.pow(l, .19040)
            return macs

        if (E <= 18.):
            macs = 1.1265 * math.pow(l, .21026)
            return macs

        if (E <= 40.):
            macs = 0.08672 * math.pow(l, .18714)
            return macs

    if (z == 3):
        if (E >= 5.90 and E <= 8.80):
            macs = 5.9 * math.pow(l, .18233)
            return macs

        if (E <= 12.50):
            macs = 4.17123 * math.pow(l, 0.26263)
            return macs

        if (E <= 19.20):
            macs = 1.97884 * math.pow(l, .26156)
            return macs

        if (E <= 40.):
            macs = .2920 * math.pow(l, .22601)
            return macs

    if (z == 4):
        if (E >= 8.0 and E <= 12.50):
            macs = 8. * math.pow(l, .38680)
            return macs

        if (E <= 19.80):
            macs = 5.53694 * math.pow(l, .38371)
            return macs

        if (E <= 40.):
            macs = 0.63152 * math.pow(l, .29211)
            return macs

    if (z == 5):
        if (E >= 10.2 and E <= 15.):
            macs = 10.2 * math.pow(l, .62897)
            return macs

        if (E <= 21.):
            macs = 6.84584 * math.pow(l, .49970)
            return macs

        if (E <= 31.):
            macs = 3.83941 * math.pow(l, .40524)
            return macs

        if (E >= 40.):
            macs = .63152 * math.pow(l, .29211)
            return macs

    if (z == 6):
        if (E >= 13. and E <= 21.):
            macs = 13. * math.pow(l, 1.10987)
            return macs

        if (E <= 27.5):
            macs = 9.94906 * math.pow(l, .74709)
            return macs

        if (E <= 40.):
            macs = 2.588 * math.pow(l, .40943)
            return macs

    if (z == 7):
        if (E >= 15. and E < 21.):
            macs = 15. * math.pow(l, 1.4640)
            return macs

        if (E <= 30.):
            macs = 12.96310 * math.pow(l, 1.06418)
            return macs

        if (E <= 40.):
            macs = 6.26451 * math.pow(l, .60023)
            return macs

    if (z == 8):
        if (E >= 17.2 and E <= 25.):
            macs = 17.2 * math.pow(l, 1.83450)
            return macs

        if (E <= 40.):
            macs = 13.21194 * math.pow(l, 1.07154)
            return macs

    if (z == 9):
        if (E >= 20. and E <= 28.5):
            macs = 20.0 * math.pow(l, 2.41791)
            return macs

        if (E <= 40.):
            macs = 14.85851 * math.pow(l, 1.19931)
            return macs

    if (z == 10):
        if (E >= 23. and E <= 30.):
            macs = 23. * math.pow(l, 3.28063)
            return macs

        if (E <= 40.):
            macs = 19.86943 * math.pow(l, 1.79454)
            return macs

    if (z == 11):
        if (E <= 25. and E <= 30.):
            macs = 25. * math.pow(l, 3.51621)
            return macs

        if (E <= 40.):
            macs = 22.51741 * math.pow(l, 2.05417)
            return macs

    if (z == 12):
        if (E >= 27.3 and E <= 30.):
            macs = 27.3 * math.pow(l, 3.19488)
            return macs

    if (z == 13):
        if (E >= 29.5 and E < 40.):
            macs = 29.5 * math.pow(l, 3.40890)
            return macs

    if (z == 14):
        if (E >= 32.5 and E <= 40.):
            macs = 32.5 * math.pow(l, 4.90164)
            return macs

    if (z == 15):
        if (E <= 35. and E <= 40.):
            macs = 35. * math.pow(l, 5.66476)
            return macs

    if (z == 16):
        if (E >= 37.5 and E <= 40.):
            macs = 37.5 * math.pow(l, 6.09135)
            return macs

    return 0.0

def MACS_HENKE_EBISU(energy_keV, atomicNumber):
    """
    Compute mass absorption coefficient from Henke and Ebisu (1974) model.

    Parameterization from tables in files KCOEFF.PRN and LCOEFF.PRN.

    @todo Find the unit of the returned mass absorption coefficient.

    @note Use Zaluzec model for hydrogen absorber.

    @param E energy in keV
    @param z atomic number of the absorber.
    @return mass absorption coefficient in ??.
    @retval -1.0 if energy is greater than 1.6 keV.
    @retval -1.0 if absorber is less than 3 or greater than 94.
    """
    if energy_keV <= 0.0:
        raise ValueError

    E = energy_keV
    z = atomicNumber
    
    if (z == 1):
        absp = mac_zaluzec_cm2_g(12.3981 / E, z)
        return (absp)

    if (E > 1.6):
        return (-1)

    zmin = 3
    zmax = 94
    if ((z < zmin) or (z > zmax)):
        return (-1)

    i = 0
    emin = i
    emax = i + 1
    ffitfener = 0
    nener = 14

    # Energy and there corresponding columns value in the kcoeff.prn (0) and lcoeff.prn (1) files.
    # position is a pair of (fileIndex, columnIndex).
    # Updated value to have the same energy for x-ray line and in the files.
    energie = [0.183, 0.277, 0.392, 0.452, 0.525, 0.573, 0.637, 0.677, 0.705, 0.776, 0.848, 0.852, 0.930, 1.012]
    # Original values
    # double energie[14] ={0.185, 0.281, 0.392, 0.452, 0.525, 0.573, 0.637, 0.677, 0.705, 0.776, 0.849, 0.852, 0.930, 1.012}
    position = [ [0, 1], [0, 2], [0, 3], [1, 1], [0, 4], [1, 3], [1, 4], [0, 5], [1, 5], [1, 6], [0, 6], [1, 7], [1, 8], [1, 9]]

    if ((E >= 0.183) and (E <= 1.012)):
        # Recherche de position dans les fichiers.
        condition = True
        while condition:
            emin = i
            emax = i + 1
            i += 1

            condition = ((energie[emax] < E) and (i < nener))

        ffitfener = 0
    else:
        if (E < 0.183):
            emin = 1
            emax = 2
            ffitfener = 1
        else:
            # Position par defaut si extrapolation au-dela de 1.01.
            emin = 12
            emax = 13
            ffitfener = 0

    posfmin = position[emin][0]
    posfmax = position[emax][0]
    poscmin = position[emin][1]
    poscmax = position[emax][1]
    posl = z - 2

    kcol = 6
    lcol = 9

    absmin = 0.0
    absmax = 0.0

    # for INI File
    file_path_K = get_current_module_path(__file__, "../../../data/casino/KCOEFF.PRN")
    file_path_L = get_current_module_path(__file__, "../../../data/casino/LCOEFF.PRN")

    if (posfmin == 0):
        with open(file_path_K, 'r') as kcoeff:
            lines = kcoeff.readlines()

            items = lines[posl-1].split()
            absmin = float(items[poscmin-1])
    else:
        with open(file_path_L, 'r') as lcoeff:
            lines = lcoeff.readlines()

            items = lines[posl-1].split()
            absmin = float(items[poscmin-1])

    if (posfmax == 0):
        with open(file_path_K, 'r') as kcoeff:
            lines = kcoeff.readlines()

            items = lines[posl-1].split()
            absmax = float(items[poscmax-1])
    else:
        with open(file_path_L, 'r') as lcoeff:
            lines = lcoeff.readlines()

            items = lines[posl-1].split()
            absmax = float(items[poscmax-1])

    absp = 0.0
    if (ffitfener == 0):
        absp = ((absmax - absmin) / (energie[emax] - energie[emin])) * (E - energie[emin]) + absmin
    else:
        # Fit exponentiel a faible energie.
        absp = math.exp( ((math.log(absmax) - math.log(absmin)) / (math.log(energie[emax]) - math.log(energie[emin]))) * (math.log(E) - math.log(energie[emin])) + math.log(absmin))

    return absp

def MACSTOTAL(energy_keV, atomicNumber):
    """
    Compute mass absorption coefficient by combining Leroux and Henke-Ebisu models.

    @note For energy less or equal than 1.01 keV it use Henke-Ebisu model.
    @note For energy greater than 1.01 keV it use Heinrich model.

    @todo Find the unit of the returned mass absorption coefficient.

    @param energy_keV electron energy in keV.
    @param atomicNumber atomic number of the absorber
    @return mass absorption coefficient in ??.
    """

    if (energy_keV <= 1.01):
        abst = MACS_HENKE_EBISU(energy_keV, atomicNumber)
    else:
        abst = MACS_HEINRICH(12.3981 / energy_keV, atomicNumber)

    return abst


def MACS_HEINRICH(wavelength_A, atomicNumberAbsorbeur):
    """
    Compute mass absorption coefficient from Heinrich model.

    @todo Find the unit of the returned mass absorption coefficient.

    @param wavelength_A electron wavelength in Angstrom.
    @param atomicNumberAbsorbeur
    @return mass absorption coefficient in ??.
    """
    l = wavelength_A

    z = atomicNumberAbsorbeur
    atomicNumber = atomicNumberAbsorbeur

    CTOTAL = 0

    ntot = 0

    atot = 0

    btot = 0
    bmult = 1
    cmult = 1

    Ec = np.zeros(10)
    n = np.zeros(4)
    a = np.zeros(5)
    b = np.zeros(5)
    Ctot = np.zeros(6)
    C = np.zeros((6,7))

    for i in range(10):
        Ec[i] = transitions[atomicNumber - 1][i]

    E = 12.3981 / l

    if (E > Ec[0]):
        if (atomicNumber < 6):
            C[0][0] = -2.87536e-4
            C[0][1] = 1.808599e-3
            C[0][2] = 0
            C[0][3] = 0
            C[0][4] = 0
            C[0][5] = 0

            n[0] = 3.34745
            n[1] = 0.02652873
            n[2] = -0.01273815
            n[3] = 0

            a[0] = 24.4545
            a[1] = 155.6055
            a[2] = -14.15422
            a[3] = 0
            a[4] = 0

            b[0] = -103.0
            b[1] = -18.2
            b[2] = 0
            b[3] = 0
            b[4] = 0

        if (atomicNumber > 5):
            C[0][0] = 5.253e-3
            C[0][1] = 1.33257e-3
            C[0][2] = -7.5937e-5
            C[0][3] = 1.69357e-6
            C[0][4] = -1.3975e-8
            C[0][5] = 0

            n[0] = 3.112
            n[1] = -0.0121
            n[2] = 0
            n[3] = 0

            a[0] = 0
            a[1] = 47.0
            a[2] = 6.52
            a[3] = -0.152624
            a[4] = 0

            b[0] = 0
            b[1] = 0
            b[2] = 0
            b[3] = 0
            b[4] = 0

    if ((E < Ec[0]) and (E > Ec[3])):
        C[0][0] = -9.24e-5
        C[0][1] = 1.41478e-4
        C[0][2] = -5.24999e-6
        C[0][3] = 9.85296e-8
        C[0][4] = -9.07306e-10
        C[0][5] = 3.19254e-12

        n[0] = 2.7575
        n[1] = 1.889e-3
        n[2] = -4.982e-5
        n[3] = 0

        a[0] = 0
        a[1] = 17.8096
        a[2] = 0.067429
        a[3] = 0.01253775
        a[4] = -1.16286e-4

        b[0] = 0
        b[1] = 0
        b[2] = 0
        b[3] = 0
        b[4] = 0

        if ((E < Ec[0]) and (E > Ec[1])):
            cmult = 1
        if ((E < Ec[1]) and (E > Ec[2])):
            cmult = 0.858
        if ((E < Ec[2]) and (E > Ec[3])):
            cmult = (0.8933 - z * 8.29e-3 + math.pow(z, 2) * 6.38e-5)

    if ((E < Ec[3]) and (E > Ec[4])):
        if (atomicNumber < 30):
            C[0][0] = 1.889757e-2
            C[0][1] = -1.8517159e-3
            C[0][2] = 6.9602789e-5
            C[0][3] = -1.1641145e-6
            C[0][4] = 7.2773258e-9
            C[0][5] = 0

        if (atomicNumber > 29):
            C[0][0] = 3.0039e-3
            C[0][1] = -1.73663566e-4
            C[0][2] = 4.0424792e-6
            C[0][3] = -4.0585911e-8
            C[0][4] = 1.497763e-10
            C[0][5] = 0

        n[0] = 0.5385
        n[1] = 0.084597
        n[2] = -1.08246e-3
        n[3] = 4.4509e-6

        a[0] = 0
        a[1] = 10.2575657
        a[2] = -0.822863477
        a[3] = 2.63199611e-2
        a[4] = -1.8641019e-4

        if (atomicNumber < 61):
            b[0] = 0
            b[1] = 5.654
            b[2] = -0.536839169
            b[3] = 0.018972278
            b[4] = -1.683474e-4

        if (atomicNumber > 60):
            b[0] = 0
            b[1] = -1232.4022
            b[2] = 51.114164
            b[3] = -0.699473097
            b[4] = 3.1779619e-3

    if ((E < Ec[4]) and (E > Ec[8])):
        C[0][0] = 7.7708e-5
        C[0][1] = -7.83544e-6
        C[0][2] = 2.209365e-7
        C[0][3] = -1.29086e-9
        C[0][4] = 0
        C[0][5] = 0

        C[1][0] = 1.406
        C[1][1] = 0.0162
        C[1][2] = -6.561e-4
        C[1][3] = 4.865e-6
        C[1][4] = 0
        C[1][5] = 0

        C[2][0] = 0.584
        C[2][1] = 0.01955
        C[2][2] = -1.285e-4
        C[2][3] = 0
        C[2][4] = 0
        C[2][5] = 0

        C[3][0] = 1.082
        C[3][1] = 1.366e-3
        C[3][2] = 0
        C[3][3] = 0
        C[3][4] = 0
        C[3][5] = 0

        C[4][0] = 1.6442
        C[4][1] = -0.0480
        C[4][2] = 4.0664e-4
        C[4][3] = 0
        C[4][4] = 0
        C[4][5] = 0

        n[0] = 3.0
        n[1] = -0.004
        n[2] = 0
        n[3] = 0

        a[0] = 0
        a[1] = 4.62
        a[2] = -0.04
        a[3] = 0
        a[4] = 0

        b[0] = 2.51
        b[1] = -0.052
        b[2] = 3.78e-4
        b[3] = 0
        b[4] = 0

        bmult = Ec[7]

    if ((E < Ec[8]) and (E > Ec[9])):
        C[0][0] = 4.3156e-3
        C[0][1] = -1.4653e-4
        C[0][2] = 1.707073e-6
        C[0][3] = -6.69827e-9
        C[0][4] = 0
        C[0][5] = 0

        cmult = 1.08

        n[0] = 0.3736
        n[1] = 0.02401
        n[2] = 0
        n[3] = 0

        a[0] = 0
        a[1] = 19.64
        a[2] = -0.61239
        a[3] = 5.39309e-3
        a[4] = 0

        b[0] = -113.0
        b[1] = 4.5
        b[2] = 0
        b[3] = 0
        b[4] = 0

    if (E < Ec[9]):
        cutoff = (0.252 * z - 31.1812) * z + 1042

        C[0][0] = 4.3156e-3
        C[0][1] = -1.4653e-4
        C[0][2] = 1.707073e-6
        C[0][3] = -6.69827e-9
        C[0][4] = 0
        C[0][5] = 0

        cmult = 1.08

        a[0] = 0
        a[1] = 19.64
        a[2] = -0.61239
        a[3] = 5.39309e-3
        a[4] = 0


    for i in range(5):
        for j in range(6):
            Ctot[i] += cmult * C[i][j] * math.pow(z, j)
    for i in range(4):
        ntot += n[i] * math.pow(z, i)
    for i in range(5):
        atot += a[i] * math.pow(z, i)
    for i in range(5):
        btot += bmult * b[i] * math.pow(z, i)

    if ((E < Ec[4]) and (E > Ec[5])):
        CTOTAL = Ctot[0] * Ctot[1] * Ctot[2]
    elif ((E < Ec[5]) and (E > Ec[6])):
        CTOTAL = Ctot[0] * Ctot[1] * Ctot[3]
    elif ((E < Ec[6]) and (E > Ec[7])):
        CTOTAL = 0.95 * Ctot[0] * Ctot[1]
    elif ((E < Ec[7]) and (E > Ec[8])):
        CTOTAL = Ctot[0] * Ctot[1] * Ctot[4]
    else:
        CTOTAL = Ctot[0]

    MACSH = CTOTAL * math.pow(z, 4) / A[atomicNumber] * math.pow((12.397 / E), ntot) * (1 - math.exp((-E * 1000 + btot) / atot))

    if (E < Ec[9]):
        MACSH = 1.02 * CTOTAL * math.pow((12.397 / E), ntot) * CTOTAL * math.pow(z, 4) / A[atomicNumber] * ((E * 1000 - cutoff) / (Ec[9] - cutoff))

    return MACSH

def EFFICACITE(energy_keV):
    """
    Compute x-ray detector collection efficiency.

    If energy is less than 7 keV, include absorption from:
    - Al layer
    - Formvar layer
    - Au layer
    - Si dead layer
    - Be window
    - Carbon contamination layer
    - Ice contamination layer

    If energy is greater than 15 keV, include the effect of Si thickness.

    If energy is between 7 and 15 keV, efficiency is one.

    If energy is less than 0.03 keV, the efficiency is zero.

    @param energy_keV x-ray energy in keV.
    @return fraction of detected x-ray.
    """

    # detector parameters.
    parameters = {}
    # Aluminium.
    parameters[1] = 120e-7
    # Parylene.
    parameters[2] = 130e-7
    # Au.
    parameters[3] = 0.0
    # Couche morte de Si.
    parameters[4] = 50e-7
    # Berrylium.
    parameters[5] = 0.0
    # Carbone.
    parameters[6] = 0.0
    # Glace H2O.
    parameters[7] = 0.0
    # Cristal.
    parameters[8] = 0.3

    l = 12.3981 / energy_keV

    if energy_keV < 7.0:
        if energy_keV > 0.03:
            if (parameters[1] != 0.0):
                AAL = mac_zaluzec_cm2_g(l, 13) * MASS_DENSITY_AL_g_cm3 * parameters[1]
            else:
                AAL = 0

            # APA=(CH_C6H6*mac_zaluzec_cm2_g(l,1)+CC*mac_zaluzec_cm2_g(l,6))*D_C*a[2]

            if parameters[2] != 0.0:
               AFORMVAR = (0.0707 * mac_zaluzec_cm2_g(l, 1)
                           + 0.6063 * mac_zaluzec_cm2_g(l, 6)
                           + 0.3231 * mac_zaluzec_cm2_g(l, 8)) * MASS_DENSITY_C_g_cm3 * parameters[2]
            else:
               AFORMVAR = 0

            if parameters[3] != 0.0:
               AAU = mac_zaluzec_cm2_g(l, 79) * MASS_DENSITY_AU_g_cm3 * parameters[3]
            else:
               AAU = 0

            if parameters[4] != 0.0:
               ASID = mac_zaluzec_cm2_g(l, 14) * MASS_DENSITY_SI_g_cm3 * parameters[4]
            else:
               ASID = 0

            if parameters[5] != 0.0:
               ABE = mac_zaluzec_cm2_g(l, 4) * MASS_DENSITY_BE_g_cm3 * parameters[5]
            else:
               ABE = 0

            if parameters[6] != 0.0:
               AC = mac_zaluzec_cm2_g(l, 6) * MASS_DENSITY_C_g_cm3 * parameters[6]
            else:
               AC = 0

            if parameters[7] != 0.0:
               AH2O = (CH_H2O * mac_zaluzec_cm2_g(l, 1) + CO * mac_zaluzec_cm2_g(l, 8)) * MASS_DENSITY_H2O_g_cm3 * parameters[7]
            else:
               AH2O = 0

            eff = math.exp(-AH2O - AAL - AFORMVAR - AAU - ASID - ABE - AC)
            return eff
        else:
            return 0.0

    if energy_keV > 15.0:
        TSI = parameters[8]
        ASI = MACSTOTAL(12.3981 / l, 14) * MASS_DENSITY_SI_g_cm3 * TSI
        eff = (1.0 - math.exp(-ASI))

        return eff

    if energy_keV > 7.0 and energy_keV < 10.0:
        return 1.0

    return 1.0

if __name__ == '__main__': #pragma: no cover
    import matplotlib.pyplot as plt

    energies_keV = np.linspace(0.001, 30.0, 500)

    plt.figure()
    efficiencies = [EFFICACITE(energy_keV) for energy_keV in energies_keV]
    plt.plot(energies_keV, efficiencies)
    #plt.xlim((0.2, 1.6))
    plt.close()

    energies_keV = np.linspace(0.1, 30.0, 500)
    plt.figure()
    for atomic_number in [1, 6, 8, 13, 14, 79]:
        macs_cm2_g = [mac_zaluzec_cm2_g(12.3981 / energy_keV, atomic_number) for energy_keV in energies_keV]
        plt.semilogy(energies_keV, macs_cm2_g, label=atomic_number)
    plt.legend()
    plt.close()

    energies_keV = np.linspace(0.01, 2.0, 100)
    plt.figure()
    atomic_number = 6
    macs_cm2_g = [mac_zaluzec_cm2_g(12.3981 / energy_keV, atomic_number) for energy_keV in energies_keV]
    plt.semilogy(energies_keV, macs_cm2_g, label="Zaluzec")
    macs_cm2_g = [MACS_HEINRICH(12.3981 / energy_keV, atomic_number) for energy_keV in energies_keV]
    plt.semilogy(energies_keV, macs_cm2_g, label="Heinrich")
    macs_cm2_g = [MACS_HENKE_EBISU(energy_keV, atomic_number) for energy_keV in energies_keV]
    plt.semilogy(energies_keV, macs_cm2_g, label="Henke")
    macs_cm2_g = [MACSTOTAL(energy_keV, atomic_number) for energy_keV in energies_keV]
    plt.semilogy(energies_keV, macs_cm2_g, '.', label="Total")

    plt.legend()

    plt.show()
