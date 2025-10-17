"""Diagnostic selection UI components.

This module handles the diagnostic browsing, searching, filtering,
and selection interface.
"""

import ipywidgets as widgets
from typing import Dict, Callable, Optional, Set, List
from .widgets import (
    create_text_widget, create_dropdown, create_button,
    create_section_header, create_scrollable_container,
    create_pagination_controls
)


class DiagnosticSelectorUI:
    """Manages the diagnostic selection interface."""

    def __init__(
        self,
        parser,
        generator,
        file_name: str,
        file_config_widgets: Dict,
        on_selection_change: Optional[Callable] = None
    ):
        """Initialize diagnostic selector.

        Args:
            parser: DiagnosticsParser instance
            generator: DiagTableGenerator instance
            file_name: Name of file to select diagnostics for
            file_config_widgets: Dictionary of file configuration widgets
            on_selection_change: Callback when selection changes
        """
        self.parser = parser
        self.generator = generator
        self.file_name = file_name
        self.file_config_widgets = file_config_widgets
        self.on_selection_change = on_selection_change

        # Cache categories to avoid repeated computation
        self._categories_cache = None

        # State
        self.current_page = 0
        self.page_size = 5
        self.filtered_diags = []
        self.selected_cache: Set[str] = set()
        self.checkboxes_dict: Dict[str, widgets.Checkbox] = {}

        # Create widgets
        self.search_widget = self._create_search_widget()
        self.category_widget = self._create_category_widget()
        self.dim_filter = self._create_dimension_filter()
        self.diag_container = create_scrollable_container([])
        self.header = create_section_header('Diagnostics', '(Selected: 0)')

        # Initialize
        self._update_selection_cache()
        self.update_diagnostics_list()

    def _create_search_widget(self) -> widgets.Text:
        """Create search text widget."""
        widget = create_text_widget(
            placeholder='e.g., tos, thetao, SST...',
            description='Search:',
            width='300px',
            description_width='60px'
        )
        widget.observe(lambda change: self.update_diagnostics_list(reset_page=True), names='value')
        return widget

    def _get_categories(self) -> Dict:
        """Get categories with caching for performance.

        Returns:
            Dictionary of categories
        """
        if self._categories_cache is None:
            self._categories_cache = self.parser.get_by_category()
        return self._categories_cache

    def _create_category_widget(self) -> widgets.Dropdown:
        """Create category dropdown with dynamic categories."""
        # Get actual categories from parser (cached)
        categories = self._get_categories()
        category_names = ['All Diagnostics'] + list(categories.keys())

        # Set default value
        if 'static' in self.file_name.lower() and 'Grid & Static' in category_names:
            default_value = 'Grid & Static'
        else:
            default_value = 'All Diagnostics'

        widget = create_dropdown(
            options=category_names,
            value=default_value,
            description='Category:',
            width='250px',
            description_width='70px'
        )
        widget.observe(lambda change: self.update_diagnostics_list(reset_page=True), names='value')
        return widget

    def _create_dimension_filter(self) -> widgets.Dropdown:
        """Create dimension filter dropdown."""
        widget = create_dropdown(
            options=['All', '2D Only', '3D Only'],
            value='All',
            description='Dimension:',
            width='200px',
            description_width='75px'
        )
        widget.observe(lambda change: self.update_diagnostics_list(reset_page=True), names='value')
        return widget

    def _update_selection_cache(self):
        """Update cache of selected fields."""
        self.selected_cache.clear()
        selected_field_names = {
            f['field_name'] for f in self.generator.fields
            if f['file_name'] == self.file_name
        }

        for diag in self.parser.diagnostics.values():
            if diag.name in selected_field_names:
                self.selected_cache.add(diag.name)
            elif diag.variants:
                for variant in diag.variants:
                    if variant in selected_field_names:
                        self.selected_cache.add(diag.name)
                        break

    def _filter_diagnostics(self) -> List:
        """Filter diagnostics based on search, category, and dimension.

        Returns:
            List of filtered Diagnostic objects
        """
        search_term = self.search_widget.value.lower()
        category = self.category_widget.value
        dim_filter_val = self.dim_filter.value

        # Start with all diagnostics
        diags = list(self.parser.diagnostics.values())

        # Apply search filter
        if search_term:
            def matches_search(d):
                if search_term in d.name.lower() or search_term in d.long_name.lower():
                    return True
                if d.variants:
                    for variant in d.variants:
                        if search_term in variant.lower():
                            return True
                return False

            diags = [d for d in diags if matches_search(d)]

        # Apply category filter (dynamic - works with any category)
        if category != 'All Diagnostics':
            cat_diags = self._get_categories().get(category, [])
            diags = [d for d in diags if d in cat_diags]

        # Apply dimension filter
        if dim_filter_val == '2D Only':
            diags = [d for d in diags if d.is_2d()]
        elif dim_filter_val == '3D Only':
            diags = [d for d in diags if d.is_3d()]

        diags.sort(key=lambda x: x.name)
        return diags

    def update_diagnostics_list(self, change=None, reset_page: bool = True):
        """Update the diagnostics list display.

        Args:
            change: Widget change event (unused)
            reset_page: Whether to reset to first page
        """
        if reset_page:
            self.current_page = 0

        # Filter diagnostics
        self.filtered_diags = self._filter_diagnostics()

        # Update selection cache
        self._update_selection_cache()

        # Calculate pagination
        total_diags = len(self.filtered_diags)
        total_pages = max(1, (total_diags + self.page_size - 1) // self.page_size)
        start_idx = self.current_page * self.page_size
        end_idx = min(start_idx + self.page_size, total_diags)
        page_diags = self.filtered_diags[start_idx:end_idx]

        # Create checkboxes
        checkboxes = []
        self.checkboxes_dict.clear()

        for diag in page_diags:
            is_checked = diag.name in self.selected_cache

            cb = widgets.Checkbox(
                value=is_checked,
                description=diag.display_name(),
                indent=False,
                layout=widgets.Layout(width='100%'),
                style={'description_width': 'initial'}
            )

            self.checkboxes_dict[diag.name] = cb

            def make_on_change(diag_obj):
                def on_change(change):
                    if change['old'] == change['new']:
                        return

                    if change['new']:
                        self._add_diagnostic(diag_obj)
                    else:
                        self._remove_diagnostic(diag_obj)

                    self._update_status()
                return on_change

            cb.observe(make_on_change(diag), names='value')
            checkboxes.append(cb)

        # Add pagination if needed
        if total_pages > 1:
            page_info, pagination = create_pagination_controls(
                self.current_page,
                total_pages,
                self._go_prev,
                self._go_next,
                start_idx + 1,
                end_idx,
                total_diags
            )
            checkboxes.append(page_info)
            checkboxes.append(pagination)
        elif total_diags == 0:
            checkboxes.append(
                widgets.HTML("<i>No diagnostics match the current filters.</i>")
            )

        self.diag_container.children = checkboxes
        self._update_status()

    def _add_diagnostic(self, diag):
        """Add a diagnostic to the generator."""
        primary_name = diag.get_primary_name()
        regional_val = self._get_regional_value()

        self.generator.add_field(
            module_name=self.file_config_widgets['module'].value,
            field_name=primary_name,
            file_name=self.file_name,
            reduction_method=self.file_config_widgets['reduction'].value,
            time_sampling='all',
            regional_section=regional_val,
            packing=self.file_config_widgets['packing'].value
        )
        self.selected_cache.add(diag.name)

    def _remove_diagnostic(self, diag):
        """Remove a diagnostic from the generator."""
        names_to_try = [diag.name]
        if diag.variants:
            names_to_try.extend(diag.variants)

        for name in names_to_try:
            self.generator.remove_field(name, self.file_name)

        self.selected_cache.discard(diag.name)

    def _get_regional_value(self) -> str:
        """Get regional section value from config widgets."""
        regional_widgets = self.file_config_widgets['regional']
        regional_type = regional_widgets['dropdown'].value

        if regional_type == 'none':
            return 'none'
        elif regional_type == 'global':
            return 'global'
        elif regional_type == 'box':
            lon_min = regional_widgets['lon_min'].value
            lon_max = regional_widgets['lon_max'].value
            lat_min = regional_widgets['lat_min'].value
            lat_max = regional_widgets['lat_max'].value
            vert_min = regional_widgets['vert_min'].value
            vert_max = regional_widgets['vert_max'].value
            return f'{lon_min} {lon_max} {lat_min} {lat_max} {vert_min} {vert_max}'

        return 'none'

    def _update_status(self):
        """Update the header with selection count."""
        count = len(self.selected_cache)
        self.header.value = f"<b style='color: #6c757d;'>Diagnostics (Selected: {count})</b>"
        if self.on_selection_change:
            self.on_selection_change()

    def _go_prev(self, button):
        """Go to previous page."""
        if self.current_page > 0:
            self.current_page -= 1
            self.update_diagnostics_list(reset_page=False)

    def _go_next(self, button):
        """Go to next page."""
        total_pages = (len(self.filtered_diags) + self.page_size - 1) // self.page_size
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.update_diagnostics_list(reset_page=False)

    def select_all_visible(self, button):
        """Select all visible diagnostics."""
        with self.diag_container.hold_sync():
            for name, cb in self.checkboxes_dict.items():
                if not cb.value:
                    cb.value = True

    def deselect_all(self, button):
        """Deselect all diagnostics."""
        with self.diag_container.hold_sync():
            for name, cb in self.checkboxes_dict.items():
                if cb.value:
                    cb.value = False

    def get_layout(self) -> widgets.VBox:
        """Get the complete diagnostic selector layout.

        Returns:
            VBox containing all diagnostic selector widgets
        """
        # Control buttons
        select_all_btn = create_button(
            'Select All Visible',
            button_style='info',
            icon='check-square',
            width='150px',
            on_click=self.select_all_visible
        )

        deselect_all_btn = create_button(
            'Deselect All',
            button_style='warning',
            icon='square',
            width='150px',
            on_click=self.deselect_all
        )

        return widgets.VBox([
            self.header,
            widgets.HBox(
                [self.search_widget, self.category_widget, self.dim_filter],
                layout=widgets.Layout(margin='0 0 10px 0')
            ),
            widgets.HBox(
                [select_all_btn, deselect_all_btn],
                layout=widgets.Layout(margin='0 0 10px 0')
            ),
            self.diag_container
        ])
