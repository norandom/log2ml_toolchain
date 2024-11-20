#!/bin/bash

# Exit on error
set -e

echo "🔍 Running Quality Assurance Checks..."

# Python QA
echo "\n📝 Running Python Checks..."
cd ../core

echo "Installing dependencies..."
python -m pip install --quiet --upgrade pip
pip install --quiet -r requirements-dev.txt
pip install --quiet -e .

echo "Running Black formatter..."
black .

echo "Running isort..."
isort .

echo "Running flake8..."
flake8 log2ml/ tests/ --max-line-length=100 --extend-ignore=E203 --statistics --show-source --count

echo "Running pytest..."
pytest tests/ --cov=log2ml --cov-report=xml

cd ../gui/vector-analyzer/src-tauri

# Rust QA
echo "\n🦀 Running Rust Checks..."

echo "Running cargo fmt..."
cargo fmt --all

echo "Running clippy..."
cargo clippy -- -D warnings

echo "\n✅ All checks completed successfully!"
