"""Setup configuration for mom6_diagnostics_gui package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (
    (this_directory / "README.md").read_text()
    if (this_directory / "README.md").exists()
    else ""
)

setup(
    name="mom6-diagnostics-gui",
    version="0.1.0",
    author="Anthony Meza",
    author_email="",
    description="Interactive diagnostic gui for MOM6 ocean model - create and manage diag_table files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anthonymeza/CESM-diags-generator",
    packages=find_packages(exclude=["tests", "examples"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.3.0",
        "ipywidgets>=7.6.0",
        "IPython>=7.16.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.10",
            "black>=21.0",
            "flake8>=3.9",
            "mypy>=0.900",
        ],
        "notebook": [
            "jupyter>=1.0.0",
            "notebook>=6.0.0",
        ],
    },
    include_package_data=True,
    keywords="MOM6 oceanography climate modeling CESM diagnostics",
    project_urls={
        "Bug Reports": "https://github.com/anthonymeza/CESM-diags-generator/issues",
        "Source": "https://github.com/anthonymeza/CESM-diags-generator",
        "Documentation": "https://github.com/anthonymeza/CESM-diags-generator#readme",
    },
)
