# MOM6 Diagnostics Manager

A tool for creating MOM6 `diag_table` using an interactive Jupyter interface

<img width="949" height="629" alt="Screenshot 2025-10-18 at 3 26 10 PM" src="https://github.com/user-attachments/assets/96728a78-32e8-46d7-bbe2-3fb968e4c748" />


## Overview

Creating `diag_table` files for MOM6 by hand can be tedious. This tool parses the `available_diags` output from MOM6 and lets you select diagnostics interactively.

## Installation

```bash
# Clone the repository
git clone https://github.com/anthonymeza/CESM-diags-generator.git
cd CESM-diags-generator

# Install with conda (recommended)
conda env create -f environment.yml
conda activate mom6-diagnostics-gui
pip install -e .

# Or install with pip
pip install -e .
```

## Usage

### Interactive Interface
Try the notebook in `examples/`!

```python
from mom6_diagnostics_gui import create_diag_table_ui

# Use built-in example data
ui = create_diag_table_ui()

# Or use your own file
ui = create_diag_table_ui('available_diags.000000')
```


## License

MIT License

## Author

Anthony Meza
