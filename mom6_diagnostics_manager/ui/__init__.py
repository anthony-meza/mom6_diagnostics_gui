"""User interface modules for MOM6 diag_tool.

The UI is modularized into the following components:
- interactive: Main UI orchestrator
- widgets: Reusable widget builders
- file_manager: File list and configuration
- diagnostic_selector: Diagnostic browsing and selection
- preview_export: Preview and export functionality
"""

from .interactive import DiagTableUI, create_diag_table_ui
from . import widgets
from . import file_manager
from . import diagnostic_selector
from . import preview_export

__all__ = [
    'DiagTableUI',
    'create_diag_table_ui',
    'widgets',
    'file_manager',
    'diagnostic_selector',
    'preview_export'
]
