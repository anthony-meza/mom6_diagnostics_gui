"""Interactive Jupyter widget interface for diag_table generation.

This is the main UI orchestrator that brings together all UI components.
"""

import ipywidgets as widgets
from IPython.display import display
import time
import os

from .output_file_manager import FileManagerUI, FileConfigUI
from .diagnostic_selector import DiagnosticSelectorUI
from .table_preview import PreviewExportUI
from .widget_builders import create_text_widget, create_help_text


class DiagTableUI:
    """Interactive UI for creating MOM6 diag_table files.

    This class orchestrates all UI components and manages the overall
    user interface workflow.
    """

    def __init__(self, parser, generator):
        """Initialize the UI.

        Args:
            parser: DiagnosticsParser instance
            generator: DiagTableGenerator instance
        """
        self.parser = parser
        self.generator = generator
        self.current_file = None
        self._ui_created = False

        # UI components (initialized later)
        self.file_manager = None
        self.file_config = None
        self.diagnostic_selector = None
        self.preview_export = None

        # Main container widgets
        self.file_config_area = None
        self.diag_area = None
        self.main_container = None

    def create_ui(self):
        """Create and return the main UI.

        Returns:
            VBox containing the complete UI
        """
        # Prevent multiple UI creation
        if self._ui_created:
            return self.main_container

        self._ui_created = True

        # CASENAME configuration
        casename_widget = self._create_casename_widget()
        casename_box = widgets.VBox([
            widgets.HTML("<h3 style='margin: 0 0 10px 0; color: #495057;'>"
                        "MOM6 Diagnostic Table Generator</h3>"),
            casename_widget
        ], layout=widgets.Layout(margin='0 0 20px 0'))

        # Help text
        help_html = create_help_text(
            "<b>Quick Start:</b> 1) Set case name 2) Click a file to select it "
            "3) Choose diagnostics 4) Preview and save<br>"
            "See <a href='https://mom6.readthedocs.io/en/main/api/generated/pages/Diagnostics.html' "
            "target='_blank'>https://mom6.readthedocs.io/en/main/api/generated/pages/Diagnostics.html</a> "
            "for more info on diagnostics setup"
        )

        # Initialize UI components
        self.file_manager = FileManagerUI(
            self.generator,
            on_file_selected=self.show_file_config
        )

        self.file_config = FileConfigUI(self.generator, self.parser)

        self.preview_export = PreviewExportUI(
            self.generator,
            on_export=self._on_export_change
        )

        # File configuration and diagnostics area
        self.file_config_area = widgets.VBox([
            widgets.HTML("<i>Click a file from the list to configure it.</i>")
        ])

        self.diag_area = widgets.VBox([
            widgets.HTML("<i>Click a file from the list to add diagnostics.</i>")
        ])

        # Create tabs for configuration/selection and preview
        config_and_select_tab = self._create_config_tab()
        preview_tab = self.preview_export.get_preview_layout()

        tabs = widgets.Tab(children=[config_and_select_tab, preview_tab])
        tabs.set_title(0, 'Configure & Select')
        tabs.set_title(1, 'Preview')

        # Left panel: File management and export
        left_panel = self._create_left_panel()

        # Right panel: Tabs
        right_panel = widgets.VBox([tabs], layout=widgets.Layout(
            width='calc(100% - 360px)',
            border='1px solid #dee2e6',
            border_radius='6px',
            background_color='#ffffff'
        ))

        # Main container
        self.main_container = widgets.HBox([
            left_panel,
            right_panel
        ], layout=widgets.Layout(
            padding='20px',
            background_color='#ffffff'
        ))

        # Initialize file list and auto-select first file
        self.file_manager.update_file_list(auto_select=True)
        self.preview_export.update_export_label()

        # Complete layout
        return widgets.VBox([casename_box, help_html, self.main_container])

    def _create_casename_widget(self) -> widgets.Text:
        """Create the case name configuration widget."""
        initial_value = (
            self.generator.title.split('CESM case: ')[-1]
            if 'CESM case: ' in self.generator.title
            else 'YOUR_CASE_NAME'
        )

        casename_widget = create_text_widget(
            value=initial_value,
            placeholder='Enter CESM case name',
            description='Case Name:',
            description_width='100px'
        )

        def update_casename(change):
            self.generator.title = f"MOM6 diagnostic fields table for CESM case: {change['new']}"

        casename_widget.observe(update_casename, names='value')
        return casename_widget

    def _create_left_panel(self) -> widgets.VBox:
        """Create the left panel with file management and export."""
        file_mgmt_layout = self.file_manager.get_layout()
        export_layout = self.preview_export.get_export_layout()

        return widgets.VBox([
            file_mgmt_layout,
            widgets.HTML("<br>"),
            export_layout
        ], layout=widgets.Layout(
            width='350px',
            padding='15px',
            border='1px solid #dee2e6',
            border_radius='6px',
            background_color='#ffffff'
        ))

    def _create_config_tab(self) -> widgets.VBox:
        """Create the configuration and selection tab."""
        return widgets.VBox([
            widgets.HTML("<h4 style='color: #495057; margin: 0 0 10px 0;'>File Configuration</h4>"),
            self.file_config_area,
            widgets.HTML("<h4 style='color: #495057; margin: 15px 0 10px 0;'>Select Diagnostics</h4>"),
            self.diag_area
        ], layout=widgets.Layout(padding='10px'))

    def show_file_config(self, file_name: str):
        """Show configuration for selected file.

        Args:
            file_name: Name of file to configure
        """
        if not file_name:
            return

        self.current_file = file_name

        # Show file configuration
        config_layout = self.file_config.show_file_config(file_name)
        self.file_config_area.children = [config_layout]

        # Show diagnostic selector
        self.diagnostic_selector = DiagnosticSelectorUI(
            self.parser,
            self.generator,
            file_name,
            self.file_config.config_widgets,
            on_selection_change=self._on_selection_change
        )

        diag_layout = self.diagnostic_selector.get_layout()
        self.diag_area.children = [diag_layout]

    def _on_selection_change(self):
        """Handle diagnostic selection changes."""
        self.preview_export.update_export_label()

    def _on_export_change(self):
        """Handle export/clear operations."""
        self.file_manager.update_file_list()
        self.preview_export.update_export_label()

        # Refresh current file view if one is selected
        if self.current_file:
            self.show_file_config(self.current_file)

    def update_preview(self):
        """Update the preview display."""
        self.preview_export.show_preview()

    def update_export_label(self):
        """Update the export label."""
        self.preview_export.update_export_label()

    def clear_cache(self):
        """Clear the cache file for the loaded diagnostics.

        Returns:
            bool: True if cache was deleted, False otherwise
        """
        return self.parser.clear_cache()


