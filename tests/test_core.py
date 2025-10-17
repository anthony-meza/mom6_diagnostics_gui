"""Tests for core functionality."""

import pytest
from mom6_diagnostics_manager.core import Diagnostic, DiagTableGenerator


class TestDiagnostic:
    """Tests for Diagnostic class."""

    def test_diagnostic_creation(self):
        """Test creating a diagnostic."""
        diag = Diagnostic(
            name="SSH",
            used=True,
            dimensions="time, yh, xh",
            long_name="Sea Surface Height",
            units="m"
        )
        assert diag.name == "SSH"
        assert diag.used is True
        assert diag.is_2d() is True
        assert diag.is_3d() is False

    def test_3d_diagnostic(self):
        """Test 3D diagnostic detection."""
        diag = Diagnostic(
            name="temp",
            used=True,
            dimensions="time, zl, yh, xh",
        )
        assert diag.is_3d() is True
        assert diag.is_2d() is False


class TestDiagTableGenerator:
    """Tests for DiagTableGenerator class."""

    def test_generator_creation(self):
        """Test creating a generator."""
        gen = DiagTableGenerator(title="Test Case", base_year=2000)
        assert gen.title == "Test Case"
        assert gen.base_year == 2000
        assert len(gen.files) == 0
        assert len(gen.fields) == 0

    def test_add_file(self):
        """Test adding a file."""
        gen = DiagTableGenerator()
        gen.add_file("ocean_static", -1, "days")
        assert len(gen.files) == 1
        assert gen.files[0]["file_name"] == "ocean_static"
        assert gen.files[0]["output_freq"] == -1

    def test_add_field(self):
        """Test adding a field."""
        gen = DiagTableGenerator()
        gen.add_file("ocean_static", -1, "days")
        gen.add_field(
            module_name="ocean_model",
            field_name="SSH",
            file_name="ocean_static"
        )
        assert len(gen.fields) == 1
        assert gen.fields[0]["field_name"] == "SSH"

    def test_remove_field(self):
        """Test removing a field."""
        gen = DiagTableGenerator()
        gen.add_file("ocean_static", -1, "days")
        gen.add_field("ocean_model", "SSH", "ocean_static")
        gen.remove_field("SSH", "ocean_static")
        assert len(gen.fields) == 0

    def test_generate_output(self):
        """Test generating diag_table content."""
        gen = DiagTableGenerator(title="Test Case", base_year=2000)
        gen.add_file("ocean_static", -1, "days")
        gen.add_field("ocean_model", "SSH", "ocean_static")

        output = gen.generate()
        assert "Test Case" in output
        assert "2000" in output
        assert "ocean_static" in output
        assert "SSH" in output
