# Contributing to MOM6 Diagnostic Table Generator

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/CESM-diags-generator.git
   cd CESM-diags-generator
   ```

3. Create a development environment:
   ```bash
   conda env create -f environment.yml
   conda activate mom6-diagnostics-manager
   pip install -e ".[dev]"
   ```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Follow the existing code style
- Write clear, descriptive commit messages
- Add tests for new functionality
- Update documentation as needed

### 3. Run Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=mom6_diagnostics_manager tests/

# Run specific test file
pytest tests/test_parser.py
```

### 4. Code Quality Checks

```bash
# Format code with black
black mom6_diagnostics_manager/

# Check code style with flake8
flake8 mom6_diagnostics_manager/ --max-line-length=100

# Type checking with mypy
mypy mom6_diagnostics_manager/
```

### 5. Submit a Pull Request

1. Push your branch to your fork
2. Open a pull request against the `main` branch
3. Describe your changes clearly in the PR description
4. Link any related issues

## Code Style Guidelines

### Python Code

- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Maximum line length: 100 characters
- Use descriptive variable and function names
- Add docstrings to all public functions and classes

Example:
```python
def parse_diagnostic(line: str, current_diag: Diagnostic) -> bool:
    """Parse a diagnostic line from available_diags file.

    Args:
        line: Line from the file to parse
        current_diag: Current diagnostic object being populated

    Returns:
        True if line was successfully parsed, False otherwise

    Raises:
        ValueError: If line format is invalid
    """
    # Implementation here
    pass
```

### Documentation

- Use clear, concise language
- Include code examples where helpful
- Keep the README up to date
- Add docstrings to all modules, classes, and functions

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line should be 50 characters or less
- Reference issues and pull requests liberally

Good examples:
```
Add support for regional sections in diag_table
Fix parser crash on malformed input
Update documentation for new UI features
```

## Testing Guidelines

### Writing Tests

- Write tests for all new features
- Use pytest fixtures for common setup
- Test both success and error cases
- Keep tests focused and independent

Example:
```python
def test_parser_valid_diagnostic():
    """Test parser correctly handles valid diagnostic entry."""
    parser = DiagnosticsParser('test_data/available_diags.txt')
    assert 'SSH' in parser.diagnostics
    assert parser.diagnostics['SSH'].units == 'm'
```

### Test Organization

```
tests/
├── test_parser.py       # Parser tests
├── test_generator.py    # Generator tests
├── test_diagnostic.py   # Diagnostic class tests
├── test_integration.py  # Integration tests
└── fixtures/            # Test data files
```

## Architecture Overview

### Core Components

1. **Diagnostic**: Data class representing a single diagnostic field
2. **DiagnosticsParser**: Parses MOM6's available_diags file
3. **DiagTableGenerator**: Generates diag_table files
4. **DiagTableUI**: Interactive Jupyter widget interface

### Adding New Features

#### Adding a New Diagnostic Category

1. Update `constants.py` with new keywords
2. Update `parser.py` to handle the new category
3. Add tests for the new category
4. Update documentation

#### Adding a New UI Widget

1. Create widget in `interactive.py`
2. Connect to appropriate callbacks
3. Test in Jupyter notebook
4. Document the new widget

## Project Structure

```
mom6_diagnostics_manager/
├── core/
│   ├── constants.py      # Configuration constants
│   ├── diagnostic.py     # Diagnostic data class
│   ├── parser.py         # Parser implementation
│   └── generator.py      # Generator implementation
├── ui/
│   └── interactive.py    # Jupyter UI widgets
└── cli/
    └── main.py          # CLI entry point
```

## Documentation

### Code Documentation

All public APIs should have comprehensive docstrings:

```python
class DiagTableGenerator:
    """Generator for MOM6 diag_table files.

    This class constructs properly formatted diag_table files for MOM6
    that specify which diagnostic fields to output and at what frequency.

    Attributes:
        title: Title for the diag_table
        base_year: Base year for time axis
        files: List of file definitions
        fields: List of field definitions

    Example:
        >>> gen = DiagTableGenerator(title="My Simulation")
        >>> gen.add_file('ocean_daily', 1, 'days')
        >>> gen.add_field('ocean_model', 'SSH', 'ocean_daily')
        >>> gen.save('diag_table')
    """
```

### User Documentation

Update README.md when adding:
- New features
- New command-line options
- Breaking changes
- Important bug fixes

## Release Process

1. Update version in `setup.py` and `meta.yaml`
2. Update `CHANGELOG.md` with release notes
3. Create a git tag: `git tag -a v0.2.0 -m "Release version 0.2.0"`
4. Push tag: `git push origin v0.2.0`
5. Build and upload conda package

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
