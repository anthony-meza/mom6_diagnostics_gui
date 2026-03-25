# Changes — 2026-03-25

## Goal
Allow `create_diag_table_ui` to accept an existing `diag_table` file as the starting point instead of the hardcoded default collection.

---

## Files changed

### `mom6_diagnostics_manager/core/diag_table_writer.py`
- Added `DiagTableGenerator.from_file(filepath)` classmethod
- Parses an existing `diag_table` file (title, base date, all file/field entries) and returns a populated `DiagTableGenerator`
- Uses Python's `csv` module to handle quoted fields including regional sections with spaces (e.g. `"-171.4 -168.7 66.1 66.1 -1 -1"`)

### `mom6_diagnostics_manager/ui/main_interface.py`

**`create_diag_table_ui`** — added `input_diag_table=None` parameter:
- If provided, calls `DiagTableGenerator.from_file(input_diag_table)` to seed the UI from that file
- If not provided, falls back to the existing default behavior (`_add_default_files`)

Usage:
```python
create_diag_table_ui(input_diag_table="/path/to/existing/diag_table")
```

**`_add_default_files`** — simplified:
- Removed its own hardcoded copy of the 6 default files
- Now reads from `DEFAULT_FILE_CONFIGS` in `default_values.py` (was duplicated in both places before)

---

## Remaining duplication (not touched)
`DEFAULT_FILE_CONFIGS` in `default_values.py` and the `default_files` section in `config.yml` still define the same 6 files independently. The config loader has a `get_default_files()` method that reads from YAML but nothing calls it. Worth cleaning up eventually but out of scope for now.
