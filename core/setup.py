from pathlib import Path

from setuptools import find_packages, setup

# Find README.md in parent directory or current directory
readme_path = Path(__file__).parent.parent / "README.md"
if not readme_path.exists():
    readme_path = Path(__file__).parent / "README.md"

# Read README.md if it exists, otherwise use a simple description
try:
    long_description = readme_path.read_text()
except FileNotFoundError:
    long_description = "A toolchain for converting log data into machine learning models using vector embeddings"

setup(
    name="log2ml",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "scikit-learn>=1.4.1",
        "flaml>=1.0.0",
        "nbformat>=5.9.0",
        "nbconvert>=7.7.0",
    ],
    author="MC",
    description="A toolchain for converting log data into machine learning models using vector embeddings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
