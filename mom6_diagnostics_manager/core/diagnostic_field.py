"""Data structures for MOM6 diagnostic fields.

Defines the Diagnostic dataclass used to represent parsed diagnostic metadata
from MOM6's available_diags file.
"""

from dataclasses import dataclass, field
from typing import List
from .config_loader import get_config


@dataclass
class Diagnostic:
    """A single diagnostic field from MOM6 with all its metadata.

    Attributes:
        name: Diagnostic field name (e.g., 'SSH', 'thetao')
        used: Whether marked as 'Used' in available_diags
        modules: List of MOM6 modules this belongs to
        dimensions: Comma-separated dimensions (e.g., 'time, zl, yh, xh')
        long_name: Human-readable description
        units: Physical units (e.g., 'm', 'degC')
        standard_name: CF convention standard name
        cell_methods: Cell methods for averaging
        variants: Available variant field names
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
        """Check if diagnostic has vertical dimensions (zl, zi)."""
        config = get_config()
        vertical_dims = config.get_vertical_dimensions()
        return any(dim in self.dimensions for dim in vertical_dims)

    def is_2d(self) -> bool:
        """Check if diagnostic is 2D (no vertical dimensions)."""
        return not self.is_3d()

    def display_name(self) -> str:
        """Return formatted display string: 'name (2D/3D) [units] - description'."""
        dim_type = "3D" if self.is_3d() else "2D"
        units_str = f" [{self.units}]" if self.units else ""
        return f"{self.name} ({dim_type}){units_str} - {self.long_name[:60]}"

    def get_primary_name(self) -> str:
        """Get primary output name (first variant if available, else name)."""
        if self.variants and len(self.variants) > 0:
            return self.variants[0]
        return self.name
