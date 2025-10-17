"""Constants and configuration for the MOM6 diagnostic tool."""

from typing import Dict, List, Tuple

# UI Configuration
UI_PAGE_SIZE = 5
UI_WIDTH_LEFT_PANEL = '350px'
UI_WIDTH_RIGHT_PANEL = 'calc(100% - 360px)'
UI_SELECTOR_HEIGHT = '160px'
UI_CONTAINER_MAX_HEIGHT = '400px'

# Color scheme
COLOR_PRIMARY = '#495057'
COLOR_SECONDARY = '#6c757d'
COLOR_SUCCESS = '#28a745'
COLOR_DANGER = '#dc3545'
COLOR_INFO = '#007bff'
COLOR_LIGHT_BG = '#f8f9fa'
COLOR_WHITE = '#ffffff'
COLOR_BORDER = '#dee2e6'

# Default file configurations
DEFAULT_STATIC_FILE = 'ocean_static'
DEFAULT_STATIC_FIELDS = ['deptho', 'geolon', 'geolat', 'wet']

# Default frequency units
FREQUENCY_UNITS = ['hours', 'days', 'months', 'years']

# Reduction methods
REDUCTION_METHODS = ['average', 'min', 'max', 'none']

# Packing options (label, value)
PACKING_OPTIONS: List[Tuple[str, int]] = [
    ('real*8', 1),
    ('real*4', 2),
    ('16-bit int', 4),
    ('1-byte', 8)
]

# Regional options
REGIONAL_OPTIONS = ['none', 'global', 'box']

# Default diag_table title template
DEFAULT_TITLE_TEMPLATE = "MOM6 diagnostic fields table for CESM case: {case_name}"
DEFAULT_CASE_NAME = "YOUR_CASE_NAME"

# Base time configuration
DEFAULT_BASE_YEAR = 1900
DEFAULT_BASE_MONTH = 1
DEFAULT_BASE_DAY = 1

# Cache configuration
CACHE_FILE_SUFFIX = '.cache'

# Dimension filters
DIMENSION_FILTERS = ['All', '2D Only', '3D Only']
VERTICAL_DIMENSIONS = ['zl', 'zi']

# File format
DEFAULT_FILE_FORMAT = 1  # netCDF

# Time axis defaults
DEFAULT_TIME_AXIS_UNITS = 'days'
DEFAULT_TIME_AXIS_NAME = 'time'

# Default packing
DEFAULT_PACKING = 2  # real*4

# Default time sampling
DEFAULT_TIME_SAMPLING = 'all'

# Module names
DEFAULT_MODULE = 'ocean_model'

# Category names for diagnostics
DIAGNOSTIC_CATEGORIES = [
    'All Diagnostics',
    'Temperature & Salinity',
    'Velocity & Transport',
    'Surface Properties',
    'Mixing & Diffusion',
    'Sea Ice',
    'Tracers',
    'Grid & Static',
    'Other'
]

# Example file configurations for default setup
DEFAULT_FILE_CONFIGS: List[Dict] = [
    {
        'name': 'ocean_static',
        'freq': -1,
        'units': 'months',
        'fields': [
            {'name': 'deptho', 'module': 'ocean_model', 'reduction': 'none'},
            {'name': 'geolon', 'module': 'ocean_model', 'reduction': 'none'},
            {'name': 'geolat', 'module': 'ocean_model', 'reduction': 'none'},
            {'name': 'wet', 'module': 'ocean_model', 'reduction': 'none'},
        ]
    },
    {
        'name': 'surf_%4yr_%3dy',
        'freq': 1,
        'units': 'hours',
        'new_file_freq': 1,
        'new_file_freq_units': 'months',
        'fields': [
            {'name': 'SSH', 'module': 'ocean_model', 'reduction': 'none'}
        ]
    },
    {
        'name': 'ocean_daily',
        'freq': 1,
        'units': 'days',
        'fields': [
            {'name': 'tos', 'module': 'ocean_model', 'reduction': 'mean'}
        ]
    },
    {
        'name': 'ocean_month',
        'freq': 1,
        'units': 'months',
        'fields': [
            {'name': 'thetao', 'module': 'ocean_model', 'reduction': 'mean'}
        ]
    },
    {
        'name': 'ocean_annual',
        'freq': 12,
        'units': 'months',
        'fields': [
            {'name': 'thetao', 'module': 'ocean_model', 'reduction': 'mean'}
        ]
    },
    {
        'name': 'ocean_Bering_Strait',
        'freq': 5,
        'units': 'days',
        'fields': [
            {
                'name': 'thetao',
                'module': 'ocean_model',
                'reduction': 'mean',
                'regional': '-171.4 -168.7 66.1 66.1 -1 -1'
            }
        ]
    }
]
