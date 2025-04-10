#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: xray_mac.mac
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Main package for the mass absorption coefficient Python code.
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
from pathlib import Path

# Third party modules.

# Local modules.

# Globals and constants variables.
__author__ = """Hendrix Demers"""
__email__ = 'hendrix.demers@mail.mcgill.ca'
__version__ = '0.2'
__project_name__ = "pyxraymac"


def get_current_module_path(module_path, relative_path=""):
    """
    Extract the current module path and combine it with the relative path and return it.

    :param str module_path: Pass the `__file__` python keyword for this parameter
    :param str relative_path: The relative path to combine with the module path
    :return: The path obtained when combine the module path and relative path
    :rtype: str
    """
    base_path = os.path.dirname(module_path)
    file_path = os.path.join(base_path, relative_path)
    file_path = os.path.abspath(file_path)
    file_path = os.path.normpath(file_path)

    return file_path


def create_path(root_path, path):
    new_path = Path(root_path) / Path(path)
    new_path.mkdir(parents=True, exist_ok=True)

    return new_path


def create_root_path(root_path):
    new_path = Path(root_path)
    new_path.mkdir(parents=True, exist_ok=True)

    return new_path
