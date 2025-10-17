"""MOM6 Diagnostic Table Generator

A tool for creating diag_table files from MOM6's available_diags output.
Provides both interactive Jupyter notebook interface and command-line tools.
"""

from .core import Diagnostic, DiagnosticsParser, DiagTableGenerator
from .ui import DiagTableUI, create_diag_table_ui

__version__ = '0.1.0'
__author__ = 'Anthony Meza'
__all__ = [
    'Diagnostic',
    'DiagnosticsParser',
    'DiagTableGenerator',
    'DiagTableUI',
    'create_diag_table_ui'
]
