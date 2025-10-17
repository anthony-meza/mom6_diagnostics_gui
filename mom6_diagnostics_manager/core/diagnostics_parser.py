"""Parser for MOM6 available_diags files.

Parses MOM6's available_diags output into Diagnostic objects. Includes
intelligent caching using pickle for faster repeated loads.
"""

import re
from typing import Dict, List, Optional
from .diagnostic_field import Diagnostic
from .config_loader import get_config
from .cache_manager import CacheManager


class DiagnosticsParser:
    """Parse MOM6 available_diags files into structured Diagnostic objects.

    Extracts diagnostic metadata from MOM6's text output and provides
    categorization and caching functionality.

    Attributes:
        filepath: Path to the available_diags file
        diagnostics: Dict mapping diagnostic names to Diagnostic objects
        use_cache: Whether caching is enabled
        config: Configuration object
    """

    def __init__(self, filepath: str, use_cache: bool = True, config_path: Optional[str] = None):
        """Initialize parser and parse the file.

        Args:
            filepath: Path to the available_diags file
            use_cache: If True, use pickle cache for faster loading
            config_path: Optional path to custom config file
        """
        self.filepath = filepath
        self.diagnostics: Dict[str, Diagnostic] = {}
        self.use_cache = use_cache
        self.config = get_config(config_path)

        # Initialize cache manager
        cache_suffix = self.config.get('cache.suffix', '.cache')
        max_caches = self.config.get('cache.max_files', 6)
        self.cache = CacheManager(
            cache_path=filepath + cache_suffix,
            cache_suffix=cache_suffix,
            max_caches=max_caches
        )

        # Try to load from cache first
        if use_cache and self.cache.is_valid(filepath):
            cached_data = self.cache.load()
            if cached_data is not None:
                self.diagnostics = cached_data
                return

        # Otherwise parse the file
        self._parse()

        # Save to cache for next time
        if use_cache:
            self.cache.save(self.diagnostics)

    def _parse(self):
        """Parse the available_diags file."""
        with open(self.filepath, 'r') as f:
            lines = f.readlines()

        current_diag = None

        for line in lines:
            line = line.strip()

            # Check for diagnostic name
            if line.startswith('"') and '[' in line:
                match = re.match(r'"([^"]+)"\s+\[(Used|Unused)\]', line)
                if match:
                    name = match.group(1)
                    used = match.group(2) == "Used"
                    current_diag = Diagnostic(name=name, used=used)
                    self.diagnostics[name] = current_diag

            # Parse metadata
            elif line.startswith('!') and current_diag:
                self._parse_metadata(line, current_diag)

    def _parse_metadata(self, line: str, diag: Diagnostic):
        """Parse metadata line.

        Args:
            line: Metadata line starting with '!'
            diag: Diagnostic object to update
        """
        line = line.lstrip('! ').strip()

        # Extract key and value from the metadata line
        if ':' not in line:
            return

        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip()

        # Map metadata keys to their parsing methods
        metadata_handlers = {
            'modules': lambda v: self._parse_list_field(v),
            'dimensions': lambda v: v,
            'long_name': lambda v: v,
            'units': lambda v: v,
            'standard_name': lambda v: v,
            'cell_methods': lambda v: v,
            'variants': lambda v: self._parse_list_field(v),
        }

        if key in metadata_handlers:
            parsed_value = metadata_handlers[key](value)
            setattr(diag, key, parsed_value)

    def _parse_list_field(self, value: str) -> List[str]:
        """Parse a list field that may be in {item1, item2} format.

        Args:
            value: String that may contain comma-separated items in braces

        Returns:
            List of parsed items
        """
        match = re.search(r'\{([^}]+)\}', value)
        if match:
            return [item.strip() for item in match.group(1).split(',')]
        return [value.strip()] if value else []

    def clear_cache(self) -> bool:
        """Delete the cache file for this diagnostics file.

        Returns:
            True if cache was deleted, False if it didn't exist
        """
        return self.cache.clear()

    @staticmethod
    def clear_all_caches(directory: str = '.', suffix: str = '.cache') -> int:
        """Delete all cache files in a directory.

        Args:
            directory: Directory to search (default: current directory)
            suffix: Cache file suffix (default: '.cache')

        Returns:
            Number of cache files deleted
        """
        return CacheManager.clear_all(directory, suffix)

    def get_by_category(self) -> Dict[str, List[Diagnostic]]:
        """Organize diagnostics by categories based on keyword matching.

        Categories and keywords are defined in config.yml. Only returns
        non-empty categories. Each diagnostic assigned to first matching category.

        Returns:
            Dict mapping category names to lists of Diagnostic objects
        """
        # Load category keywords from config
        category_keywords = self.config.get_category_keywords()

        # Initialize only the categories we use
        categories = {}

        # Categorize diagnostics
        for diag in self.diagnostics.values():
            name_lower = diag.name.lower()

            # Check if it matches any category
            for category_name, keywords in category_keywords.items():
                if any(keyword in name_lower for keyword in keywords):
                    if category_name not in categories:
                        categories[category_name] = []
                    categories[category_name].append(diag)
                    break  # Each diagnostic in only one category

        # Only return non-empty categories
        return categories
