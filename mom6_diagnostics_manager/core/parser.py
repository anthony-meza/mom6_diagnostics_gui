"""Parser for MOM6 available_diags files."""

import re
import pickle
import os
from typing import Dict, List, Optional
from .diagnostic import Diagnostic
from .config_loader import get_config


class DiagnosticsParser:
    """Parser for available_diags files from MOM6.

    This class parses the text output from MOM6's available_diags file
    which lists all available diagnostic fields and their metadata.

    Attributes:
        filepath: Path to the available_diags file
        diagnostics: Dictionary mapping diagnostic names to Diagnostic objects
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
        cache_suffix = self.config.get('cache.suffix', '.cache')
        self._cache_path = filepath + cache_suffix

        # Try to load from cache first
        if use_cache and self._load_from_cache():
            return

        # Otherwise parse the file
        self._parse()

        # Save to cache for next time
        if use_cache:
            self._save_to_cache()

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

    def _load_from_cache(self) -> bool:
        """Load diagnostics from pickle cache if available and valid.

        Returns:
            True if cache was loaded successfully, False otherwise
        """
        try:
            # Check if cache exists
            if not os.path.exists(self._cache_path):
                return False

            # Check if cache is newer than source file
            cache_mtime = os.path.getmtime(self._cache_path)
            source_mtime = os.path.getmtime(self.filepath)

            if cache_mtime < source_mtime:
                # Cache is outdated
                return False

            # Load from cache
            with open(self._cache_path, 'rb') as f:
                self.diagnostics = pickle.load(f)

            return True

        except Exception:
            # If anything goes wrong, just parse normally
            return False

    def _save_to_cache(self):
        """Save diagnostics to pickle cache."""
        try:
            with open(self._cache_path, 'wb') as f:
                pickle.dump(self.diagnostics, f, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception:
            # Silently ignore cache save errors
            pass

    def clear_cache(self) -> bool:
        """Delete the cache file for this diagnostics file.

        Returns:
            True if cache was deleted, False if it didn't exist

        Example:
            >>> parser = DiagnosticsParser('available_diags.000000')
            >>> parser.clear_cache()  # Remove cache file
            True
        """
        if os.path.exists(self._cache_path):
            try:
                os.remove(self._cache_path)
                return True
            except Exception as e:
                print(f"Warning: Could not delete cache file: {e}")
                return False
        return False

    @staticmethod
    def clear_all_caches(directory: str = '.', pattern: str = '*.cache') -> int:
        """Delete all cache files in a directory.

        Args:
            directory: Directory to search for cache files (default: current directory)
            pattern: Glob pattern for cache files (default: '*.cache')

        Returns:
            Number of cache files deleted

        Example:
            >>> DiagnosticsParser.clear_all_caches('.')
            3  # Deleted 3 cache files
        """
        from pathlib import Path
        count = 0
        cache_dir = Path(directory)

        for cache_file in cache_dir.glob(pattern):
            try:
                cache_file.unlink()
                count += 1
            except Exception as e:
                print(f"Warning: Could not delete {cache_file}: {e}")

        return count

    def get_by_category(self) -> Dict[str, List[Diagnostic]]:
        """Organize diagnostics by categories.

        Simple categorization: Grid & Static and everything else.
        Only returns categories that have diagnostics (dynamic).

        Returns:
            Dictionary mapping category names to lists of Diagnostic objects
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
