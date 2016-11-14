# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2016 Hendrix Demers"
__license__ = ""

import os.path
import logging


def get_current_module_path(module_path, relative_path=""):
    base_path = os.path.dirname(module_path)
    logging.debug(base_path)

    file_path = os.path.join(base_path, relative_path)
    logging.debug(file_path)
    file_path = os.path.normpath(file_path)

    return file_path
