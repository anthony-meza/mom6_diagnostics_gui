"""Interactive Jupyter widget interface for diag_table generation."""

import ipywidgets as widgets
from IPython.display import display, clear_output
from typing import Dict


class DiagTableUI:
    """Interactive UI for creating MOM6 diag_table files."""

    def __init__(self, parser, generator):
        """Initialize the UI."""
        self.parser = parser
        self.generator = generator
        self.current_file = None
        self.file_tabs = {}
        self._ui_created = False

        # Widgets
        self.file_selector = None
        self.file_config_area = None
        self.diag_area = None
        self.main_container = None
        self.export_label = None
        self.preview_output = None

    def update_preview(self):
        """Update the preview area with current diag_table."""
        if self.preview_output is None:
            return

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
                    layout=widgets.Layout(width='100%', height='500px'),
                    disabled=True
                )

                preview_accordion = widgets.Accordion(children=[preview_text])
                preview_accordion.set_title(0, f'diag_table ({num_files} files, {num_fields} diagnostics)')
                preview_accordion.selected_index = 0

                display(preview_accordion)

            except Exception as e:
                error_html = widgets.HTML(f"<span style='color: #dc3545;'>✗ ERROR: {str(e)}</span>")
                display(error_html)

    def update_export_label(self):
        """Update the export label with current counts."""
        if self.export_label is not None:
            num_files = len(self.generator.files)
            num_fields = len(self.generator.fields)
            self.export_label.value = f"<b style='color: #495057;'>Export</b> <span style='color: #6c757d; font-size: 0.9em;'>({num_files} file(s), {num_fields} diagnostic(s))</span>"

    def create_ui(self):
        """Create the main UI with file management."""
        # Prevent multiple UI creation
        if self._ui_created:
            return self.main_container

        self._ui_created = True

        # CASENAME configuration at the top
        casename_widget = widgets.Text(
            value=self.generator.title.split('CESM case: ')[-1] if 'CESM case: ' in self.generator.title else 'YOUR_CASE_NAME',
            placeholder='Enter CESM case name',
            description='Case Name:',
            layout=widgets.Layout(width='100%'),
            style={'description_width': '100px'}
        )

        def update_casename(change):
            """Update the generator title with new case name."""
            self.generator.title = f"MOM6 diagnostic fields table for CESM case: {change['new']}"

        casename_widget.observe(update_casename, names='value')

        casename_box = widgets.VBox([
            widgets.HTML("<h3 style='margin: 0 0 10px 0; color: #495057;'>MOM6 Diagnostic Table Generator</h3>"),
            casename_widget
        ], layout=widgets.Layout(margin='0 0 20px 0'))

        # Simplified help - just HTML, no accordion
        help_html = widgets.HTML("""
            <div style='background: #f8f9fa; padding: 10px; border-radius: 4px; margin-bottom: 10px; font-size: 0.9em;'>
            <b>Quick Start:</b> 1) Set case name 2) Double-click a file 3) Choose diagnostics 4) Preview and save
            </div>
        """)

        # File list header
        file_list_label = widgets.HTML("<b style='color: #495057;'>Output Files</b> <span style='color: #6c757d; font-size: 0.9em;'>(Double click to select)</span>")

        self.file_selector = widgets.Select(
            options=[],
            description='',
            layout=widgets.Layout(
                width='100%',
                height='160px',
                border='1px solid #ced4da',
                border_radius='4px'
            ),
            style={'description_width': '0px'}
        )

        # File management buttons
        add_file_btn = widgets.Button(
            description='Add File',
            button_style='success',
            icon='plus',
            layout=widgets.Layout(width='48%')
        )

        remove_file_btn = widgets.Button(
            description='Remove',
            button_style='danger',
            icon='trash',
            layout=widgets.Layout(width='48%')
        )

        # Preview button
        preview_btn = widgets.Button(
            description='Preview diag_table',
            button_style='info',
            icon='eye',
            layout=widgets.Layout(width='100%')
        )

        # Preview output area
        self.preview_output = widgets.Output()

        # Export section header with status
        self.export_label = widgets.HTML("<b style='color: #495057;'>Export</b> <span style='color: #6c757d; font-size: 0.9em;'>(0 file(s), 0 diagnostic(s))</span>")

        output_path_widget = widgets.Text(
            value='./diag_table',
            placeholder='Path to save diag_table',
            description='Save to:',
            layout=widgets.Layout(width='100%')
        )

        save_btn = widgets.Button(
            description='Save File',
            button_style='success',
            icon='save',
            layout=widgets.Layout(width='48%')
        )

        clear_btn = widgets.Button(
            description='Clear All',
            button_style='danger',
            icon='trash',
            layout=widgets.Layout(width='48%')
        )

        export_status = widgets.Output()

        # File configuration area
        self.file_config_area = widgets.VBox([
            widgets.HTML("<i>Select a file or add a new one to configure.</i>")
        ])

        # Diagnostics selection area
        self.diag_area = widgets.VBox([
            widgets.HTML("<i>Double-click a file to add diagnostics.</i>")
        ])

        def show_preview(b):
            """Display preview of diag_table."""
            self.update_preview()

        def save_diag_table(b):
            """Save diag_table to file."""
            with export_status:
                clear_output(wait=True)
                try:
                    # Save file
                    filepath = self.generator.save(output_path_widget.value)

                    # Update status with checkmark
                    num_files = len(self.generator.files)
                    num_fields = len(self.generator.fields)
                    status_html = widgets.HTML(f"<span style='color: #28a745;'>✓ Saved ({num_files} file(s), {num_fields} diagnostic(s))</span>")
                    display(status_html)
                    self.update_export_label()

                except Exception as e:
                    error_html = widgets.HTML(f"<span style='color: #dc3545;'>✗ ERROR: {str(e)}</span>")
                    display(error_html)

        def clear_all(b):
            """Clear all configurations."""
            with export_status:
                clear_output(wait=True)
                self.generator.clear()

                # Restore default configuration
                # Static file
                self.generator.add_file('ocean_static', -1, 'months')
                self.generator.add_field('ocean_model', 'deptho', 'ocean_static', 'deptho', 'all', 'none', 'none', 2)
                self.generator.add_field('ocean_model', 'geolon', 'ocean_static', 'geolon', 'all', 'none', 'none', 2)
                self.generator.add_field('ocean_model', 'geolat', 'ocean_static', 'geolat', 'all', 'none', 'none', 2)
                self.generator.add_field('ocean_model', 'wet', 'ocean_static', 'wet', 'all', 'none', 'none', 2)

                # High-frequency file
                self.generator.add_file('surf_%4yr_%3dy', 1, 'hours', new_file_freq=1, new_file_freq_units='months')
                self.generator.add_field('ocean_model', 'SSH', 'surf_%4yr_%3dy', 'SSH', 'all', 'none', 'none', 2)

                # Daily averages
                self.generator.add_file('ocean_daily', 1, 'days')
                self.generator.add_field('ocean_model', 'tos', 'ocean_daily', 'tos', 'all', 'mean', 'none', 2)

                # Monthly averages
                self.generator.add_file('ocean_month', 1, 'months')
                self.generator.add_field('ocean_model', 'thetao', 'ocean_month', 'thetao', 'all', 'mean', 'none', 2)

                # Annual averages
                self.generator.add_file('ocean_annual', 12, 'months')
                self.generator.add_field('ocean_model', 'thetao', 'ocean_annual', 'thetao', 'all', 'mean', 'none', 2)

                # Vertical section
                self.generator.add_file('ocean_Bering_Strait', 5, 'days')
                self.generator.add_field('ocean_model', 'thetao', 'ocean_Bering_Strait', 'thetao', 'all', 'mean', '-171.4 -168.7 66.1 66.1 -1 -1', 2)

                self.update_file_list()
                status_html = widgets.HTML("<span style='color: #28a745;'>✓ Configuration cleared</span>")
                display(status_html)
                self.update_export_label()

        # Register button handlers
        preview_btn.on_click(show_preview)
        save_btn.on_click(save_diag_table)
        clear_btn.on_click(clear_all)

        # Add file section header
        add_file_header = widgets.HTML("<b style='color: #6c757d;'>Add New File</b>")

        # Add file dialog widgets - just name
        new_file_name = widgets.Text(
            placeholder='e.g., ocean_daily%4yr-%2mo',
            description='Name:',
            layout=widgets.Layout(width='100%'),
            style={'description_width': '60px'}
        )

        new_file_output = widgets.Output()

        def add_file(b):
            """Add a new output file with default freq/units."""
            with new_file_output:
                clear_output(wait=True)
                if not new_file_name.value:
                    error_html = widgets.HTML("<span style='color: #dc3545;'>Please enter a file name</span>")
                    display(error_html)
                    return

                try:
                    # Add file with default freq=1, units='days'
                    self.generator.add_file(
                        new_file_name.value,
                        1,
                        'days'
                    )
                    status_html = widgets.HTML(f"<span style='color: #28a745;'>✓ Added {new_file_name.value} (configure freq/units in File Configuration)</span>")
                    display(status_html)
                    new_file_name.value = ''
                    self.update_file_list()
                    self.update_export_label()
                except Exception as e:
                    error_html = widgets.HTML(f"<span style='color: #dc3545;'>✗ ERROR: {str(e)}</span>")
                    display(error_html)

        def remove_file(b):
            """Remove selected file."""
            with new_file_output:
                clear_output(wait=True)
                if not self.file_selector.value:
                    error_html = widgets.HTML("<span style='color: #dc3545;'>No file selected</span>")
                    display(error_html)
                    return

                if self.file_selector.value == 'ocean_static':
                    error_html = widgets.HTML("<span style='color: #dc3545;'>Cannot remove ocean_static</span>")
                    display(error_html)
                    return

                try:
                    file_to_remove = self.file_selector.value

                    # Remove file from generator's files list
                    self.generator.files = [f for f in self.generator.files if f['file_name'] != file_to_remove]

                    # Remove all fields associated with this file
                    self.generator.fields = [f for f in self.generator.fields if f['file_name'] != file_to_remove]

                    status_html = widgets.HTML(f"<span style='color: #28a745;'>✓ Removed {file_to_remove}</span>")
                    display(status_html)
                    self.update_file_list()
                    self.update_export_label()
                except Exception as e:
                    error_html = widgets.HTML(f"<span style='color: #dc3545;'>✗ ERROR: {str(e)}</span>")
                    display(error_html)

        def on_file_selected(change):
            """Handle file selection."""
            if change['new']:
                self.show_file_config(change['new'])

        add_file_btn.on_click(add_file)
        remove_file_btn.on_click(remove_file)
        self.file_selector.observe(on_file_selected, names='value')

        # Layout - Left panel (file management)
        file_mgmt_area = widgets.VBox([
            file_list_label,
            self.file_selector,
            widgets.HBox([add_file_btn, remove_file_btn]),
            add_file_header,
            new_file_name,
            new_file_output,
            widgets.HTML("<br>"),
            self.export_label,
            output_path_widget,
            widgets.HBox([save_btn, clear_btn]),
            export_status
        ], layout=widgets.Layout(
            width='350px',
            padding='15px',
            border='1px solid #dee2e6',
            border_radius='6px',
            background_color='#ffffff'
        ))

        # Tab 1: Configure & Select
        config_and_select_tab = widgets.VBox([
            widgets.HTML("<h4 style='color: #495057; margin: 10px 0;'>File Configuration</h4>"),
            self.file_config_area,
            widgets.HTML("<h4 style='color: #495057; margin: 15px 0 10px 0;'>Select Diagnostics</h4>"),
            self.diag_area
        ], layout=widgets.Layout(
            padding='15px'
        ))

        # Tab 2: Preview
        preview_tab = widgets.VBox([
            widgets.HTML("<h4 style='color: #495057; margin: 10px 0;'>Preview</h4>"),
            preview_btn,
            self.preview_output
        ], layout=widgets.Layout(
            padding='15px'
        ))

        # Create tabs
        tabs = widgets.Tab(children=[config_and_select_tab, preview_tab])
        tabs.set_title(0, 'Configure & Select')
        tabs.set_title(1, 'Preview')

        # Right panel with tabs - wider for better text display
        right_panel = widgets.VBox([tabs], layout=widgets.Layout(
            width='calc(100% - 360px)',
            border='1px solid #dee2e6',
            border_radius='6px',
            background_color='#ffffff'
        ))

        # Main container - 2 columns
        self.main_container = widgets.HBox([
            file_mgmt_area,
            right_panel
        ], layout=widgets.Layout(
            padding='20px',
            background_color='#ffffff'
        ))

        # Initialize - don't auto-select to avoid slow initial load
        self.update_file_list(auto_select=False)
        self.update_export_label()

        # Complete layout
        return widgets.VBox([casename_box, help_html, self.main_container])

    def update_file_list(self, auto_select=True):
        """Update the file selector with current files."""
        file_names = [f['file_name'] for f in self.generator.files]
        self.file_selector.options = file_names
        if auto_select and file_names and not self.file_selector.value:
            self.file_selector.value = file_names[0]

    def show_file_config(self, file_name: str):
        """Show configuration for selected file."""
        self.current_file = file_name

        # Find file config
        file_config = None
        for f in self.generator.files:
            if f['file_name'] == file_name:
                file_config = f
                break

        if not file_config:
            return

        is_static = 'static' in file_name.lower()

        # Frequency widgets
        freq_widget = widgets.IntText(
            value=file_config['output_freq'],
            description='Freq:',
            disabled=is_static,
            layout=widgets.Layout(width='48%')
        )

        units_widget = widgets.Dropdown(
            options=['hours', 'days', 'months', 'years'],
            value=file_config['output_freq_units'],
            description='Units:',
            disabled=is_static,
            layout=widgets.Layout(width='48%')
        )

        # Module widget
        all_modules = set(['ocean_model'])
        for diag in self.parser.diagnostics.values():
            all_modules.update(diag.modules)

        module_widget = widgets.Dropdown(
            options=sorted(list(all_modules)),
            value='ocean_model',
            description='Module:',
            layout=widgets.Layout(width='48%')
        )

        # Reduction widget
        reduction_widget = widgets.Dropdown(
            options=['average', 'min', 'max', 'none'],
            value='average',
            description='Reduction:',
            layout=widgets.Layout(width='48%')
        )

        # Packing widget
        packing_widget = widgets.Dropdown(
            options=[('real*8', 1), ('real*4', 2), ('16-bit int', 4), ('1-byte', 8)],
            value=2,
            description='Packing:',
            layout=widgets.Layout(width='48%')
        )

        # Regional dropdown
        regional_dropdown = widgets.Dropdown(
            options=['none', 'global', 'box'],
            value='none',
            description='Regional:',
            layout=widgets.Layout(width='100%')
        )

        # Regional box input widgets (initially hidden)
        lon_min_widget = widgets.FloatText(
            value=0.0,
            description='Lon Min:',
            layout=widgets.Layout(width='48%')
        )
        lon_max_widget = widgets.FloatText(
            value=0.0,
            description='Lon Max:',
            layout=widgets.Layout(width='48%')
        )
        lat_min_widget = widgets.FloatText(
            value=0.0,
            description='Lat Min:',
            layout=widgets.Layout(width='48%')
        )
        lat_max_widget = widgets.FloatText(
            value=0.0,
            description='Lat Max:',
            layout=widgets.Layout(width='48%')
        )
        vert_min_widget = widgets.FloatText(
            value=0.0,
            description='Vert Min:',
            layout=widgets.Layout(width='48%')
        )
        vert_max_widget = widgets.FloatText(
            value=0.0,
            description='Vert Max:',
            layout=widgets.Layout(width='48%')
        )

        # Container for regional box inputs
        regional_box_inputs = widgets.VBox([
            widgets.HBox([lon_min_widget, lon_max_widget]),
            widgets.HBox([lat_min_widget, lat_max_widget]),
            widgets.HBox([vert_min_widget, vert_max_widget])
        ], layout=widgets.Layout(display='none'))

        def on_regional_change(change):
            """Show/hide regional box inputs based on selection."""
            if change['new'] == 'box':
                regional_box_inputs.layout.display = 'block'
            else:
                regional_box_inputs.layout.display = 'none'

        regional_dropdown.observe(on_regional_change, names='value')

        apply_output = widgets.Output()

        def apply_changes(b):
            """Apply settings to file configuration and selected diagnostics."""
            with apply_output:
                clear_output(wait=True)
                try:
                    # Update file configuration (freq and units)
                    for file_def in self.generator.files:
                        if file_def['file_name'] == file_name:
                            file_def['output_freq'] = freq_widget.value
                            file_def['output_freq_units'] = units_widget.value
                            break

                    # Get all fields for this file
                    fields = [f for f in self.generator.fields if f['file_name'] == file_name]

                    # Construct regional_section based on dropdown
                    regional_type = regional_dropdown.value
                    if regional_type == 'none':
                        regional_val = 'none'
                    elif regional_type == 'global':
                        regional_val = 'global'
                    elif regional_type == 'box':
                        lon_min = lon_min_widget.value
                        lon_max = lon_max_widget.value
                        lat_min = lat_min_widget.value
                        lat_max = lat_max_widget.value
                        vert_min = vert_min_widget.value
                        vert_max = vert_max_widget.value
                        regional_val = f'{lon_min} {lon_max} {lat_min} {lat_max} {vert_min} {vert_max}'
                    else:
                        regional_val = 'none'

                    # Update each field
                    for field in fields:
                        field['module_name'] = module_widget.value
                        field['reduction_method'] = reduction_widget.value
                        field['regional_section'] = regional_val
                        field['packing'] = packing_widget.value

                    status_html = widgets.HTML(f"<span style='color: #28a745;'>✓ Settings applied to file and {len(fields)} diagnostic(s)</span>")
                    display(status_html)

                except Exception as e:
                    error_html = widgets.HTML(f"<span style='color: #dc3545;'>✗ ERROR: {str(e)}</span>")
                    display(error_html)

        apply_btn = widgets.Button(
            description='Apply Settings to Selected',
            button_style='warning',
            icon='refresh',
            layout=widgets.Layout(width='250px')
        )
        apply_btn.on_click(apply_changes)

        config_widgets = [
            widgets.HTML(f"<b>File: {file_name}</b>"),
            widgets.HBox([freq_widget, units_widget]),
            widgets.HBox([module_widget, reduction_widget]),
            widgets.HBox([packing_widget]),
            regional_dropdown,
            regional_box_inputs,
            widgets.HTML("<br>"),
            widgets.HBox([apply_btn, apply_output])
        ]

        if is_static:
            config_widgets.append(widgets.HTML("<i style='color: #666;'>Note: Static file configuration is protected.</i>"))

        self.file_config_area.children = config_widgets

        # Show diagnostics for this file
        self.show_diagnostics(file_name, module_widget, reduction_widget, packing_widget, regional_dropdown,
                            lon_min_widget, lon_max_widget, lat_min_widget, lat_max_widget,
                            vert_min_widget, vert_max_widget)

    def show_diagnostics(self, file_name: str, module_widget, reduction_widget, packing_widget, regional_dropdown,
                        lon_min_widget, lon_max_widget, lat_min_widget, lat_max_widget,
                        vert_min_widget, vert_max_widget):
        """Show diagnostic selection for the current file."""

        # Selected diagnostics container (for tab 2)
        selected_container = widgets.VBox([],
            layout=widgets.Layout(
                max_height='400px',
                overflow_y='auto',
                border='1px solid #dee2e6',
                border_radius='4px',
                padding='10px',
                background_color='#fafafa'
            )
        )

        selected_page = [0]
        selected_page_size = 5

        def update_selected_display():
            """Update the selected diagnostics tab."""
            selected_fields = [f['field_name'] for f in self.generator.fields if f['file_name'] == file_name]

            if not selected_fields:
                selected_container.children = [widgets.HTML("<i>No diagnostics selected for this file yet.</i>")]
                return

            # Calculate pagination
            total_selected = len(selected_fields)
            total_pages = (total_selected + selected_page_size - 1) // selected_page_size
            start_idx = selected_page[0] * selected_page_size
            end_idx = min(start_idx + selected_page_size, total_selected)
            page_fields = selected_fields[start_idx:end_idx]

            # Create checkboxes
            items = []
            for field_name in page_fields:
                # Find diagnostic
                diag_obj = None
                for diag in self.parser.diagnostics.values():
                    if diag.name == field_name or (diag.variants and field_name in diag.variants):
                        diag_obj = diag
                        break

                if diag_obj:
                    cb = widgets.Checkbox(
                        value=True,
                        description=diag_obj.display_name(),
                        indent=False,
                        layout=widgets.Layout(width='100%'),
                        style={'description_width': 'initial'}
                    )

                    def make_unselect_handler(diag):
                        def on_unselect(change):
                            if not change['new']:
                                # Remove field
                                names_to_try = [diag.name]
                                if diag.variants:
                                    names_to_try.extend(diag.variants)
                                for name in names_to_try:
                                    self.generator.remove_field(name, file_name)
                                # Refresh both tabs
                                update_selected_display()
                                update_diagnostics_list(reset_page=False)
                        return on_unselect

                    cb.observe(make_unselect_handler(diag_obj), names='value')
                    items.append(cb)

            # Pagination
            if total_pages > 1:
                page_info = widgets.HTML(
                    f"<div style='text-align: center; margin: 10px 0; color: #6c757d;'>"
                    f"Page {selected_page[0] + 1} of {total_pages} "
                    f"(showing {start_idx + 1}-{end_idx} of {total_selected})"
                    f"</div>"
                )

                prev_btn = widgets.Button(description='← Previous', disabled=(selected_page[0] == 0), layout=widgets.Layout(width='48%'))
                next_btn = widgets.Button(description='Next →', disabled=(selected_page[0] >= total_pages - 1), layout=widgets.Layout(width='48%'))

                def go_prev(b):
                    if selected_page[0] > 0:
                        selected_page[0] -= 1
                        update_selected_display()

                def go_next(b):
                    if selected_page[0] < total_pages - 1:
                        selected_page[0] += 1
                        update_selected_display()

                prev_btn.on_click(go_prev)
                next_btn.on_click(go_next)

                items.append(page_info)
                items.append(widgets.HBox([prev_btn, next_btn]))

            selected_container.children = items

        # Search and filter widgets
        search_widget = widgets.Text(
            placeholder='e.g., tos, thetao, SST...',
            description='Search:',
            layout=widgets.Layout(width='300px'),
            style={'description_width': '60px'}
        )

        category_widget = widgets.Dropdown(
            options=['All Diagnostics', 'Grid & Static'],
            value='Grid & Static' if 'static' in file_name.lower() else 'All Diagnostics',
            description='Category:',
            layout=widgets.Layout(width='250px'),
            style={'description_width': '70px'}
        )

        dim_filter = widgets.Dropdown(
            options=['All', '2D Only', '3D Only'],
            value='All',
            description='Dimension:',
            layout=widgets.Layout(width='200px'),
            style={'description_width': '75px'}
        )

        # Header that shows selection count
        select_diag_header = widgets.HTML("<b style='color: #6c757d;'>Diagnostics (Selected: 0)</b>")

        diag_container = widgets.VBox([],
            layout=widgets.Layout(
                max_height='400px',
                overflow_y='auto',
                border='1px solid #dee2e6',
                border_radius='4px',
                padding='10px',
                background_color='#fafafa'
            )
        )

        checkboxes_dict: Dict[str, widgets.Checkbox] = {}

        # Cache for field names to avoid repeated lookups
        _selected_fields_cache = set()

        # Pagination state
        current_page = [0]  # Use list to allow modification in nested function
        page_size = 5
        filtered_diags = []  # Store filtered results for pagination

        def update_diagnostics_list(change=None, reset_page=True):
            """Update the list of diagnostics based on filters."""
            nonlocal filtered_diags

            search_term = search_widget.value.lower()
            category = category_widget.value
            dim_filter_val = dim_filter.value

            # Reset to first page when filters change
            if reset_page:
                current_page[0] = 0

            # Filter diagnostics
            diags = list(self.parser.diagnostics.values())

            if search_term:
                def matches_search(d):
                    # Check name and long_name
                    if search_term in d.name.lower() or search_term in d.long_name.lower():
                        return True
                    # Check variants
                    if d.variants:
                        for variant in d.variants:
                            if search_term in variant.lower():
                                return True
                    return False

                diags = [d for d in diags if matches_search(d)]

            if category == 'Grid & Static':
                cat_diags = self.parser.get_by_category().get('Grid & Static', [])
                diags = [d for d in diags if d in cat_diags]

            if dim_filter_val == '2D Only':
                diags = [d for d in diags if d.is_2d()]
            elif dim_filter_val == '3D Only':
                diags = [d for d in diags if d.is_3d()]

            diags.sort(key=lambda x: x.name)
            filtered_diags = diags  # Store for pagination

            # Update cache of selected fields for this file
            # Check if any variant of a diagnostic is selected
            _selected_fields_cache.clear()
            selected_field_names = {f['field_name'] for f in self.generator.fields if f['file_name'] == file_name}

            for diag in self.parser.diagnostics.values():
                # Check if diagnostic name is selected
                if diag.name in selected_field_names:
                    _selected_fields_cache.add(diag.name)
                # Check if any variant is selected
                elif diag.variants:
                    for variant in diag.variants:
                        if variant in selected_field_names:
                            _selected_fields_cache.add(diag.name)
                            break

            # Calculate pagination
            total_diags = len(filtered_diags)
            total_pages = (total_diags + page_size - 1) // page_size  # Ceiling division
            start_idx = current_page[0] * page_size
            end_idx = min(start_idx + page_size, total_diags)
            page_diags = filtered_diags[start_idx:end_idx]

            # Create checkboxes
            checkboxes = []
            checkboxes_dict.clear()

            # Pre-compute display names to avoid repeated calls
            for diag in page_diags:
                is_checked = diag.name in _selected_fields_cache

                # Create checkbox with proper layout to avoid text cutoff
                cb = widgets.Checkbox(
                    value=is_checked,
                    description=diag.display_name(),
                    indent=False,
                    layout=widgets.Layout(width='100%'),
                    style={'description_width': 'initial'}
                )

                checkboxes_dict[diag.name] = cb

                def make_on_change(diag_obj):
                    def on_change(change):
                        # Only process actual changes
                        if change['old'] == change['new']:
                            return

                        if change['new']:
                            # Use the primary name (first variant if available)
                            primary_name = diag_obj.get_primary_name()

                            # Construct regional_section based on dropdown
                            regional_type = regional_dropdown.value

                            if regional_type == 'none':
                                regional_val = 'none'
                            elif regional_type == 'global':
                                regional_val = 'global'
                            elif regional_type == 'box':
                                # Build box specification: lon_min lon_max lat_min lat_max vert_min vert_max
                                lon_min = lon_min_widget.value
                                lon_max = lon_max_widget.value
                                lat_min = lat_min_widget.value
                                lat_max = lat_max_widget.value
                                vert_min = vert_min_widget.value
                                vert_max = vert_max_widget.value
                                regional_val = f'{lon_min} {lon_max} {lat_min} {lat_max} {vert_min} {vert_max}'
                            else:
                                regional_val = 'none'

                            self.generator.add_field(
                                module_name=module_widget.value,
                                field_name=primary_name,
                                file_name=file_name,
                                reduction_method=reduction_widget.value,
                                time_sampling='all',
                                regional_section=regional_val,
                                packing=packing_widget.value
                            )
                            _selected_fields_cache.add(diag_obj.name)
                        else:
                            # Remove by checking all possible names (diagnostic name + all variants)
                            names_to_try = [diag_obj.name]
                            if diag_obj.variants:
                                names_to_try.extend(diag_obj.variants)

                            for name in names_to_try:
                                self.generator.remove_field(name, file_name)

                            _selected_fields_cache.discard(diag_obj.name)
                        update_status()
                    return on_change

                cb.observe(make_on_change(diag), names='value')
                checkboxes.append(cb)

            # Add pagination info and controls
            if total_pages > 1:
                page_info = widgets.HTML(
                    f"<div style='text-align: center; margin: 10px 0; color: #6c757d;'>"
                    f"Page {current_page[0] + 1} of {total_pages} "
                    f"(showing {start_idx + 1}-{end_idx} of {total_diags} diagnostics)"
                    f"</div>"
                )

                prev_btn = widgets.Button(
                    description='← Previous',
                    disabled=(current_page[0] == 0),
                    layout=widgets.Layout(width='48%')
                )

                next_btn = widgets.Button(
                    description='Next →',
                    disabled=(current_page[0] >= total_pages - 1),
                    layout=widgets.Layout(width='48%')
                )

                def go_prev(b):
                    if current_page[0] > 0:
                        current_page[0] -= 1
                        update_diagnostics_list(reset_page=False)

                def go_next(b):
                    if current_page[0] < total_pages - 1:
                        current_page[0] += 1
                        update_diagnostics_list(reset_page=False)

                prev_btn.on_click(go_prev)
                next_btn.on_click(go_next)

                pagination_controls = widgets.HBox([prev_btn, next_btn])
                checkboxes.append(page_info)
                checkboxes.append(pagination_controls)
            elif total_diags == 0:
                checkboxes.append(widgets.HTML("<i>No diagnostics match the current filters.</i>"))

            diag_container.children = checkboxes
            update_status()

        def update_status():
            count = len(_selected_fields_cache)
            select_diag_header.value = f"<b style='color: #6c757d;'>Diagnostics (Selected: {count})</b>"
            update_selected_display()
            self.update_export_label()

        def select_all(b):
            # Use hold_sync to batch updates and prevent lag
            with diag_container.hold_sync():
                for name, cb in checkboxes_dict.items():
                    if not cb.value:
                        cb.value = True

        def deselect_all(b):
            # Use hold_sync to batch updates and prevent lag
            with diag_container.hold_sync():
                for name, cb in checkboxes_dict.items():
                    if cb.value:
                        cb.value = False

        select_all_btn = widgets.Button(
            description='Select All Visible',
            button_style='info',
            icon='check-square',
            layout=widgets.Layout(width='150px')
        )
        select_all_btn.on_click(select_all)

        deselect_all_btn = widgets.Button(
            description='Deselect All',
            button_style='warning',
            icon='square',
            layout=widgets.Layout(width='150px')
        )
        deselect_all_btn.on_click(deselect_all)

        search_widget.observe(update_diagnostics_list, names='value')
        category_widget.observe(update_diagnostics_list, names='value')
        dim_filter.observe(update_diagnostics_list, names='value')

        update_diagnostics_list()
        update_selected_display()

        # Tab 1: Browse and select diagnostics
        browse_tab = widgets.VBox([
            select_diag_header,
            widgets.HBox([search_widget, category_widget, dim_filter], layout=widgets.Layout(margin='0 0 10px 0')),
            widgets.HBox([
                select_all_btn,
                deselect_all_btn
            ], layout=widgets.Layout(margin='0 0 10px 0')),
            diag_container
        ])

        # Tab 2: View selected diagnostics
        selected_header = widgets.HTML("<b style='color: #6c757d;'>Selected Diagnostics</b>")
        selected_tab = widgets.VBox([
            selected_header,
            selected_container
        ])

        # Create tabs
        diag_tabs = widgets.Tab(children=[browse_tab, selected_tab])
        diag_tabs.set_title(0, 'Select Diagnostics')
        diag_tabs.set_title(1, 'See Selected')

        self.diag_area.children = [diag_tabs]


