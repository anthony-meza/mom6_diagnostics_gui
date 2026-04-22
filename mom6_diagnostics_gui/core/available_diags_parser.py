"""Parser for MOM6 available_diags files."""

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Diagnostic:
    """A single diagnostic field from MOM6 with all its metadata."""

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
        return any(dim in self.dimensions for dim in ["zl", "zi"])

    def display_name(self) -> str:
        dim_type = "3D" if self.is_3d() else "2D"
        units_str = f" [{self.units}]" if self.units else ""
        return f"{self.name} ({dim_type}){units_str} - {self.long_name[:60]}"

    def get_primary_name(self) -> str:
        if self.variants:
            return self.variants[0]
        return self.name


def _load_category_keywords() -> Dict[str, List[str]]:
    return {
        "Grid & Static": ["geo", "depth", "area", "wet", "mask", "grid", "static"],
    }


class AvailableDiagsParser:
    """Parse MOM6 available_diags files into structured Diagnostic objects."""

    def __init__(self, filepath: Optional[str] = None):
        """Initialize parser and parse the file.

        Args:
            filepath: Path to the available_diags file. If None, creates an empty parser.
        """
        self.filepath = filepath
        self.diagnostics: Dict[str, Diagnostic] = {}

        if filepath is not None:
            self._parse()

    def _parse(self):
        with open(self.filepath, "r") as f:
            lines = f.readlines()

        current_diag = None
        for line in lines:
            line = line.strip()
            if line.startswith('"') and "[" in line:
                match = re.match(r'"([^"]+)"\s+\[(Used|Unused)\]', line)
                if match:
                    current_diag = Diagnostic(
                        name=match.group(1), used=match.group(2) == "Used"
                    )
                    self.diagnostics[current_diag.name] = current_diag
            elif line.startswith("!") and current_diag:
                self._parse_metadata(line, current_diag)

    def _parse_metadata(self, line: str, diag: Diagnostic):
        line = line.lstrip("! ").strip()
        if ":" not in line:
            return
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        handlers = {
            "modules": self._parse_list_field,
            "variants": self._parse_list_field,
            "dimensions": lambda v: v,
            "long_name": lambda v: v,
            "units": lambda v: v,
            "standard_name": lambda v: v,
            "cell_methods": lambda v: v,
        }
        if key in handlers:
            setattr(diag, key, handlers[key](value))

    def _parse_list_field(self, value: str) -> List[str]:
        match = re.search(r"\{([^}]+)\}", value)
        if match:
            return [item.strip() for item in match.group(1).split(",")]
        return [value.strip()] if value else []

    def get_by_category(self) -> Dict[str, List[Diagnostic]]:
        category_keywords = _load_category_keywords()
        categories: Dict[str, List[Diagnostic]] = {}
        for diag in self.diagnostics.values():
            name_lower = diag.name.lower()
            for category_name, keywords in category_keywords.items():
                if any(keyword in name_lower for keyword in keywords):
                    categories.setdefault(category_name, []).append(diag)
                    break
        return categories
