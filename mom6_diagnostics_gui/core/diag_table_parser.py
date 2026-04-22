"""Generator for MOM6 diag_table files."""

import csv
from pathlib import Path
from typing import List, Dict, Optional


class DiagTableGenerator:
    """Generator for MOM6 diag_table files.

    This class constructs a properly formatted diag_table file
    for MOM6 that specifies which diagnostic fields to output
    and at what frequency.

    Attributes:
        title: Title for the diag_table
        base_year: Base year for time axis
        base_month: Base month for time axis
        base_day: Base day for time axis
        files: List of file definitions
        fields: List of field definitions
    """

    def __init__(
        self,
        title: str = "MOM6 Simulation",
        base_year: int = 1900,
        base_month: int = 1,
        base_day: int = 1,
    ):
        """Initialize the generator.

        Args:
            title: Title for the diag_table
            base_year: Base year for time axis
            base_month: Base month for time axis
            base_day: Base day for time axis
        """
        self.title = title
        self.base_year = base_year
        self.base_month = base_month
        self.base_day = base_day
        self.files: List[Dict] = []
        self.fields: List[Dict] = []

    def clear(self):
        """Clear all files and fields."""
        self.files = []
        self.fields = []

    def add_file(
        self,
        file_name: str,
        output_freq: int,
        output_freq_units: str = "days",
        file_format: int = 1,
        time_axis_units: str = "days",
        time_axis_name: str = "time",
        new_file_freq: Optional[int] = None,
        new_file_freq_units: Optional[str] = None,
    ) -> Dict:
        """Add file definition.

        Args:
            file_name: Name of output file (can include date formatting like %4yr-%2mo-%2dy)
            output_freq: Frequency of output
            output_freq_units: Units for output frequency ('hours', 'days', 'months', 'years')
            file_format: Output file format (1=netCDF)
            time_axis_units: Units for time axis
            time_axis_name: Name of time axis variable
            new_file_freq: Optional frequency to create new files (for date formatting)
            new_file_freq_units: Optional units for new file frequency

        Returns:
            Dictionary containing the file definition

        Raises:
            ValueError: If parameters are invalid
        """
        # Validate inputs
        if not file_name:
            raise ValueError("file_name cannot be empty")

        valid_freq_units = ["hours", "days", "months", "years"]
        if output_freq_units not in valid_freq_units:
            raise ValueError(
                f"output_freq_units must be one of {valid_freq_units} and not {output_freq_units}"
            )

        if new_file_freq is not None and new_file_freq_units is None:
            raise ValueError(
                "new_file_freq_units must be specified when new_file_freq is provided"
            )

        # Check if file already exists
        for f in self.files:
            if f["file_name"] == file_name:
                return f

        file_def = {
            "file_name": file_name,
            "output_freq": output_freq,
            "output_freq_units": output_freq_units,
            "file_format": file_format,
            "time_axis_units": time_axis_units,
            "time_axis_name": time_axis_name,
            "new_file_freq": new_file_freq,
            "new_file_freq_units": new_file_freq_units,
        }
        self.files.append(file_def)
        return file_def

    def add_field(
        self,
        module_name: str,
        field_name: str,
        file_name: str,
        output_name: Optional[str] = None,
        time_sampling: str = "all",
        reduction_method: str = "none",
        regional_section: str = "none",
        packing: int = 2,
    ) -> Dict:
        """Add field definition.

        Args:
            module_name: Name of the module ('ocean_model', 'ocean_model_z', etc.)
            field_name: Name of the diagnostic field
            file_name: Name of output file to write to
            output_name: Name in output file (defaults to field_name)
            time_sampling: Time sampling method ('all', 'snapshot')
            reduction_method: Reduction method ('none', 'mean', 'min', 'max', 'sum', '.false.')
            regional_section: Regional section coordinates or 'none'
            packing: Packing precision (1=double, 2=float, 4=short, 8=byte)

        Returns:
            Dictionary containing the field definition

        Raises:
            ValueError: If parameters are invalid
        """
        # Validate inputs
        if not module_name:
            raise ValueError("module_name cannot be empty")
        if not field_name:
            raise ValueError("field_name cannot be empty")
        if not file_name:
            raise ValueError("file_name cannot be empty")

        valid_packing = [1, 2, 4, 8]
        if packing not in valid_packing:
            raise ValueError(f"packing must be one of {valid_packing}")

        if output_name is None:
            output_name = field_name

        # Check if field already exists in this file
        for f in self.fields:
            if f["field_name"] == field_name and f["file_name"] == file_name:
                return f

        field_def = {
            "module_name": module_name,
            "field_name": field_name,
            "output_name": output_name,
            "file_name": file_name,
            "time_sampling": time_sampling,
            "reduction_method": reduction_method,
            "regional_section": regional_section,
            "packing": packing,
        }
        self.fields.append(field_def)
        return field_def

    def remove_field(self, field_name: str, file_name: str):
        """Remove a field from a specific file.

        Args:
            field_name: Name of the diagnostic field
            file_name: Name of the file to remove it from
        """
        self.fields = [
            f
            for f in self.fields
            if not (f["field_name"] == field_name and f["file_name"] == file_name)
        ]

    def get_fields_for_file(self, file_name: str) -> List[Dict]:
        """Get all fields for a specific file.

        Args:
            file_name: Name of the file

        Returns:
            List of field definitions for this file
        """
        return [f for f in self.fields if f["file_name"] == file_name]

    def _format_file_line(self, file_def: Dict) -> str:
        """Format a file definition line for diag_table.

        Args:
            file_def: Dictionary containing file definition parameters

        Returns:
            Formatted file line string
        """
        base_line = (
            f'"{file_def["file_name"]}", '
            f'{file_def["output_freq"]}, '
            f'"{file_def["output_freq_units"]}", '
            f'{file_def["file_format"]}, '
            f'"{file_def["time_axis_units"]}", '
            f'"{file_def["time_axis_name"]}"'
        )

        if file_def["new_file_freq"] is not None:
            base_line += (
                f', {file_def["new_file_freq"]}, "{file_def["new_file_freq_units"]}"'
            )

        return base_line

    def _format_field_line(self, field_def: Dict) -> str:
        """Format a field definition line for diag_table.

        Args:
            field_def: Dictionary containing field definition parameters

        Returns:
            Formatted field line string
        """
        return (
            f'"{field_def["module_name"]}", '
            f'"{field_def["field_name"]}", '
            f'"{field_def["output_name"]}", '
            f'"{field_def["file_name"]}", '
            f'"{field_def["time_sampling"]}", '
            f'"{field_def["reduction_method"]}", '
            f'"{field_def["regional_section"]}", '
            f'{field_def["packing"]}'
        )

    def _group_fields_by_file(self) -> Dict[str, List[Dict]]:
        """Group field definitions by their output file.

        Returns:
            Dictionary mapping file names to lists of field definitions
        """
        files_with_fields = {}
        for field_def in self.fields:
            fname = field_def["file_name"]
            if fname not in files_with_fields:
                files_with_fields[fname] = []
            files_with_fields[fname].append(field_def)
        return files_with_fields

    def generate(self) -> str:
        """Generate diag_table content.

        Returns:
            String containing the complete diag_table file content
        """
        lines = []

        # Title section
        lines.append(self.title)
        lines.append(f"{self.base_year}  {self.base_month}  {self.base_day}  0  0  0")

        # File section header
        lines.append("### Section-1: File List")
        lines.append("#========================")

        # File sections
        for file_def in self.files:
            lines.append(self._format_file_line(file_def))

        lines.append("")

        # Field section header
        lines.append("### Section-2: Fields List")
        lines.append("#=========================")

        # Group fields by file for better organization
        files_with_fields = self._group_fields_by_file()

        # Field sections (organized by file)
        for fname, fields in files_with_fields.items():
            lines.append(f'# "{fname}"')
            for field_def in fields:
                lines.append(self._format_field_line(field_def))
            lines.append("")

        return "\n".join(lines)

    @classmethod
    def from_file(cls, filepath: str) -> "DiagTableGenerator":
        """Load a DiagTableGenerator from an existing diag_table file.

        Args:
            filepath: Path to an existing diag_table file

        Returns:
            DiagTableGenerator populated with the file's contents
        """
        lines = Path(filepath).read_text().splitlines()

        title = lines[0].strip()
        date_parts = lines[1].strip().split()
        base_year, base_month, base_day = (
            int(date_parts[0]),
            int(date_parts[1]),
            int(date_parts[2]),
        )

        generator = cls(
            title=title, base_year=base_year, base_month=base_month, base_day=base_day
        )

        in_files = False
        in_fields = False

        for line in lines[2:]:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                if "Section-1" in stripped:
                    in_files, in_fields = True, False
                elif "Section-2" in stripped:
                    in_files, in_fields = False, True
                continue

            row = [r.strip().strip('"') for r in next(csv.reader([stripped]))]

            if in_files:
                generator.add_file(
                    file_name=row[0],
                    output_freq=int(row[1]),
                    output_freq_units=row[2],
                    file_format=int(row[3]),
                    time_axis_units=row[4],
                    time_axis_name=row[5],
                    new_file_freq=int(row[6]) if len(row) > 6 else None,
                    new_file_freq_units=row[7] if len(row) > 7 else None,
                )
            elif in_fields:
                generator.add_field(
                    module_name=row[0],
                    field_name=row[1],
                    file_name=row[3],
                    output_name=row[2],
                    time_sampling=row[4],
                    reduction_method=row[5],
                    regional_section=row[6],
                    packing=int(row[7]),
                )

        return generator

    def save(self, filepath: str) -> str:
        """Save diag_table to file.

        Args:
            filepath: Path where to save the diag_table file

        Returns:
            Path to the saved file
        """
        content = self.generate()
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w") as f:
            f.write(content)
        return filepath
