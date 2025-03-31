#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.mac.models.penelope
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`xray_mac.mac.models.penelope` module.
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
import os.path

# Third party modules.

# Local modules.

# Project modules.
from xray_mac.mac import get_current_module_path
from xray_mac.mac.models.penelope import list_files, PhotoElectric

# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    # assert False
    assert True


def test_data_file():
    data_file_path = get_current_module_path(__file__, "../../../data/penelope2018/pendbase.zip")

    assert os.path.isfile(data_file_path)


def test_list_files():
    data_file_path = get_current_module_path(__file__, "../../../data/penelope2018/pendbase.zip")
    file_names = list_files(data_file_path)

    assert "pendbase/readme.txt" in file_names

    assert "pendbase/pdfiles/pdgph03.p18" in file_names


def test_photo_electric_read_carbon():
    data_file_path = get_current_module_path(__file__, "../../../data/penelope2018/pendbase.zip")

    photo_electric = PhotoElectric()
    assert photo_electric.atomic_number == 0
    assert photo_electric.number_shells == 0
    assert photo_electric.number_grid_energies == 0
    assert len(photo_electric.shell_ids) == 0
    assert len(photo_electric.ionization_energies_eV) == 0

    assert len(photo_electric.energies_eV) == 0
    assert len(photo_electric.totals_barn) == 0
    assert len(photo_electric.partials_barn) == 0

    photo_electric.read_data(data_file_path, 6)
    assert photo_electric.atomic_number == 6
    assert photo_electric.number_shells == 1
    assert photo_electric.number_grid_energies == 211
    assert len(photo_electric.shell_ids) == 1
    assert len(photo_electric.ionization_energies_eV) == 1

    assert photo_electric.shell_ids[0] == 1
    assert photo_electric.ionization_energies_eV[0] == 2.88e2

    assert len(photo_electric.energies_eV) == 211
    assert len(photo_electric.totals_barn) == 211
    assert photo_electric.energies_eV.shape == (211,)
    assert photo_electric.totals_barn.shape == (211,)
    assert photo_electric.partials_barn.shape == (211, 1)


def test_photo_electric_read_gold():
    data_file_path = get_current_module_path(__file__, "../../../data/penelope2018/pendbase.zip")

    photo_electric = PhotoElectric()
    assert photo_electric.atomic_number == 0
    assert photo_electric.number_shells == 0
    assert photo_electric.number_grid_energies == 0
    assert len(photo_electric.shell_ids) == 0
    assert len(photo_electric.ionization_energies_eV) == 0

    assert len(photo_electric.energies_eV) == 0
    assert len(photo_electric.totals_barn) == 0
    assert len(photo_electric.partials_barn) == 0

    photo_electric.read_data(data_file_path, 79)
    assert photo_electric.atomic_number == 79
    assert photo_electric.number_shells == 16
    assert photo_electric.number_grid_energies == 450
    assert len(photo_electric.shell_ids) == 16
    assert len(photo_electric.ionization_energies_eV) == 16

    assert photo_electric.shell_ids[0] == 1
    assert photo_electric.ionization_energies_eV[0] == 8.0729e4

    assert len(photo_electric.energies_eV) == 450
    assert len(photo_electric.totals_barn) == 450
    assert photo_electric.energies_eV.shape == (450,)
    assert photo_electric.totals_barn.shape == (450,)
    assert photo_electric.partials_barn.shape == (450, 16)

    assert photo_electric.energies_eV[0] == 50.0
    assert photo_electric.energies_eV[-1] == 1.00000E+09
    assert photo_electric.totals_barn[0] == 1.92283E+07
    assert photo_electric.totals_barn[-1] == 1.08103E-03
    assert photo_electric.partials_barn[0, 0] == 0.00000E+00
    assert photo_electric.partials_barn[0, -1] == 0.00000E+00
    assert photo_electric.partials_barn[-1, 0] == 9.13454E-04
    assert photo_electric.partials_barn[-1, -1] == 4.87514E-11


def test_photo_electric_read_carbon_without_normalization():
    data_file_path = get_current_module_path(__file__, "../../../data/penelope2018/pendbase.zip")

    photo_electric = PhotoElectric()
    assert photo_electric.atomic_number == 0
    assert photo_electric.number_shells == 0
    assert photo_electric.number_grid_energies == 0
    assert len(photo_electric.shell_ids) == 0
    assert len(photo_electric.ionization_energies_eV) == 0

    assert len(photo_electric.energies_eV) == 0
    assert len(photo_electric.totals_barn) == 0
    assert len(photo_electric.partials_barn) == 0

    photo_electric.read_data(data_file_path, 6, with_normalization=False)
    assert photo_electric.atomic_number == 6
    assert photo_electric.number_shells == 1
    assert photo_electric.number_grid_energies == 210
    assert len(photo_electric.shell_ids) == 1
    assert len(photo_electric.ionization_energies_eV) == 1

    assert photo_electric.shell_ids[0] == 1
    assert photo_electric.ionization_energies_eV[0] == 2.88e2

    assert len(photo_electric.energies_eV) == 210
    assert len(photo_electric.totals_barn) == 210
    assert photo_electric.energies_eV.shape == (210,)
    assert photo_electric.totals_barn.shape == (210,)
    assert photo_electric.partials_barn.shape == (210, 1)


def test_totals_cm2_g():
    data_file_path = get_current_module_path(__file__, "../../../data/penelope2018/pendbase.zip")

    photo_electric = PhotoElectric()
    photo_electric.read_data(data_file_path, 79)
    totals_cm2_g = photo_electric.totals_cm2_g

    assert totals_cm2_g.shape == (450,)

    assert totals_cm2_g[0] == 58789.4536256206
    assert totals_cm2_g[-1] == 3.3051888650013073e-06


def test_partials_cm2_g():
    data_file_path = get_current_module_path(__file__, "../../../data/penelope2018/pendbase.zip")

    photo_electric = PhotoElectric()
    photo_electric.read_data(data_file_path, 79)
    partials_cm2_g = photo_electric.partials_cm2_g

    assert partials_cm2_g.shape == (450, 16)

    assert partials_cm2_g[0, 0] == 0.00000E+00
    assert partials_cm2_g[0, -1] == 0.00000E+00
    assert partials_cm2_g[-1, 0] == 2.7928346017140172e-06
    assert partials_cm2_g[-1, -1] == 1.4905468343452516e-13
