# Data Directory

This directory is for storing your MOM6 diagnostic files and generated outputs.

## Purpose

- Store your `available_diags` input files
- Save generated `diag_table` output files
- Keep cache files organized

## Recommended Structure

```
data/
├── available_diags.000000       # Your input diagnostic files
├── available_diags.000001
├── diag_table                   # Generated output files
├── diag_table_production
└── *.cache                      # Cache files (auto-generated)
```

## Usage Examples

### Store your diagnostics file here
```bash
cp /path/to/your/available_diags.000000 data/
```

### Use it in the UI
```python
from mom6_diagnostics_manager import create_diag_table_ui

ui = create_diag_table_ui('data/available_diags.000000')
```

### Save output to this directory
```python
# In the UI, specify output path as: data/diag_table
# Or use Python API:
from mom6_diagnostics_manager import DiagTableGenerator

gen = DiagTableGenerator(title="My Case")
# ... configure files and fields ...
gen.save('data/diag_table')
```

## Notes

- This directory is ignored by git (except this README)
- Place your input files and outputs here to keep the project organized
- Cache files (`.cache`) are automatically created and cleaned up
