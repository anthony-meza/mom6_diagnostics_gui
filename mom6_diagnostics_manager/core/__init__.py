"""Core functionality for parsing diagnostics and generating diag_table files.

Main Classes:
    Diagnostic - Dataclass for diagnostic field metadata
    DiagnosticsParser - Parse available_diags files
    DiagTableGenerator - Generate diag_table configuration files
"""

from .diagnostic_field import Diagnostic
from .diagnostics_parser import DiagnosticsParser
from .diag_table_writer import DiagTableGenerator
from . import default_values

__all__ = ['Diagnostic', 'DiagnosticsParser', 'DiagTableGenerator', 'default_values']
