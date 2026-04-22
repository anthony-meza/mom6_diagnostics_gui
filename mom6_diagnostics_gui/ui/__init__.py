"""User interface modules for interactive Jupyter notebook interface.

The UI components:
- main_interface: Main UI orchestrator and entry point
- widget_builders: Reusable widget components
- output_file_manager: Output file management
- diagnostic_selector: Diagnostic browsing and selection
- table_preview: Preview and export functionality
"""

from .main_interface import DiagTableUI, create_diag_table_ui
from . import widget_builders
from . import output_file_manager
from . import diagnostic_selector
from . import table_preview

__all__ = [
    "DiagTableUI",
    "create_diag_table_ui",
    "widget_builders",
    "output_file_manager",
    "diagnostic_selector",
    "table_preview",
]
