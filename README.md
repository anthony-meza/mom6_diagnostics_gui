# MOM6 Diagnostics Manager

A tool for creating MOM6 `diag_table` files. Provides an interactive Jupyter interface, Python API, and command-line tool.

## Overview

Creating `diag_table` files for MOM6 by hand is tedious. This tool parses the `available_diags` output from MOM6 and lets you select diagnostics interactively or programmatically.

## Features

- Interactive Jupyter UI for browsing and selecting diagnostics
- Filter by category or dimension (2D/3D)
- Configure multiple output files with different frequencies
- Python API for scripting
- Built-in example data for testing

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

### Python API

```python
from mom6_diagnostics_manager import DiagnosticsParser, DiagTableGenerator

parser = DiagnosticsParser('available_diags.000000')
gen = DiagTableGenerator(title="MOM6 diag table for NWA12", base_year=1900)

gen.add_file('ocean_daily', 1, 'days')
gen.add_field('ocean_model', 'SSH', 'ocean_daily', reduction_method='mean')
gen.save('diag_table')
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

## Troubleshooting

**UI not displaying in Jupyter:**
```bash
jupyter nbextension enable --py widgetsnbextension
```

For JupyterLab:
```bash
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

**Slow first load:** Large `available_diags` files are cached after the first load.

## Issues

Report bugs at: https://github.com/anthonymeza/CESM-diags-generator/issues

## License

MIT License

## Author

Anthony Meza
