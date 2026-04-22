"""Reusable widget components for the MOM6 diagnostic UI.

This module provides common widget builders and utilities used across
the interactive interface.
"""

import ipywidgets as widgets
from typing import List, Tuple, Optional, Callable


def create_text_widget(
    value: str = "",
    placeholder: str = "",
    description: str = "",
    width: str = "100%",
    description_width: str = "100px",
) -> widgets.Text:
    """Create a styled text input widget.

    Args:
        value: Initial value
        placeholder: Placeholder text
        description: Label text
        width: Widget width
        description_width: Label width

    Returns:
        Configured Text widget
    """
    return widgets.Text(
        value=value,
        placeholder=placeholder,
        description=description,
        layout=widgets.Layout(width=width),
        style={"description_width": description_width},
    )


def create_dropdown(
    options: List,
    value: Optional[str] = None,
    description: str = "",
    width: str = "100%",
    description_width: str = "160px",
    disabled: bool = False,
) -> widgets.Dropdown:
    """Create a styled dropdown widget.

    Args:
        options: List of options
        value: Initial selected value
        description: Label text
        width: Widget width
        description_width: Label width
        disabled: Whether widget is disabled

    Returns:
        Configured Dropdown widget
    """
    kwargs = {
        "options": options,
        "description": description,
        "layout": widgets.Layout(width=width),
        "style": {"description_width": description_width},
        "disabled": disabled,
    }
    if value is not None:
        kwargs["value"] = value

    return widgets.Dropdown(**kwargs)


def create_button(
    description: str,
    button_style: str = "",
    icon: str = "",
    width: str = "100%",
    on_click: Optional[Callable] = None,
    disabled: bool = False,
) -> widgets.Button:
    """Create a styled button widget.

    Args:
        description: Button text
        button_style: Style ('success', 'info', 'warning', 'danger')
        icon: Font Awesome icon name
        width: Button width
        on_click: Click handler function
        disabled: Whether button is disabled

    Returns:
        Configured Button widget
    """
    button = widgets.Button(
        description=description,
        button_style=button_style,
        icon=icon,
        layout=widgets.Layout(width=width),
        disabled=disabled,
    )

    if on_click:
        button.on_click(on_click)

    return button


def create_html_label(
    text: str, color: str = "#495057", size: str = "inherit", bold: bool = False
) -> widgets.HTML:
    """Create a styled HTML label.

    Args:
        text: Label text
        color: Text color (hex)
        size: Font size
        bold: Whether text is bold

    Returns:
        HTML widget with styled text
    """
    weight = "bold" if bold else "normal"
    return widgets.HTML(
        f"<span style='color: {color}; font-size: {size}; font-weight: {weight};'>{text}</span>"
    )


def create_status_html(message: str, status: str = "success") -> widgets.HTML:
    """Create a status message widget.

    Args:
        message: Status message
        status: Status type ('success', 'error', 'info')

    Returns:
        HTML widget with colored status message
    """
    colors = {
        "success": "#28a745",
        "error": "#dc3545",
        "info": "#007bff",
        "warning": "#ffc107",
    }

    icons = {"success": "✓", "error": "✗", "info": "ℹ", "warning": "⚠"}

    color = colors.get(status, colors["info"])
    icon = icons.get(status, "")

    return widgets.HTML(f"<span style='color: {color};'>{icon} {message}</span>")


def create_section_header(text: str, subtitle: str = "") -> widgets.HTML:
    """Create a section header with optional subtitle.

    Args:
        text: Main header text
        subtitle: Optional subtitle text

    Returns:
        HTML widget with formatted header
    """
    subtitle_html = (
        f" <span style='color: #6c757d; font-size: 0.9em;'>{subtitle}</span>"
        if subtitle
        else ""
    )
    return widgets.HTML(f"<b style='color: #495057;'>{text}</b>{subtitle_html}")


def create_help_text(text: str) -> widgets.HTML:
    """Create a help text widget.

    Args:
        text: Help text content

    Returns:
        HTML widget with styled help text
    """
    return widgets.HTML(
        f"<div style='background: #f8f9fa; padding: 10px; border-radius: 4px; "
        f"margin-bottom: 10px; font-size: 0.9em;'>{text}</div>"
    )