# Global UI instance for singleton pattern
_ui_instance = None


def create_diag_table_ui(diag_file):
    """Create and display interactive UI for diag_table generation."""
    global _ui_instance

    if _ui_instance is not None:
        print("UI already exists. Restart kernel to reload.")
        return _ui_instance

    try:
        from ..core import DiagnosticsParser, DiagTableGenerator
        import time
        import os

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

        # Parse and cache diagnostics BEFORE creating any UI widgets
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

        # Now create the generator and UI
        generator = DiagTableGenerator(
            title="MOM6 diagnostic fields table for CESM case: YOUR_CASE_NAME",
            base_year=1900
        )

        # Add default ocean_static file
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
        generator.add_field('ocean_model', 'thetao', 'ocean_Bering_Strait', 'thetao', 'all', 'mean', '-171.4 -168.7 66.1 66.1 -1 -1', 2)

        progress.value = 80
        status_label.value = 'Creating UI...'

        ui_start = time.time()
        ui = DiagTableUI(parser, generator)
        init_time = time.time() - ui_start

        create_start = time.time()
        ui_widget = ui.create_ui()
        create_time = time.time() - create_start

        ui_time = time.time() - ui_start

        progress.value = 100
        status_label.value = f'Ready! (init: {init_time:.2f}s, create: {create_time:.2f}s, total: {ui_time:.2f}s)'
        progress.bar_style = 'success'

        display(ui_widget)

        # Close the progress bar after a short delay
        loading_box.close()

        _ui_instance = ui
        return ui

    except FileNotFoundError:
        print(f"ERROR: File not found: {diag_file}")
        return None
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return None
