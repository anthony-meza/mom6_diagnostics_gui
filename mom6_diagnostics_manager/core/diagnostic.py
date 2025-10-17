"""Core diagnostic data structures."""

from dataclasses import dataclass, field
from typing import List
from .config_loader import get_config


@dataclass
class Diagnostic:
    """Represents a single diagnostic field from MOM6.

    Attributes:
        name: The diagnostic field name
        used: Whether the diagnostic is currently used
        modules: List of modules this diagnostic belongs to
        dimensions: Dimension string (e.g., 'time, zl, yh, xh')
        long_name: Human-readable description
        units: Physical units
        standard_name: CF standard name if applicable
        cell_methods: Cell methods for time/space averaging
        variants: List of available variants
    """
    name: str
    used: bool
    modules: List[str] = field(default_factory=list)
    dimensions: str = ""
    long_name: str = ""
    units: str = ""
    standard_name: str = ""
    cell_methods: str = ""
    variants: List[str] = field(default_factory=list)

    def is_3d(self) -> bool:
        """Check if diagnostic is 3D.

        Returns:
            True if diagnostic has vertical dimensions (from config)
        """
        config = get_config()
        vertical_dims = config.get_vertical_dimensions()
        return any(dim in self.dimensions for dim in vertical_dims)

    def is_2d(self) -> bool:
        """Check if diagnostic is 2D.

        Returns:
            True if diagnostic does not have vertical dimensions
        """
        return not self.is_3d()

    def display_name(self) -> str:
        """Return formatted display name with metadata.

        Returns:
            Formatted string with dimension type, units, and description
        """
        dim_type = "3D" if self.is_3d() else "2D"
        units_str = f" [{self.units}]" if self.units else ""
        return f"{self.name} ({dim_type}){units_str} - {self.long_name[:60]}"

    def get_primary_name(self) -> str:
        """Get the primary field name (first variant if available, otherwise name).

        Returns:
            The first variant if variants exist, otherwise the diagnostic name
        """
        if self.variants and len(self.variants) > 0:
            return self.variants[0]
        return self.name
