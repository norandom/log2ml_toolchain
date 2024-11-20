#!/bin/bash

# ANSI color codes
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored status messages
print_status() {
    echo -e "${BLUE}[*]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[+]${NC} $1"
}

print_error() {
    echo -e "${RED}[!]${NC} $1"
}

# Create necessary directories
print_status "Creating directories..."
mkdir -p data tokenizer

# Input file path
input_file="data/lab_logs_blindtest_activity_sysmon_1000samples_july_28_2024_filtered_clean.csv"
output_file="data/vectorized_sysmon_bpe.parquet"
tokenizer_file="tokenizer/sysmon_bpe.json"

# Check if input file exists
if [ ! -f "$input_file" ]; then
    print_error "Input file not found: $input_file"
    print_error "Please ensure the input file is present in the data directory."
    exit 1
fi

# Vectorize dataset using BPE tokenization
print_status "Vectorizing dataset using BPE tokenization..."
python ./tools/vectorize_dataset.py \
    --input "$input_file" \
    --output "$output_file" \
    --tokenizer "$tokenizer_file" \
    || { print_error "Failed to vectorize dataset"; exit 1; }

print_success "Vectorization completed successfully"
print_success "Output saved to: $output_file"
