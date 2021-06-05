#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: penelope
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Check penelope data
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

# Third party modules.
import matplotlib.pyplot as plt

# Local modules.

# Project modules.
from xray.mac.models.penelope import PhotoElectric, SHELL_NAMES
from xray.mac import get_current_module_path

# Globals and constants variables.


def plot_data2(photo_electric, photo_electric_wo_normalization, title):
    plt.figure()
    plt.title(title)
    plt.plot(photo_electric.energies_eV, photo_electric.totals_cm2_g, label="Total w N")
    plt.plot(photo_electric_wo_normalization.energies_eV, photo_electric_wo_normalization.totals_cm2_g, label="Total wo N")

    plt.xlabel("Energy (eV)")
    plt.ylabel(r"MAC $\frac{\mu}{\rho}$ (cm2/g)")
    plt.xscale("log")
    plt.yscale("log")
    plt.legend()

    for shell_id in photo_electric.shell_ids:
        plt.figure()
        label = "{} {}".format(title, SHELL_NAMES[shell_id])
        plt.title(label)
        plt.plot(photo_electric.energies_eV, photo_electric.partials_cm2_g[:, shell_id-1], label="w N")
        plt.plot(photo_electric_wo_normalization.energies_eV, photo_electric_wo_normalization.partials_cm2_g[:, shell_id-1], label="wo N")

        plt.xlabel("Energy (eV)")
        plt.ylabel(r"MAC $\frac{\mu}{\rho}$ (cm2/g)")
        plt.xscale("log")
        plt.yscale("log")
        plt.legend()


def plot_data(photo_electric, title):
    plt.figure()
    plt.title(title)

    plt.plot(photo_electric.energies_eV, photo_electric.totals_cm2_g, label="Total")
    for shell_id in photo_electric.shell_ids:
        label = "{}".format(SHELL_NAMES[shell_id])
        plt.plot(photo_electric.energies_eV, photo_electric.partials_cm2_g[:, shell_id-1], label=label)

    plt.xlabel("Energy (eV)")
    plt.ylabel(r"MAC $\frac{\mu}{\rho}$ (cm2/g)")
    plt.xscale("log")
    plt.yscale("log")
    plt.legend()


def plot_lithium(data_file_path):
    photo_electric = PhotoElectric()
    photo_electric.read_data(data_file_path, 3)
    plot_data(photo_electric, "Li")


def plot_carbon(data_file_path):
    photo_electric = PhotoElectric()
    photo_electric.read_data(data_file_path, 6)
    plot_data(photo_electric, "C")


def plot_gold(data_file_path):
    photo_electric = PhotoElectric()
    photo_electric.read_data(data_file_path, 79)
    plot_data(photo_electric, "Au")


def plot_compare_normlization(data_file_path):
    photo_electric = PhotoElectric()
    photo_electric.read_data(data_file_path, 6)

    photo_electric_wo_normalization = PhotoElectric()
    photo_electric_wo_normalization.read_data(data_file_path, 6, with_normalization=False)

    plot_data2(photo_electric, photo_electric_wo_normalization, "C")


if __name__ == '__main__':
    data_file_path = get_current_module_path(__file__, "../data/penelope2018/pendbase.zip")

    # plot_lithium(data_file_path)
    # plot_carbon(data_file_path)
    # plot_gold(data_file_path)

    plot_compare_normlization(data_file_path)

    plt.show()
