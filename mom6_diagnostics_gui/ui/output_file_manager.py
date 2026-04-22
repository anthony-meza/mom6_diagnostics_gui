"""File management UI components for the MOM6 diagnostic tool.

This module handles the file list, file addition/removal, and file
configuration widgets.
"""

import ipywidgets as widgets
from IPython.display import clear_output
from typing import Callable, Optional
from .widget_builders import (
    create_button,
    create_text_widget,
    create_dropdown,
    create_number_input,
    create_section_header,
    create_status_html,
    create_hbox_row,
    create_float_input,
)


class FileManagerUI:
    """Manages the file list and file configuration UI."""

    def __init__(self, generator, on_file_selected: Optional[Callable] = None):
        """Initialize file manager UI.

        Args:
            generator: DiagTableGenerator instance
            on_file_selected: Callback when a file is selected
        """
        self.generator = generator
        self.on_file_selected = on_file_selected

        # Create widgets
        self.file_selector = self._create_file_selector()
        self.add_file_widgets = self._create_add_file_widgets()
        self.file_buttons = self._create_file_buttons()

    def _create_file_selector(self) -> widgets.Select:
        """Create the file list selector."""
        file_selector = widgets.Select(
            options=[],
            description="",
            layout=widgets.Layout(
                width="100%",
                height="160px",
                border="1px solid #ced4da",
                border_radius="4px",
            ),
            style={"description_width": "0px"},
        )

        if self.on_file_selected:
            file_selector.observe(
                lambda change: (
                    self.on_file_selected(change["new"]) if change["new"] else None
                ),
                names="value",
            )

        return file_selector

    def _create_file_buttons(self) -> widgets.HBox:
        """Create add/remove file buttons."""
        add_btn = create_button(
            "Add File",
            button_style="success",
            icon="plus",
            width="48%",
            on_click=self._on_add_file,
        )

        remove_btn = create_button(
            "Remove",
            button_style="danger",
            icon="trash",
            width="48%",
            on_click=self._on_remove_file,
        )

        return widgets.HBox([add_btn, remove_btn])

    def _create_add_file_widgets(self) -> dict:
        """Create widgets for adding new files."""
        widgets_dict = {
            "header": create_section_header("Add New File"),
            "name": create_text_widget(
                placeholder="e.g., ocean_daily%4yr-%2mo",
                description="Name:",
                description_width="60px",
            ),
            "output": widgets.Output(),
        }
        return widgets_dict

    def _on_add_file(self, button):
        """Handle add file button click."""
        with self.add_file_widgets["output"]:
            clear_output(wait=True)
            name = self.add_file_widgets["name"].value

            if not name:
                display(create_status_html("Please enter a file name", "error"))
                return

            try:
                # Add file with defaults
                self.generator.add_file(name, 1, "days")
                display(
                    create_status_html(
                        f"Added {name} (configure freq/units in File Configuration)",
                        "success",
                    )
                )
                self.add_file_widgets["name"].value = ""
                self.update_file_list()
            except Exception as e:
                display(create_status_html(f"ERROR: {str(e)}", "error"))

    def _on_remove_file(self, button):
        """Handle remove file button click."""
        with self.add_file_widgets["output"]:
            clear_output(wait=True)

            if not self.file_selector.value:
                display(create_status_html("No file selected", "error"))
                return

            if self.file_selector.value == "ocean_static":
                display(create_status_html("Cannot remove ocean_static", "error"))
                return

            try:
                file_to_remove = self.file_selector.value

                # Remove file and associated fields
                self.generator.files = [
                    f for f in self.generator.files if f["file_name"] != file_to_remove
                ]
                self.generator.fields = [
                    f for f in self.generator.fields if f["file_name"] != file_to_remove
                ]

                display(create_status_html(f"Removed {file_to_remove}", "success"))
                self.update_file_list()
            except Exception as e:
                display(create_status_html(f"ERROR: {str(e)}", "error"))

    def update_file_list(self, auto_select: bool = True):
        """Update the file selector with current files.

        Args:
            auto_select: Whether to auto-select the first file
        """
        file_names = [f["file_name"] for f in self.generator.files]
        self.file_selector.options = file_names
        if auto_select and file_names and not self.file_selector.value:
            self.file_selector.value = file_names[0]

    def get_layout(self) -> widgets.VBox:
        """Get the complete file manager layout.

        Returns:
            VBox containing all file manager widgets
        """
        return widgets.VBox(
            [
                create_section_header("Output Files", "(Click to select)"),
                self.file_selector,
                self.file_buttons,
                self.add_file_widgets["header"],
                self.add_file_widgets["name"],
                self.add_file_widgets["output"],
            ],
            layout=widgets.Layout(width="100%"),
        )