def create_diag_table_ui(diag_file=None):
    """Create and display interactive UI for diag_table generation.

    Args:
        diag_file: Path to available_diags file. If None, uses the example
                   diagnostic file included with the package.

    Returns:
        DiagTableUI instance
    """
    try:
        from ..core import DiagnosticsParser, DiagTableGenerator
        from pathlib import Path

        # Use default example file if none provided
        if diag_file is None:
            package_dir = Path(__file__).parent.parent
            diag_file = str(package_dir / 'data' / 'available_diags.000000')
            print(f"Using example diagnostic file: {diag_file}")

        # Show progress bar
        progress = widgets.IntProgress(
            value=0,
            min=0,
            max=100,
            description='Loading:',
            bar_style='info',
            orientation='horizontal',
            layout=widgets.Layout(width='50%')
        )
        status_label = widgets.Label(value='Parsing diagnostics...')
        loading_box = widgets.VBox([progress, status_label])
        display(loading_box)

        # Parse diagnostics
        progress.value = 20
        start = time.time()
        parser = DiagnosticsParser(diag_file, use_cache=True)
        parse_time = time.time() - start

        total = len(parser.diagnostics)

        # Check if cache was used
        cache_file = diag_file + '.cache'
        cache_used = os.path.exists(cache_file)
        cache_status = " (from cache)" if cache_used and parse_time < 0.1 else ""

        progress.value = 60
        status_label.value = f'Loaded {total} diagnostics in {parse_time:.3f}s{cache_status}'

        # Create generator with default setup
        generator = DiagTableGenerator(
            title="MOM6 diagnostic fields table for CESM case: YOUR_CASE_NAME",
            base_year=1900
        )

        # Add default files
        _add_default_files(generator)

        progress.value = 80
        status_label.value = 'Creating UI...'

        # Create UI
        ui_start = time.time()
        ui = DiagTableUI(parser, generator)
        ui_widget = ui.create_ui()
        ui_time = time.time() - ui_start

        progress.value = 100
        status_label.value = f'Ready! (UI created in {ui_time:.2f}s)'
        progress.bar_style = 'success'

        display(ui_widget)

        # Close the progress bar
        loading_box.close()

        return ui

    except FileNotFoundError:
        print(f"ERROR: File not found: {diag_file}")
        return None
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def _add_default_files(generator):
    """Add default file configurations to generator.

    Args:
        generator: DiagTableGenerator instance
    """
    # Static file
    generator.add_file('ocean_static', -1, 'months')
    generator.add_field('ocean_model', 'deptho', 'ocean_static', 'deptho', 'all', 'none', 'none', 2)
    generator.add_field('ocean_model', 'geolon', 'ocean_static', 'geolon', 'all', 'none', 'none', 2)
    generator.add_field('ocean_model', 'geolat', 'ocean_static', 'geolat', 'all', 'none', 'none', 2)
    generator.add_field('ocean_model', 'wet', 'ocean_static', 'wet', 'all', 'none', 'none', 2)

    # High-frequency file
    generator.add_file('surf_%4yr_%3dy', 1, 'hours', new_file_freq=1, new_file_freq_units='months')
    generator.add_field('ocean_model', 'SSH', 'surf_%4yr_%3dy', 'SSH', 'all', 'none', 'none', 2)

    # Daily averages
    generator.add_file('ocean_daily', 1, 'days')
    generator.add_field('ocean_model', 'tos', 'ocean_daily', 'tos', 'all', 'mean', 'none', 2)

    # Monthly averages
    generator.add_file('ocean_month', 1, 'months')
    generator.add_field('ocean_model', 'thetao', 'ocean_month', 'thetao', 'all', 'mean', 'none', 2)

    # Annual averages
    generator.add_file('ocean_annual', 12, 'months')
    generator.add_field('ocean_model', 'thetao', 'ocean_annual', 'thetao', 'all', 'mean', 'none', 2)

    # Vertical section
    generator.add_file('ocean_Bering_Strait', 5, 'days')
    generator.add_field('ocean_model', 'thetao', 'ocean_Bering_Strait', 'thetao', 'all', 'mean',
                       '-171.4 -168.7 66.1 66.1 -1 -1', 2)
