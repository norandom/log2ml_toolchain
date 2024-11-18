#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}Log2ML Toolchain - Vectorizer Demo${NC}"
echo "=================================="
echo

# Display the first few lines of the sample log file
echo -e "${GREEN}Sample log entries:${NC}"
head -n 3 sample_data/sample_logs.log
echo "..."
echo

# Function to display last entry with truncated vector
display_last_entry() {
    local parquet_file=$1
    local title=$2
    echo -e "${GREEN}$title${NC}"
    python3 -c "
import pandas as pd
import numpy as np
df = pd.read_parquet('$parquet_file')
last_row = df.iloc[-1]
vector_preview = np.array2string(np.array(last_row['vector'][:10]), precision=4, suppress_small=True)
print(f'Text: {last_row[\"text\"]}')
print(f'Vector (first 10 dimensions): {vector_preview}...')
"
    echo
}

# Default word tokenization
echo -e "${GREEN}1. Using default word tokenization...${NC}"
cat sample_data/sample_logs.log | ./tools/vectorizer > vectorized_logs_word.parquet

if [ $? -eq 0 ]; then
    display_last_entry "vectorized_logs_word.parquet" "Last entry (word tokenization):"
else
    echo "Error during word tokenization vectorization"
    exit 1
fi

# BPE tokenization (training new tokenizer)
echo -e "${GREEN}2. Training and using BPE tokenization...${NC}"
cat sample_data/sample_logs.log | ./tools/vectorizer -bpe tokenizer.json > vectorized_logs_bpe.parquet

if [ $? -eq 0 ]; then
    display_last_entry "vectorized_logs_bpe.parquet" "Last entry (BPE tokenization):"
else
    echo "Error during BPE tokenization vectorization"
    exit 1
fi

# Using saved BPE tokenizer
echo -e "${GREEN}3. Using saved BPE tokenizer...${NC}"
cat sample_data/sample_logs.log | ./tools/vectorizer -bpe tokenizer.json > vectorized_logs_bpe2.parquet

if [ $? -eq 0 ]; then
    display_last_entry "vectorized_logs_bpe2.parquet" "Last entry (saved BPE tokenizer):"
else
    echo "Error during second BPE tokenization vectorization"
    exit 1
fi
