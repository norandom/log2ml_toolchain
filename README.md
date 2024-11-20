# Log2ML Toolchain

### Build Status
[![Build and Test](https://github.com/norandom/log2ml_toolchain/actions/workflows/build.yml/badge.svg)](https://github.com/norandom/log2ml_toolchain/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/norandom/log2ml_toolchain/branch/main/graph/badge.svg)](https://codecov.io/gh/norandom/log2ml_toolchain)

### Code Quality
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Flake8](https://img.shields.io/badge/Flake8-passing-brightgreen.svg)](https://flake8.pycqa.org/)
[![cargo clippy](https://img.shields.io/badge/clippy-passing-brightgreen.svg)](https://github.com/rust-lang/rust-clippy)

### Testing
[![pytest](https://img.shields.io/badge/pytest-passing-brightgreen.svg)](https://docs.pytest.org/)
[![Coverage](https://img.shields.io/badge/Coverage-80%25-brightgreen.svg)](https://coverage.readthedocs.io/)
[![cargo test](https://img.shields.io/badge/cargo%20test-passing-brightgreen.svg)](https://doc.rust-lang.org/cargo/commands/cargo-test.html)

### Technologies
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?&logo=PyTorch&logoColor=white)](https://pytorch.org/)
[![Rust](https://img.shields.io/badge/Rust-000000?logo=rust&logoColor=white)](https://www.rust-lang.org/)
[![Tauri](https://img.shields.io/badge/Tauri-FFC131?logo=Tauri&logoColor=white)](https://tauri.studio/)
[![Node.js](https://img.shields.io/badge/Node.js-43853D?logo=node.js&logoColor=white)](https://nodejs.org/)
[![Bash](https://img.shields.io/badge/Shell_Script-121011?logo=gnu-bash&logoColor=white)](https://www.gnu.org/software/bash/)

A toolchain for converting log data into machine learning models using vector embeddings.

## Features

- Convert log data into vector embeddings
- Automatic model generation using AutoML
- Interactive visualization of embeddings
- Model performance analysis
- Seamless integration with Jupyter notebooks

## Project Structure

```
log2ml_toolchain/
├── core/                   # Python package
│   ├── log2ml/            # Main package code
│   │   ├── utils/         # Utility functions
│   │   └── vectorizer/    # Vectorization logic
│   ├── tests/             # Test suite
│   │   ├── unit/         # Unit tests
│   │   └── integration/  # Integration tests
│   └── requirements-dev.txt
├── gui/                    # Tauri-based GUI
│   └── vector-analyzer/   # Vector analysis interface
├── notebooks/             # Jupyter notebooks
├── sample_data/           # Example datasets
├── sample_models/         # Example models
└── scripts/               # Utility scripts
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mc/log2ml_toolchain.git
cd log2ml_toolchain
```

2. Install Python dependencies:
```bash
cd core
pip install -r requirements-dev.txt
pip install -e .
cd ..
```

3. Install GUI dependencies:
```bash
cd gui/vector-analyzer
yarn install
cd ../..
```

## Development

### Quality Assurance

Run all quality checks locally:
```bash
./scripts/qa.sh
```

This will:
- Format Python code with `black`
- Sort imports with `isort`
- Run Python linting with `flake8`
- Run Python tests with `pytest`
- Format Rust code with `cargo fmt`
- Run Rust linting with `clippy`

### Running the GUI

Start the Vector Analyzer GUI:
```bash
./scripts/start_gui.sh
```

## Usage

1. Place your log data in CSV format in the `sample_data/` directory
2. Start the GUI using `./scripts/start_gui.sh`
3. Load your data and select the desired model type
4. Analyze the results in the interactive visualization

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Run quality checks (`./scripts/qa.sh`)
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