class FileConfigUI:
    """Handles configuration of individual files."""

    def __init__(self, generator, parser):
        """Initialize file configuration UI.

        Args:
            generator: DiagTableGenerator instance
            parser: DiagnosticsParser instance
        """
        self.generator = generator
        self.parser = parser
        self.current_file = None
        self.config_widgets = {}

    def show_file_config(self, file_name: str) -> widgets.VBox:
        """Create configuration widgets for a file.

        Args:
            file_name: Name of file to configure

        Returns:
            VBox containing configuration widgets
        """
        self.current_file = file_name

        # Find file config
        file_config = None
        for f in self.generator.files:
            if f["file_name"] == file_name:
                file_config = f
                break

        if not file_config:
            return widgets.VBox([widgets.HTML("<i>File not found</i>")])

        is_static = "static" in file_name.lower()

        # Create configuration widgets
        freq_widget = create_number_input(
            file_config["output_freq"],
            description="Output freq.:",
            disabled=is_static,
            width="320px",
            description_width="85px",
        )

        units_widget = create_dropdown(
            options=["hours", "days", "months", "years"],
            value=file_config["output_freq_units"],
            description="Freq. units:",
            width="320px",
            disabled=is_static,
            description_width="80px",
        )

        # Get all modules from diagnostics
        all_modules = set(["ocean_model"])
        for diag in self.parser.diagnostics.values():
            all_modules.update(diag.modules)

        module_widget = create_dropdown(
            options=sorted(list(all_modules)),
            value="ocean_model",
            description="Module name:",
            width="320px",
            description_width="95px",
        )

        reduction_widget = create_dropdown(
            options=["mean", "min", "max", "none"],
            value="mean",
            description="Reduction method:",
            width="320px",
            description_width="120px",
        )

        packing_widget = create_dropdown(
            options=[("real*8", 1), ("real*4", 2), ("16-bit int", 4), ("1-byte", 8)],
            value=2,
            description="Data precision:",
            width="320px",
            description_width="105px",
        )

        # Regional configuration
        regional_widgets = self._create_regional_widgets()

        # Apply button
        apply_output = widgets.Output()

        def apply_changes(b):
            """Apply settings to file and fields."""
            with apply_output:
                clear_output(wait=True)
                try:
                    # Update file configuration
                    for file_def in self.generator.files:
                        if file_def["file_name"] == file_name:
                            file_def["output_freq"] = freq_widget.value
                            file_def["output_freq_units"] = units_widget.value
                            break

                    # Get regional value
                    regional_val = self._get_regional_value(regional_widgets)

                    # Update fields
                    fields = [
                        f for f in self.generator.fields if f["file_name"] == file_name
                    ]
                    for field in fields:
                        field["module_name"] = module_widget.value
                        field["reduction_method"] = reduction_widget.value
                        field["regional_section"] = regional_val
                        field["packing"] = packing_widget.value

                    display(
                        create_status_html(
                            f"Settings applied to file and {len(fields)} diagnostic(s)",
                            "success",
                        )
                    )
                except Exception as e:
                    display(create_status_html(f"ERROR: {str(e)}", "error"))

        apply_btn = create_button(
            "Apply Settings to Selected",
            button_style="warning",
            icon="refresh",
            width="250px",
            on_click=apply_changes,
        )

        # Store widgets for later access
        self.config_widgets = {
            "freq": freq_widget,
            "units": units_widget,
            "module": module_widget,
            "reduction": reduction_widget,
            "packing": packing_widget,
            "regional": regional_widgets,
        }

        # Build layout
        config_widgets = [
            widgets.HTML(f"<b>File: {file_name}</b>"),
            widgets.HBox(
                [freq_widget, units_widget], layout=widgets.Layout(column_gap="10px")
            ),
            widgets.HBox(
                [module_widget, reduction_widget],
                layout=widgets.Layout(column_gap="10px"),
            ),
            widgets.HBox([packing_widget]),
            regional_widgets["dropdown"],
            regional_widgets["container"],
            widgets.HTML("<br>"),
            widgets.HBox([apply_btn, apply_output]),
        ]

        if is_static:
            config_widgets.append(
                widgets.HTML(
                    "<i style='color: #666;'>Note: Static file configuration is protected.</i>"
                )
            )

        return widgets.VBox(config_widgets)

    def _create_regional_widgets(self) -> dict:
        """Create regional section configuration widgets."""
        regional_dropdown = create_dropdown(
            options=["none", "global", "box"],
            value="none",
            description="Regional section:",
            description_width="110px",
        )

        # Box input widgets (initially hidden)
        lon_min = create_float_input(0.0, "Lon Min:")
        lon_max = create_float_input(0.0, "Lon Max:")
        lat_min = create_float_input(0.0, "Lat Min:")
        lat_max = create_float_input(0.0, "Lat Max:")
        vert_min = create_float_input(0.0, "Vert Min:")
        vert_max = create_float_input(0.0, "Vert Max:")

        regional_box_inputs = widgets.VBox(
            [
                create_hbox_row(lon_min, lon_max),
                create_hbox_row(lat_min, lat_max),
                create_hbox_row(vert_min, vert_max),
            ],
            layout=widgets.Layout(display="none"),
        )

        def on_regional_change(change):
            """Show/hide regional box inputs."""
            if change["new"] == "box":
                regional_box_inputs.layout.display = "block"
            else:
                regional_box_inputs.layout.display = "none"

        regional_dropdown.observe(on_regional_change, names="value")

        return {
            "dropdown": regional_dropdown,
            "container": regional_box_inputs,
            "lon_min": lon_min,
            "lon_max": lon_max,
            "lat_min": lat_min,
            "lat_max": lat_max,
            "vert_min": vert_min,
            "vert_max": vert_max,
        }

    def _get_regional_value(self, regional_widgets: dict) -> str:
        """Get regional section value from widgets.

        Args:
            regional_widgets: Dictionary of regional widgets

        Returns:
            Regional section string
        """
        regional_type = regional_widgets["dropdown"].value

        if regional_type == "none":
            return "none"
        elif regional_type == "global":
            return "global"
        elif regional_type == "box":
            lon_min = regional_widgets["lon_min"].value
            lon_max = regional_widgets["lon_max"].value
            lat_min = regional_widgets["lat_min"].value
            lat_max = regional_widgets["lat_max"].value
            vert_min = regional_widgets["vert_min"].value
            vert_max = regional_widgets["vert_max"].value
            return f"{lon_min} {lon_max} {lat_min} {lat_max} {vert_min} {vert_max}"

        return "none"
