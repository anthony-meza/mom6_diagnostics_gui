"""Configuration loader for MOM6 diagnostic tool.

This module handles loading configuration from YAML files, with fallback
to built-in constants if the config file is not available.
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Optional
import yaml


class Config:
    """Configuration manager for the MOM6 diagnostic tool.

    This class loads configuration from a YAML file and provides
    easy access to configuration values with fallback to defaults.

    Attributes:
        config_data: Dictionary containing all configuration values
    """

    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration.

        Args:
            config_path: Path to custom config file. If None, uses package default.
        """
        self.config_data = self._load_config(config_path)

    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from YAML file.

        Args:
            config_path: Path to custom config file

        Returns:
            Dictionary containing configuration values

        Raises:
            FileNotFoundError: If custom config_path is specified but doesn't exist
        """
        # Default config location
        if config_path is None:
            package_dir = Path(__file__).parent.parent
            config_path = package_dir / 'config.yml'

        config_file = Path(config_path)

        if not config_file.exists():
            if config_path is not None:
                raise FileNotFoundError(f"Config file not found: {config_path}")
            # Fall back to built-in default values
            from . import default_values
            return self._fallback_config(default_values)

        try:
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing config file: {e}")

    def _fallback_config(self, constants) -> Dict[str, Any]:
        """Create fallback config from constants module.

        Args:
            constants: Constants module

        Returns:
            Dictionary with configuration
        """
        return {
            'dimensions': {
                'vertical': constants.VERTICAL_DIMENSIONS
            },
            'defaults': {
                'base_year': constants.DEFAULT_BASE_YEAR,
                'base_month': constants.DEFAULT_BASE_MONTH,
                'base_day': constants.DEFAULT_BASE_DAY,
                'file_format': constants.DEFAULT_FILE_FORMAT,
                'time_axis_units': constants.DEFAULT_TIME_AXIS_UNITS,
                'time_axis_name': constants.DEFAULT_TIME_AXIS_NAME,
                'packing': constants.DEFAULT_PACKING,
                'time_sampling': constants.DEFAULT_TIME_SAMPLING,
                'module': constants.DEFAULT_MODULE,
            },
            'ui': {
                'page_size': constants.UI_PAGE_SIZE,
                'width_left_panel': constants.UI_WIDTH_LEFT_PANEL,
                'selector_height': constants.UI_SELECTOR_HEIGHT,
                'container_max_height': constants.UI_CONTAINER_MAX_HEIGHT,
            },
            'cache': {
                'enabled': True,
                'suffix': constants.CACHE_FILE_SUFFIX
            }
        }

    def get(self, key_path: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation.

        Args:
            key_path: Path to config value using dots (e.g., 'defaults.base_year')
            default: Default value if key not found

        Returns:
            Configuration value or default

        Example:
            >>> config = Config()
            >>> config.get('defaults.base_year')
            1900
            >>> config.get('ui.page_size', 10)
            5
        """
        keys = key_path.split('.')
        value = self.config_data

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def get_category_keywords(self) -> Dict[str, List[str]]:
        """Get diagnostic category keywords.

        Returns:
            Dictionary mapping category names to keyword lists
        """
        return self.config_data.get('category_keywords', {})

    def use_dynamic_categories(self) -> bool:
        """Check if categories should be dynamic (only show non-empty).

        Returns:
            True if only non-empty categories should be shown
        """
        return self.get('categories.dynamic_only', True)

    def allow_multiple_categories(self) -> bool:
        """Check if diagnostics can appear in multiple categories.

        Returns:
            True if diagnostics can appear in multiple categories
        """
        return self.get('categories.allow_multiple', False)

    def get_vertical_dimensions(self) -> List[str]:
        """Get list of vertical dimension names.

        Returns:
            List of dimension names that indicate 3D fields
        """
        return self.get('dimensions.vertical', ['zl', 'zi'])

    def get_default_files(self) -> List[Dict[str, Any]]:
        """Get default file configurations.

        Returns:
            List of file configuration dictionaries
        """
        return self.get('default_files', [])

    def get_ui_colors(self) -> Dict[str, str]:
        """Get UI color scheme.

        Returns:
            Dictionary mapping color names to hex codes
        """
        return self.get('ui.colors', {})

    def get_packing_options(self) -> List[Dict[str, Any]]:
        """Get packing options for UI.

        Returns:
            List of packing option dictionaries
        """
        return self.get('options.packing', [])


# Global config instance
_config_instance: Optional[Config] = None


def get_config(config_path: Optional[str] = None) -> Config:
    """Get the global configuration instance.

    Args:
        config_path: Optional path to custom config file

    Returns:
        Config instance
    """
    global _config_instance

    if _config_instance is None or config_path is not None:
        _config_instance = Config(config_path)

    return _config_instance


def reload_config(config_path: Optional[str] = None):
    """Reload configuration from file.

    Args:
        config_path: Optional path to custom config file
    """
    global _config_instance
    _config_instance = Config(config_path)
