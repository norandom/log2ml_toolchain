#!/usr/bin/env python3

import os
import sys
import argparse
import pandas as pd
from pathlib import Path
from tools.vectorizer import (
    create_linformer_model,
    create_bpe_tokenizer,
    train_bpe_tokenizer,
    process_input,
)

def vectorize_dataset(input_file, output_file, tokenizer_file):
    """Vectorize the text column of the dataset using BPE tokenization"""
    # Read the dataset
    print(f"Reading dataset from {input_file}...")
    df = pd.read_csv(input_file)
    messages = df['text'].tolist()
    
    # Initialize model
    print("Initializing Linformer model...")
    model = create_linformer_model()
    
    # Create and train BPE tokenizer
    print("Creating and training BPE tokenizer...")
    tokenizer, trainer = create_bpe_tokenizer()
    print("Training on text data...")
    tokenizer = train_bpe_tokenizer(tokenizer, trainer, "\n".join(messages))
    
    # Save the tokenizer
    print(f"Saving BPE tokenizer to {tokenizer_file}...")
    tokenizer.save(str(tokenizer_file))
    
    # Process messages
    print("Vectorizing text with BPE tokenization...")
    vectors = []
    total = len(messages)
    
    for i, message in enumerate(messages, 1):
        if i % 100 == 0:
            print(f"Processing text {i}/{total}")
        vector = process_input(message, tokenizer, model)
        vectors.append(vector.tolist())
    
    # Create output DataFrame
    print("Creating output DataFrame...")
    output_df = pd.DataFrame({
        'text': messages,
        'vector': vectors
    })
    
    # Save to parquet
    print(f"Saving to {output_file}...")
    output_df.to_parquet(output_file, index=False)
    print("Done!")

def main():
    parser = argparse.ArgumentParser(description='Vectorize Log2ML dataset text using BPE tokenization')
    parser.add_argument('--input', type=str,
                       default='data/lab_logs_blindtest_activity_sysmon_1000samples_july_28_2024_filtered_clean.csv',
                       help='Input CSV file path')
    parser.add_argument('--output', type=str,
                       default='data/vectorized_sysmon_bpe.parquet',
                       help='Output Parquet file path')
    parser.add_argument('--tokenizer', type=str,
                       default='tokenizer/sysmon_bpe.json',
                       help='Path to save the trained BPE tokenizer')
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file {args.input} not found.")
        print("Please run tools/download_dataset.py first.")
        sys.exit(1)
    
    # Create output directories if they don't exist
    Path(args.output).parent.mkdir(exist_ok=True)
    Path(args.tokenizer).parent.mkdir(exist_ok=True)
    
    vectorize_dataset(args.input, args.output, args.tokenizer)

if __name__ == '__main__':
    main()
