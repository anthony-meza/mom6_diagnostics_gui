# MOM6 Diagnostics Manager

<img width="949" height="629" alt="Screenshot 2025-10-18 at 3 26 10 PM" src="https://github.com/user-attachments/assets/96728a78-32e8-46d7-bbe2-3fb968e4c748" />

A tool for creating MOM6 `diag_table` files. Provides an interactive Jupyter interface, Python API, and command-line tool.

## Overview

Creating `diag_table` files for MOM6 by hand is tedious. This tool parses the `available_diags` output from MOM6 and lets you select diagnostics interactively or programmatically.

## Installation

```bash
# Clone the repository
git clone https://github.com/anthonymeza/CESM-diags-generator.git
cd CESM-diags-generator

# Install with conda (recommended)
conda env create -f environment.yml
conda activate mom6-diagnostics-manager
pip install -e .

# Or install with pip
pip install -e .
```

## Usage

### Interactive Interface

```python
from mom6_diagnostics_manager import create_diag_table_ui

# Use built-in example data
ui = create_diag_table_ui()

# Or use your own file
ui = create_diag_table_ui('available_diags.000000')
```


## Example diag_table Output

```
MOM6 diagnostic fields table for CESM case: NWA12
1900  1  1  0  0  0

### Section-1: File List
"ocean_daily", 1, "days", 1, "days", "time"
"ocean_static", -1, "months", 1, "days", "time"

### Section-2: Fields List
"ocean_model", "SSH", "SSH", "ocean_daily", "all", "mean", "none", 2
"ocean_model", "geolon", "geolon", "ocean_static", "all", "none", "none", 2
```

## Issues

Report bugs at: https://github.com/anthonymeza/CESM-diags-generator/issues

## License

MIT License

## Author

Anthony Meza
