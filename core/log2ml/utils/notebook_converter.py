#!/usr/bin/env python3
"""Notebook converter module for converting Jupyter notebooks to Python modules."""

import sys
import tempfile
from pathlib import Path
from typing import Tuple

import nbformat


def convert_notebook_to_module(
    notebook_path: str, output_path: str = None
) -> Tuple[str, str]:
    """
    Convert a Jupyter notebook to a Python module.

    Args:
        notebook_path: Path to the notebook file
        output_path: Optional path for the output Python file. If None, creates in temp directory.

    Returns:
        Tuple of (module_path, module_name)
    """
    # Read the notebook
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)

    # Create Python file content
    py_content = [
        "# Auto-generated from Jupyter notebook",
        "import pandas as pd",
        "import numpy as np",
        "from typing import List, Dict, Any\n",
        "def run_analysis(csv_path: str, model_type: str) -> Dict[str, Any]:",
        "    # Initialize result dictionary",
        "    result = {'charts': [], 'metrics': {}}\n",
    ]

    # Extract code cells
    for cell in nb.cells:
        if cell.cell_type == "code":
            # Skip cells with specific tags if they exist
            if "tags" in cell.metadata and "skip-conversion" in cell.metadata.tags:
                continue

            # Indent the code to be part of run_analysis function
            indented_code = "\n".join(
                "    " + line for line in cell.source.split("\n") if line.strip()
            )
            py_content.extend(
                [
                    "\n    # " + "-" * 46,  # 46 to account for 4-space indent
                    indented_code,
                ]
            )

    # Add return statement
    py_content.extend(["\n    return result"])

    # Create output path
    if output_path is None:
        # Create temporary directory if it doesn't exist
        temp_dir = Path(tempfile.gettempdir()) / "log2ml_notebooks"
        temp_dir.mkdir(parents=True, exist_ok=True)

        # Use notebook name for the Python file
        module_name = (
            Path(notebook_path).stem.replace(" ", "_").replace("(", "").replace(")", "")
        )
        output_path = str(temp_dir / f"{module_name}.py")

    # Write to Python file
    with open(output_path, "w") as f:
        f.write("\n".join(py_content))

    return output_path, Path(output_path).stem


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python notebook_converter.py <notebook_path> [output_path]")
        sys.exit(1)

    notebook_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    module_path, module_name = convert_notebook_to_module(notebook_path, output_path)
    print(f"Converted notebook to module: {module_path}")
