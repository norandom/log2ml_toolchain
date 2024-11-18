# Log2ML Toolchain

A collection of tools for converting log data into machine learning-ready formats.

## Tools

### Vectorizer

The vectorizer tool converts log file entries into vector representations using Linformer. It supports both word-level and BPE (Byte-Pair Encoding) tokenization.

#### Features

- Line-by-line log file processing
- Word-level tokenization (default)
- BPE tokenization with training capability
- Parquet output format with both text and vector data
- Linformer-based vectorization with configurable parameters

#### Usage

1. Default word tokenization:
```bash
cat logfile.log | ./tools/vectorizer > output.parquet
```

2. Train and use BPE tokenization:
```bash
cat logfile.log | ./tools/vectorizer -bpe tokenizer.json > output.parquet
```

3. Use existing BPE tokenizer:
```bash
cat logfile.log | ./tools/vectorizer -bpe existing_tokenizer.json > output.parquet
```

#### Output Format

The tool generates a Parquet file containing:
- `text`: Original log entry text
- `vector`: Vector representation (30,000 dimensions)

#### Model Configuration

- Vocabulary Size: 30,000 tokens
- Maximum Sequence Length: 700
- Embedding Dimension: 64
- Attention Heads: 4
- Transformer Layers: 2
- Activation: GELU

## Directory Structure

```
log2ml_toolchain/
├── tools/
│   └── vectorizer        # Main vectorization tool
├── sample_data/
│   └── sample_logs.log   # Example log file
├── requirements.txt      # Python dependencies
└── vectorizer_demo.sh    # Demo script
```

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Demo

Run the demo script to see the vectorizer in action:
```bash
./vectorizer_demo.sh
```

The demo shows:
1. Default word tokenization
2. Training and using a new BPE tokenizer
3. Reusing a saved BPE tokenizer

## Dependencies

- torch
- linformer-pytorch
- pandas
- pyarrow
- tokenizers

## Development

### Setup Development Environment

1. Clone the repository
2. Install development dependencies:
```bash
pip install -r requirements.txt -r requirements-dev.txt
```

### Running Tests

Run the test suite:
```bash
pytest tests/
```

Run tests with coverage:
```bash
pytest tests/ --cov=tools --cov-report=term-missing
```

### Code Quality

Format code:
```bash
black tools/ tests/
isort tools/ tests/
```

Run linting:
```bash
flake8 tools/ tests/ --max-line-length=100
```

## CI/CD

This project uses GitHub Actions for continuous integration and delivery. The pipeline includes:

1. Testing
   - Runs test suite on Python 3.8, 3.9, 3.10, and 3.11
   - Generates coverage reports
   - Uploads coverage to Codecov

2. Linting
   - Black for code formatting
   - isort for import sorting
   - flake8 for code quality

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

MIT License
