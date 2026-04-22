"""Preview and export UI components.

This module handles the diag_table preview and export functionality.
"""

import ipywidgets as widgets
from IPython.display import clear_output, display
from .widget_builders import (
    create_button,
    create_text_widget,
    create_section_header,
    create_status_html,
    create_hbox_row,
)
from pathlib import Path


class PreviewExportUI:
    """Manages the preview and export interface."""

    def __init__(
        self,
        generator,
        on_export: callable = None,
        default_save_location="../data/diag_table",
    ):
        """Initialize preview/export UI.

        Args:
            generator: DiagTableGenerator instance
            on_export: Callback after successful export
        """
        self.generator = generator
        self.on_export = on_export

        # Create widgets
        self.preview_output = widgets.Output()
        self.export_status = widgets.Output()
        self.export_label = create_section_header(
            "Export", "(0 file(s), 0 diagnostic(s))"
        )

        # Create data directory if it doesn't exist (in parent directory)
        data_dir = Path(default_save_location).parent
        if not data_dir.exists():
            data_dir.mkdir(parents=True, exist_ok=True)

        self.output_path_widget = create_text_widget(
            value=default_save_location,
            placeholder="Path to save diag_table",
            description="Save to:",
        )

    def update_export_label(self):
        """Update export label with current counts."""
        num_files = len(self.generator.files)
        num_fields = len(self.generator.fields)
        self.export_label.value = (
            f"<b style='color: #495057;'>Export</b> "
            f"<span style='color: #6c757d; font-size: 0.9em;'>"
            f"({num_files} file(s), {num_fields} diagnostic(s))</span>"
        )

    def show_preview(self, button=None):
        """Display preview of diag_table."""
        with self.preview_output:
            clear_output(wait=True)
            try:
                # Generate content
                content = self.generator.generate()

                # Count files and fields
                num_files = len(self.generator.files)
                num_fields = len(self.generator.fields)

                # Show preview in accordion
                preview_text = widgets.Textarea(
                    value=content,
                    layout=widgets.Layout(width="100%", height="500px"),
                    disabled=True,
                )

                preview_accordion = widgets.Accordion(children=[preview_text])
                preview_accordion.set_title(
                    0, f"diag_table ({num_files} files, {num_fields} diagnostics)"
                )
                preview_accordion.selected_index = 0

                display(preview_accordion)

            except Exception as e:
                display(create_status_html(f"ERROR: {str(e)}", "error"))

    def save_diag_table(self, button=None):
        """Save diag_table to file."""
        with self.export_status:
            clear_output(wait=True)
            try:
                # Save file
                filepath = self.generator.save(self.output_path_widget.value)

                # Update status
                num_files = len(self.generator.files)
                num_fields = len(self.generator.fields)
                display(
                    create_status_html(
                        f"Saved ({num_files} file(s), {num_fields} diagnostic(s))",
                        "success",
                    )
                )

                self.update_export_label()

                if self.on_export:
                    self.on_export()

            except Exception as e:
                display(create_status_html(f"ERROR: {str(e)}", "error"))

    def clear_all(self, button=None):
        """Clear all configurations and restore defaults."""
        with self.export_status:
            clear_output(wait=True)
            self.generator.clear()

            # Restore default configuration
            self._restore_defaults()

            display(create_status_html("Configuration cleared", "success"))
            self.update_export_label()

            if self.on_export:
                self.on_export()

    def _restore_defaults(self):
        """Restore default file configurations."""
        # Static file
        self.generator.add_file("ocean_static", -1, "months")
        self.generator.add_field(
            "ocean_model", "deptho", "ocean_static", "deptho", "all", "none", "none", 2
        )
        self.generator.add_field(
            "ocean_model", "geolon", "ocean_static", "geolon", "all", "none", "none", 2
        )
        self.generator.add_field(
            "ocean_model", "geolat", "ocean_static", "geolat", "all", "none", "none", 2
        )
        self.generator.add_field(
            "ocean_model", "wet", "ocean_static", "wet", "all", "none", "none", 2
        )

        # High-frequency file
        self.generator.add_file(
            "surf_%4yr_%3dy", 1, "hours", new_file_freq=1, new_file_freq_units="months"
        )
        self.generator.add_field(
            "ocean_model", "SSH", "surf_%4yr_%3dy", "SSH", "all", "none", "none", 2
        )

        # Daily averages
        self.generator.add_file("ocean_daily", 1, "days")
        self.generator.add_field(
            "ocean_model", "tos", "ocean_daily", "tos", "all", "mean", "none", 2
        )

        # Monthly averages
        self.generator.add_file("ocean_month", 1, "months")
        self.generator.add_field(
            "ocean_model", "thetao", "ocean_month", "thetao", "all", "mean", "none", 2
        )

        # Annual averages
        self.generator.add_file("ocean_annual", 12, "months")
        self.generator.add_field(
            "ocean_model", "thetao", "ocean_annual", "thetao", "all", "mean", "none", 2
        )

        # Vertical section
        self.generator.add_file("ocean_Bering_Strait", 5, "days")
        self.generator.add_field(
            "ocean_model",
            "thetao",
            "ocean_Bering_Strait",
            "thetao",
            "all",
            "mean",
            "-171.4 -168.7 66.1 66.1 -1 -1",
            2,
        )

    def get_preview_layout(self) -> widgets.VBox:
        """Get preview tab layout.

        Returns:
            VBox containing preview widgets
        """
        preview_btn = create_button(
            "Preview diag_table",
            button_style="info",
            icon="eye",
            on_click=self.show_preview,
        )

        return widgets.VBox(
            [
                widgets.HTML(
                    "<h4 style='color: #495057; margin: 10px 0;'>Preview</h4>"
                ),
                preview_btn,
                self.preview_output,
            ],
            layout=widgets.Layout(padding="15px"),
        )

    def get_export_layout(self) -> widgets.VBox:
        """Get export controls layout.

        Returns:
            VBox containing export widgets
        """
        save_btn = create_button(
            "Save File",
            button_style="success",
            icon="save",
            width="48%",
            on_click=self.save_diag_table,
        )

        clear_btn = create_button(
            "Clear All",
            button_style="danger",
            icon="trash",
            width="48%",
            on_click=self.clear_all,
        )

        return widgets.VBox(
            [
                self.export_label,
                self.output_path_widget,
                create_hbox_row(save_btn, clear_btn),
                self.export_status,
            ]
        )
