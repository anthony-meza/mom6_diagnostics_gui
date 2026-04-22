# Data Directory

This directory contains data files used by the MOM6 Diagnostic Tool.

## Contents

- **`available_diags.000000`** - Example MOM6 diagnostic file (included with package)
  - Used as the default when calling `create_diag_table_ui()` without arguments
  - Contains sample diagnostics from a MOM6 simulation
  - Great for testing and learning the tool

## Adding Your Own Files

Place your MOM6 `available_diags` files here for easy access when using the diagnostic tool.

## Example Usage

```python
from mom6_diagnostics_gui import create_diag_table_ui

# Option 1: Use the built-in example file (default)
ui = create_diag_table_ui()

# Option 2: Use your own file
ui = create_diag_table_ui('path/to/your/available_diags.000000')
```

## File Types

- `available_diags.*` - MOM6 diagnostic availability files
- Custom diagnostic files
- Configuration overrides (optional)

## Notes

- The example file `available_diags.000000` is included in version control
- Other data files you add here are ignored by git by default
- Cache files (`.cache`) are automatically generated for faster loading
