#!/usr/bin/env python
"""Regression testing for the project."""

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

if __name__ == "__main__":
    import nose
    import sys
    argv = sys.argv
    argv.append("--cover-package=xray.models")
    nose.main(argv=argv)
