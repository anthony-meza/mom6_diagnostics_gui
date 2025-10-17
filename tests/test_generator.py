"""Tests for the DiagTableGenerator."""

import pytest
import tempfile
from pathlib import Path
from mom6_diagnostics_manager.core import DiagTableGenerator


class TestDiagTableGenerator:
    """Tests for DiagTableGenerator class."""

    def test_basic_creation(self):
        """Test creating a basic generator."""
        gen = DiagTableGenerator(
            title="Test Simulation",
            base_year=2000,
            base_month=1,
            base_day=1
        )
        assert gen.title == "Test Simulation"
        assert gen.base_year == 2000
        assert gen.base_month == 1
        assert gen.base_day == 1

    def test_add_static_file(self):
        """Test adding a static file."""
        gen = DiagTableGenerator()
        gen.add_file("ocean_static", -1, "days")

        assert len(gen.files) == 1
        file_def = gen.files[0]
        assert file_def["file_name"] == "ocean_static"
        assert file_def["output_freq"] == -1
        assert file_def["output_freq_units"] == "days"

    def test_add_daily_file(self):
        """Test adding a daily output file."""
        gen = DiagTableGenerator()
        gen.add_file(
            "ocean_daily",
            output_freq=1,
            output_freq_units="days",
            new_file_freq=1,
            new_file_freq_units="months"
        )

        assert len(gen.files) == 1
        file_def = gen.files[0]
        assert file_def["file_name"] == "ocean_daily"
        assert file_def["output_freq"] == 1
        assert file_def["new_file_freq"] == 1
        assert file_def["new_file_freq_units"] == "months"

    def test_add_field_default_output_name(self):
        """Test adding a field with default output name."""
        gen = DiagTableGenerator()
        gen.add_file("ocean_static", -1, "days")
        gen.add_field(
            module_name="ocean_model",
            field_name="SSH",
            file_name="ocean_static"
        )

        assert len(gen.fields) == 1
        field_def = gen.fields[0]
        assert field_def["field_name"] == "SSH"
        assert field_def["output_name"] == "SSH"
        assert field_def["module_name"] == "ocean_model"
        assert field_def["file_name"] == "ocean_static"

    def test_add_field_custom_output_name(self):
        """Test adding a field with custom output name."""
        gen = DiagTableGenerator()
        gen.add_file("ocean_static", -1, "days")
        gen.add_field(
            module_name="ocean_model",
            field_name="SSH",
            output_name="sea_surface_height",
            file_name="ocean_static"
        )

        field_def = gen.fields[0]
        assert field_def["field_name"] == "SSH"
        assert field_def["output_name"] == "sea_surface_height"

    def test_add_field_with_reduction(self):
        """Test adding a field with reduction method."""
        gen = DiagTableGenerator()
        gen.add_file("ocean_daily", 1, "days")
        gen.add_field(
            module_name="ocean_model",
            field_name="SSH",
            file_name="ocean_daily",
            reduction_method="mean"
        )

        field_def = gen.fields[0]
        assert field_def["reduction_method"] == "mean"

    def test_remove_field(self):
        """Test removing a field."""
        gen = DiagTableGenerator()
        gen.add_file("ocean_static", -1, "days")
        gen.add_field("ocean_model", "SSH", "ocean_static")
        gen.add_field("ocean_model", "geolon", "ocean_static")

        assert len(gen.fields) == 2

        gen.remove_field("SSH", "ocean_static")
        assert len(gen.fields) == 1
        assert gen.fields[0]["field_name"] == "geolon"

    def test_get_fields_for_file(self):
        """Test getting fields for a specific file."""
        gen = DiagTableGenerator()
        gen.add_file("ocean_static", -1, "days")
        gen.add_file("ocean_daily", 1, "days")

        gen.add_field("ocean_model", "SSH", "ocean_daily")
        gen.add_field("ocean_model", "geolon", "ocean_static")
        gen.add_field("ocean_model", "geolat", "ocean_static")

        daily_fields = gen.get_fields_for_file("ocean_daily")
        static_fields = gen.get_fields_for_file("ocean_static")

        assert len(daily_fields) == 1
        assert len(static_fields) == 2
        assert daily_fields[0]["field_name"] == "SSH"

    def test_clear(self):
        """Test clearing all configuration."""
        gen = DiagTableGenerator()
        gen.add_file("ocean_static", -1, "days")
        gen.add_field("ocean_model", "SSH", "ocean_static")

        gen.clear()

        assert len(gen.files) == 0
        assert len(gen.fields) == 0

    def test_generate_basic_output(self):
        """Test generating basic diag_table output."""
        gen = DiagTableGenerator(title="Test Case", base_year=2000)
        gen.add_file("ocean_static", -1, "days")
        gen.add_field("ocean_model", "SSH", "ocean_static", reduction_method=".false.")

        output = gen.generate()

        # Check title section
        assert "Test Case" in output
        assert "2000  1  1  0  0  0" in output

        # Check file section
        assert '"ocean_static", -1, "days"' in output

        # Check field section
        assert '"ocean_model"' in output
        assert '"SSH"' in output
        assert '"ocean_static"' in output

    def test_generate_multi_file_output(self):
        """Test generating output with multiple files."""
        gen = DiagTableGenerator(title="Multi-File Test")
        gen.add_file("ocean_static", -1, "days")
        gen.add_file("ocean_daily", 1, "days", new_file_freq=1, new_file_freq_units="months")

        gen.add_field("ocean_model", "geolon", "ocean_static")
        gen.add_field("ocean_model", "SSH", "ocean_daily", reduction_method="mean")

        output = gen.generate()

        assert '"ocean_static"' in output
        assert '"ocean_daily"' in output
        assert "geolon" in output
        assert "SSH" in output
        assert "mean" in output

    def test_save_to_file(self):
        """Test saving diag_table to file."""
        gen = DiagTableGenerator(title="Save Test")
        gen.add_file("ocean_static", -1, "days")
        gen.add_field("ocean_model", "SSH", "ocean_static")

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_diag_table"
            saved_path = gen.save(str(filepath))

            assert Path(saved_path).exists()

            # Read back and verify
            with open(saved_path, 'r') as f:
                content = f.read()

            assert "Save Test" in content
            assert "ocean_static" in content
            assert "SSH" in content

    def test_duplicate_file_handling(self):
        """Test that duplicate files are not added."""
        gen = DiagTableGenerator()
        gen.add_file("ocean_static", -1, "days")
        gen.add_file("ocean_static", -1, "days")  # Duplicate

        assert len(gen.files) == 1

    def test_duplicate_field_handling(self):
        """Test that duplicate fields are not added."""
        gen = DiagTableGenerator()
        gen.add_file("ocean_static", -1, "days")
        gen.add_field("ocean_model", "SSH", "ocean_static")
        gen.add_field("ocean_model", "SSH", "ocean_static")  # Duplicate

        assert len(gen.fields) == 1
