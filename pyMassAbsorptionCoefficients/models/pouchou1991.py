#!/usr/bin/env python
"""
Mass absorption coefficients tables from Pouchou and Pichoir (1991).
"""

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2007 Hendrix Demers"
__license__ = ""

# Standard library modules.

# Third party modules.

# Local modules.

# Globals and constants variables.
LINE_Ka = 'Ka'
LINE_Lb = 'Lb'
LINE_La = 'La'
LINE_Mb = 'Mb'

class MacPouchou1991():
    def __init__(self):
        self.data_mac_cm2_g = {}

        self.data_mac_cm2_g[LINE_Ka] = {}

        atomic_number_emitter = 5
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter] = {}

        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][5] = 3500.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][6] = 6750.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][7] = 11000.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][8] = 16500.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][13] = 64000.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][14] = 80000.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][22] = 15000.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][23] = 18000.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][24] = 20700.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][26] = 27800.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][27] = 32000.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][28] = 37000.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][40] = 4400.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][41] = 4500.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][42] = 4600.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][57] = 2500.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][73] = 23000.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][74] = 21000.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][92] = 7400.0

        atomic_number_emitter = 6
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter] = {}

        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][5] = 39000.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][6] = 2170.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][14] = 35000.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][22] = 8100.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][23] = 8850.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][24] = 10700.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][26] = 13500.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][40] = 25000.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][41] = 24000.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][42] = 20500.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][72] = 18000.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][73] = 17000.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][74] = 18000.0

        atomic_number_emitter = 7
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter] = {}

        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][5] = 15800.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][7] = 1640.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][13] = 13800.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][14] = 17000.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][22] = 4270.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][23] = 4950.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][24] = 5650.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][26] = 7190.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][40] = 24000.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][41] = 25000.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][42] = 25800.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][72] = 14000.0
        self.data_mac_cm2_g[LINE_Ka][atomic_number_emitter][73] = 15500.0

        self.data_mac_cm2_g[LINE_Ka][14] = {}
        self.data_mac_cm2_g[LINE_Ka][14][73] = 1490.0

        self.data_mac_cm2_g[LINE_Ka][16] = {}
        self.data_mac_cm2_g[LINE_Ka][16][79] = 2200.0

        self.data_mac_cm2_g[LINE_Lb] = {}

        self.data_mac_cm2_g[LINE_Lb][29] = {}
        self.data_mac_cm2_g[LINE_Lb][29][29] = 6750.0

        self.data_mac_cm2_g[LINE_La] = {}
        self.data_mac_cm2_g[LINE_La][33] = {}
        self.data_mac_cm2_g[LINE_La][33][31] = 7000.0

        self.data_mac_cm2_g[LINE_La][42] = {}
        self.data_mac_cm2_g[LINE_La][42][79] = 2200.0

        self.data_mac_cm2_g[LINE_Mb] = {}

        self.data_mac_cm2_g[LINE_Mb][64] = {}
        self.data_mac_cm2_g[LINE_Mb][64][64] = 4700.0

        self.data_mac_cm2_g[LINE_Mb][72] = {}
        self.data_mac_cm2_g[LINE_Mb][72][72] = 3000.0

        self.data_mac_cm2_g[LINE_Mb][73] = {}
        self.data_mac_cm2_g[LINE_Mb][73][73] = 2500.0

        self.data_mac_cm2_g[LINE_Mb][74] = {}
        self.data_mac_cm2_g[LINE_Mb][74][74] = 2080.0

        self.data_mac_cm2_g[LINE_Mb][79] = {}
        self.data_mac_cm2_g[LINE_Mb][79][78] = 2550.0

        self.data_mac_cm2_g[LINE_Mb][80] = {}
        self.data_mac_cm2_g[LINE_Mb][80][79] = 2170.0

        self.data_mac_cm2_g[LINE_La][21] = {}
        self.data_mac_cm2_g[LINE_La][21][21] = 4750.0

        self.data_mac_cm2_g[LINE_La][22] = {}
        self.data_mac_cm2_g[LINE_La][22][22] = 4550.0

        self.data_mac_cm2_g[LINE_La][23] = {}
        self.data_mac_cm2_g[LINE_La][23][23] = 4370.0

        self.data_mac_cm2_g[LINE_La][24] = {}
        self.data_mac_cm2_g[LINE_La][24][24] = 3850.0

        self.data_mac_cm2_g[LINE_La][25] = {}
        self.data_mac_cm2_g[LINE_La][25][25] = 3340.0

        self.data_mac_cm2_g[LINE_La][26] = {}
        self.data_mac_cm2_g[LINE_La][26][26] = 3350.0

        self.data_mac_cm2_g[LINE_La][27] = {}
        self.data_mac_cm2_g[LINE_La][27][27] = 3260.0

        self.data_mac_cm2_g[LINE_La][28] = {}
        self.data_mac_cm2_g[LINE_La][28][28] = 3560.0

        self.data_mac_cm2_g[LINE_La][29] = {}
        self.data_mac_cm2_g[LINE_La][29][29] = 1755.0

    def is_available(self, atomic_number_absorber, atomic_number_emitter, line_emitter):
        xrayTransitionKey = self.extract_transition_key(line_emitter)

        if xrayTransitionKey    in self.data_mac_cm2_g:
            if atomic_number_emitter in self.data_mac_cm2_g[xrayTransitionKey]:
                if atomic_number_absorber in self.data_mac_cm2_g[xrayTransitionKey][atomic_number_emitter]:
                    return True

        return False

    def mac_cm2_g(self, atomic_number_absorber, atomic_number_emitter, line_emitter):
        if self.is_available(atomic_number_absorber, atomic_number_emitter, line_emitter):
            xray_transition_key = self.extract_transition_key(line_emitter)

            return self.data_mac_cm2_g[xray_transition_key][atomic_number_emitter][atomic_number_absorber]

    def extract_transition_key(self, line_emitter):
        xray_transition_keys = list(self.data_mac_cm2_g.keys())
        xray_transition_keys.sort()

        for xray_transition_key in xray_transition_keys:
            if line_emitter in xray_transition_key:
                return xray_transition_key

            if len(line_emitter) > len(xray_transition_key):
                if line_emitter[:len(xray_transition_key)] in xray_transition_key:
                    return xray_transition_key

        return line_emitter
