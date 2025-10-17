"""Cache management for diagnostic files.

Handles pickle caching of parsed diagnostics with automatic cleanup
to limit the number of cache files.
"""

import pickle
import os
from pathlib import Path
from typing import Any, Optional


class CacheManager:
    """Manage cache files for diagnostic parsing.

    Handles saving, loading, and cleanup of cache files with a
    configurable limit on the number of cache files kept.
    """

    def __init__(self, cache_path: str, cache_suffix: str = '.cache', max_caches: int = 6):
        """Initialize cache manager.

        Args:
            cache_path: Full path to the cache file
            cache_suffix: Suffix for cache files (default: '.cache')
            max_caches: Maximum number of cache files to keep (default: 6)
        """
        self.cache_path = cache_path
        self.cache_suffix = cache_suffix
        self.max_caches = max_caches

    def load(self) -> Optional[Any]:
        """Load data from cache if available and valid.

        Returns:
            Cached data if valid, None otherwise
        """
        try:
            # Check if cache exists
            if not os.path.exists(self.cache_path):
                return None

            # Load from cache
            with open(self.cache_path, 'rb') as f:
                return pickle.load(f)

        except Exception:
            # If anything goes wrong, return None
            return None

    def is_valid(self, source_path: str) -> bool:
        """Check if cache is newer than source file.

        Args:
            source_path: Path to the source file

        Returns:
            True if cache is valid (newer than source)
        """
        try:
            if not os.path.exists(self.cache_path):
                return False

            cache_mtime = os.path.getmtime(self.cache_path)
            source_mtime = os.path.getmtime(source_path)

            return cache_mtime >= source_mtime

        except Exception:
            return False

    def save(self, data: Any):
        """Save data to cache and cleanup old caches.

        Args:
            data: Data to cache (must be pickleable)
        """
        try:
            # Save to cache
            with open(self.cache_path, 'wb') as f:
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

            # Clean up old caches
            self.cleanup()

        except Exception:
            # Silently ignore cache save errors
            pass

    def cleanup(self):
        """Remove oldest cache files if we exceed the limit."""
        try:
            # Get directory containing this cache file
            cache_dir = Path(self.cache_path).parent

            # Find all cache files with this suffix
            cache_files = list(cache_dir.glob(f'*{self.cache_suffix}'))

            # If we have more than max_caches, remove oldest ones
            if len(cache_files) > self.max_caches:
                # Sort by modification time (oldest first)
                cache_files.sort(key=lambda p: p.stat().st_mtime)

                # Remove oldest files until we're at the limit
                files_to_remove = len(cache_files) - self.max_caches
                for cache_file in cache_files[:files_to_remove]:
                    try:
                        cache_file.unlink()
                    except Exception:
                        pass  # Ignore errors removing old caches

        except Exception:
            # Silently ignore cleanup errors
            pass

    def clear(self) -> bool:
        """Delete this cache file.

        Returns:
            True if cache was deleted, False if it didn't exist
        """
        if os.path.exists(self.cache_path):
            try:
                os.remove(self.cache_path)
                return True
            except Exception:
                return False
        return False

    @staticmethod
    def clear_all(directory: str = '.', suffix: str = '.cache') -> int:
        """Delete all cache files in a directory.

        Args:
            directory: Directory to search (default: current directory)
            suffix: Cache file suffix (default: '.cache')

        Returns:
            Number of cache files deleted
        """
        count = 0
        cache_dir = Path(directory)

        for cache_file in cache_dir.glob(f'*{suffix}'):
            try:
                cache_file.unlink()
                count += 1
            except Exception:
                pass

        return count
