#!/usr/bin/env python3

import argparse
import os
import sys
from pathlib import Path

import pandas as pd

from log2ml.vectorizer.vectorizer import (create_bpe_tokenizer,
                                          create_linformer_model,
                                          process_input)


def vectorize_dataset(input_file, output_file, tokenizer_file):
    """Vectorize the text column of the dataset using BPE tokenization"""
    # Read the dataset
    df = pd.read_csv(input_file)
    messages = df["text"].tolist()

    # Create and train tokenizer
    tokenizer, trainer = create_bpe_tokenizer()
    tokenizer = tokenizer.train_from_iterator(messages, trainer=trainer)

    # Save tokenizer
    tokenizer.save(tokenizer_file)

    # Create model
    model = create_linformer_model()

    # Process each message
    vectors = []
    for message in messages:
        vector = process_input(message, tokenizer, model)
        vectors.append(vector.tolist())

    # Save results
    result_df = pd.DataFrame(vectors)
    result_df.to_csv(output_file, index=False)


def main():
    """Main function for vectorizing datasets"""
    parser = argparse.ArgumentParser(
        description="Vectorize text data using BPE tokenization and Linformer"
    )
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Input CSV file containing a 'text' column",
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="Output file for saving the vectors",
    )
    parser.add_argument(
        "--tokenizer",
        "-t",
        required=True,
        help="File to save the trained tokenizer",
    )

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file {args.input} does not exist")
        sys.exit(1)

    Path(args.output).parent.mkdir(exist_ok=True)
    Path(args.tokenizer).parent.mkdir(exist_ok=True)

    vectorize_dataset(args.input, args.output, args.tokenizer)


if __name__ == "__main__":
    main()
