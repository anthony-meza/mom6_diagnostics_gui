"""Tests for the DiagnosticsParser."""

import pytest
import tempfile
from pathlib import Path
from mom6_diagnostics_manager.core import DiagnosticsParser


@pytest.fixture
def sample_available_diags():
    """Create a sample available_diags file for testing."""
    content = """
"SSH" [Used]
  ! modules: ocean_model
  ! long_name: Sea Surface Height
  ! units: m
  ! dimensions: time, yh, xh
  ! standard_name: sea_surface_height

"temp" [Unused]
  ! modules: ocean_model
  ! long_name: Potential Temperature
  ! units: degC
  ! dimensions: time, zl, yh, xh
  ! cell_methods: time: mean

"geolon" [Used]
  ! modules: ocean_model
  ! long_name: Longitude of tracer (T) points
  ! units: degrees_east
  ! dimensions: yh, xh
"""

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(content)
        temp_path = f.name

    yield temp_path

    # Cleanup
    Path(temp_path).unlink()


class TestDiagnosticsParser:
    """Tests for DiagnosticsParser class."""

    def test_parser_creation(self, sample_available_diags):
        """Test creating a parser with a sample file."""
        parser = DiagnosticsParser(sample_available_diags)
        assert len(parser.diagnostics) == 3
        assert "SSH" in parser.diagnostics
        assert "temp" in parser.diagnostics
        assert "geolon" in parser.diagnostics

    def test_parse_metadata(self, sample_available_diags):
        """Test that metadata is correctly parsed."""
        parser = DiagnosticsParser(sample_available_diags)

        ssh = parser.diagnostics["SSH"]
        assert ssh.name == "SSH"
        assert ssh.used is True
        assert ssh.long_name == "Sea Surface Height"
        assert ssh.units == "m"
        assert "ocean_model" in ssh.modules

    def test_2d_3d_detection(self, sample_available_diags):
        """Test 2D/3D field detection."""
        parser = DiagnosticsParser(sample_available_diags)

        ssh = parser.diagnostics["SSH"]
        temp = parser.diagnostics["temp"]

        assert ssh.is_2d() is True
        assert ssh.is_3d() is False

        assert temp.is_3d() is True
        assert temp.is_2d() is False

    def test_used_unused_detection(self, sample_available_diags):
        """Test detection of used/unused fields."""
        parser = DiagnosticsParser(sample_available_diags)

        assert parser.diagnostics["SSH"].used is True
        assert parser.diagnostics["temp"].used is False
        assert parser.diagnostics["geolon"].used is True

    def test_category_organization(self, sample_available_diags):
        """Test that diagnostics are organized into categories."""
        parser = DiagnosticsParser(sample_available_diags)
        categories = parser.get_by_category()

        assert isinstance(categories, dict)

        # With simplified categories, we should have Grid & Static
        # geolon should be in Grid & Static
        assert "Grid & Static" in categories

        # Grid & Static should have geolon
        grid_diags = categories["Grid & Static"]
        assert any(d.name == 'geolon' for d in grid_diags)

    def test_file_not_found(self):
        """Test handling of nonexistent file."""
        with pytest.raises(FileNotFoundError):
            DiagnosticsParser("/nonexistent/path/to/file.txt")