def create_accordion(
    title: str, content: widgets.Widget, selected_index: Optional[int] = None
) -> widgets.Accordion:
    """Create an accordion widget.

    Args:
        title: Accordion title
        content: Widget to place inside
        selected_index: Initial selected index (None for collapsed)

    Returns:
        Configured Accordion widget
    """
    accordion = widgets.Accordion(children=[content])
    accordion.set_title(0, title)
    if selected_index is not None:
        accordion.selected_index = selected_index
    return accordion


def create_scrollable_container(
    children: List[widgets.Widget], max_height: str = "400px"
) -> widgets.VBox:
    """Create a scrollable container.

    Args:
        children: List of widgets to contain
        max_height: Maximum height before scrolling

    Returns:
        VBox with scroll capabilities
    """
    return widgets.VBox(
        children,
        layout=widgets.Layout(
            max_height=max_height,
            overflow_y="auto",
            border="1px solid #dee2e6",
            border_radius="4px",
            padding="10px",
            background_color="#fafafa",
        ),
    )


def create_hbox_row(
    *widgets_list, spacing: str = "0", justify_content: str = "flex-start"
) -> widgets.HBox:
    """Create a horizontal box layout.

    Args:
        *widgets_list: Widgets to place horizontally
        spacing: Spacing between widgets
        justify_content: Horizontal alignment ('flex-start', 'center', 'flex-end', 'space-between')

    Returns:
        HBox with widgets
    """
    return widgets.HBox(
        list(widgets_list), layout=widgets.Layout(margin=f"0 0 {spacing} 0")
    )


def create_vbox_column(*widgets_list, spacing: str = "0") -> widgets.VBox:
    """Create a vertical box layout.

    Args:
        *widgets_list: Widgets to place vertically
        spacing: Spacing between widgets

    Returns:
        VBox with widgets
    """
    return widgets.VBox(
        list(widgets_list), layout=widgets.Layout(margin=f"0 0 {spacing} 0")
    )


def create_pagination_controls(
    current_page: int,
    total_pages: int,
    on_prev: Callable,
    on_next: Callable,
    item_start: int,
    item_end: int,
    total_items: int,
) -> Tuple[widgets.HTML, widgets.HBox]:
    """Create pagination controls with page info.

    Args:
        current_page: Current page number (0-indexed)
        total_pages: Total number of pages
        on_prev: Callback for previous button
        on_next: Callback for next button
        item_start: Starting item index (1-indexed for display)
        item_end: Ending item index
        total_items: Total number of items

    Returns:
        Tuple of (page_info HTML widget, pagination buttons HBox)
    """
    page_info = widgets.HTML(
        f"<div style='text-align: center; margin: 10px 0; color: #6c757d;'>"
        f"Page {current_page + 1} of {total_pages} "
        f"(showing {item_start}-{item_end} of {total_items})"
        f"</div>"
    )

    prev_btn = create_button(
        "← Previous", disabled=(current_page == 0), width="48%", on_click=on_prev
    )

    next_btn = create_button(
        "Next →",
        disabled=(current_page >= total_pages - 1),
        width="48%",
        on_click=on_next,
    )

    pagination = widgets.HBox([prev_btn, next_btn])

    return page_info, pagination


def create_number_input(
    value: int,
    description: str = "",
    width: str = "48%",
    disabled: bool = False,
    description_width: str = "160px",
) -> widgets.IntText:
    """Create a number input widget.

    Args:
        value: Initial value
        description: Label text
        width: Widget width
        disabled: Whether widget is disabled
        description_width: Label width

    Returns:
        IntText widget
    """
    return widgets.IntText(
        value=value,
        description=description,
        disabled=disabled,
        layout=widgets.Layout(width=width),
        style={"description_width": description_width},
    )


def create_float_input(
    value: float,
    description: str = "",
    width: str = "48%",
    description_width: str = "160px",
) -> widgets.FloatText:
    """Create a float input widget.

    Args:
        value: Initial value
        description: Label text
        width: Widget width
        description_width: Label width

    Returns:
        FloatText widget
    """
    return widgets.FloatText(
        value=value,
        description=description,
        layout=widgets.Layout(width=width),
        style={"description_width": description_width},
    )
