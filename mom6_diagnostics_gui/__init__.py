"""MOM6 Diagnostics GUI - Interactive tool for creating diag_table files.

Provides three ways to configure MOM6 diagnostic outputs:
1. Interactive Jupyter UI - Visual, point-and-click selection
2. Python API - Programmatic generation for automation
3. Command-line - Scriptable CLI for batch processing

Quick Start:
    >>> from mom6_diagnostics_gui import create_diag_table_ui
    >>> ui = create_diag_table_ui()  # Uses built-in example data

Documentation: https://github.com/anthonymeza/CESM-diags-generator
"""

from .core import Diagnostic, AvailableDiagsParser, DiagTableGenerator
from .ui import DiagTableUI, create_diag_table_ui

__version__ = "0.1.0"
__author__ = "Anthony Meza"
__all__ = [
    "Diagnostic",
    "DiagnosticsParser",
    "DiagTableGenerator",
    "DiagTableUI",
    "create_diag_table_ui",
]
