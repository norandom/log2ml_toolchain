# Log2ML Toolchain

A command-line tool for converting log files into machine learning-ready vector representations using Linformer.

## Features

- Convert log files to fixed-size vector representations
- Support for both word-level and BPE tokenization
- Output in Parquet format with original text and vectors
- Pipe-compatible for Unix-style workflows
- Configurable tokenization and model parameters

## Quick Start

```bash
# Basic usage with word tokenization
cat sample_data/sample_logs.log | ./tools/vectorizer > data/vectors.parquet

# Using BPE tokenization (training new tokenizer)
cat sample_data/sample_logs.log | ./tools/vectorizer -bpe tokenizer/my_tokenizer.json > data/vectors_bpe.parquet

# Using pre-trained BPE tokenizer
cat sample_data/sample_logs.log | ./tools/vectorizer -bpe tokenizer/existing_tokenizer.json > data/vectors_bpe2.parquet
```

## Installation

### Prerequisites

- Python 3.10 or 3.11
- CUDA-capable GPU (recommended)
- Unix-like system

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/log2ml_toolchain.git
cd log2ml_toolchain
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Technical Details

### Model Architecture

- **Tokenization**:
  - Word-level tokenizer (default)
  - BPE tokenizer with configurable vocabulary
  - Special token support: [PAD], [UNK], [CLS], [SEP], [MASK]

- **Linformer Configuration**:
  - Vocabulary Size: 30,000 tokens
  - Maximum Sequence Length: 700 tokens
  - Embedding Dimensions: 64 channels
  - Attention Heads: 4
  - Transformer Layers: 2
  - Activation: GELU

### Output Format

The tool outputs Parquet files with two columns:
- `text`: Original log line
- `vector`: Fixed-size vector representation (30,000 dimensions)

## Directory Structure

```
log2ml_toolchain/
├── tools/
│   └── vectorizer        # Main vectorization tool
├── data/
│   └── *.parquet        # Generated vector data files
├── tokenizer/
│   └── *.json          # Trained tokenizer files
├── sample_data/
│   └── sample_logs.log  # Example log file
├── tests/
│   └── test_vectorizer.py  # Test suite
├── requirements.txt      # Python dependencies
├── requirements-dev.txt  # Development dependencies
└── vectorizer_demo.sh    # Demo script
```

## Development

### Setup Development Environment

1. Install development dependencies:
```bash
pip install -r requirements.txt -r requirements-dev.txt
```

### Running Tests

```bash
# Run test suite
pytest tests/

# Run with coverage
pytest tests/ --cov=tools --cov-report=term-missing
```

### Code Quality

```bash
# Format code
black tools/ tests/
isort tools/ tests/

# Run linting
flake8 tools/ tests/ --max-line-length=100
```

## CI/CD

GitHub Actions workflow includes:
- Testing on Python 3.10 and 3.11
- Code coverage reporting
- Automatic code formatting
- Linting checks

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## Dependencies

### Core Dependencies
- torch (>=2.0.0)
- linformer-pytorch (>=0.1.0)
- pandas (>=2.0.0)
- pyarrow (>=14.0.1)
- tokenizers (>=0.15.0)

### Development Dependencies
- pytest (>=7.0.0)
- black (>=23.0.0)
- isort (>=5.12.0)
- flake8 (>=6.0.0)
- coverage (>=7.0.0)

## License

MIT License - see [LICENSE](LICENSE) for details
