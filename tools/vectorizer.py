#!/usr/bin/env python3

import sys
import torch
import argparse
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from linformer_pytorch import LinformerLM
from tokenizers import Tokenizer, models, trainers, pre_tokenizers
from tokenizers.models import WordLevel, BPE
from tokenizers.pre_tokenizers import Whitespace, ByteLevel
from tokenizers.trainers import BpeTrainer


def create_linformer_model():
    """Create and initialize Linformer model for vectorization"""
    model = LinformerLM(
        num_tokens=30000,      # Number of tokens in the LM
        input_size=700,        # Dimension 1 of the input
        channels=64,           # Dimension 2 of the input
        dim_d=None,           # Overwrites the inner dim of the attention heads
        dim_k=128,            # The second dimension of the P_bar matrix
        dim_ff=128,           # Dimension in the feed forward network
        dropout_ff=0.15,      # Dropout for feed forward network
        nhead=4,              # Number of attention heads
        depth=2,              # How many times to run the model
        dropout=0.1,          # How much dropout to apply to P_bar after softmax
        activation="gelu",    # What activation to use
        checkpoint_level="C0", # What checkpoint level to use
        parameter_sharing="layerwise", # What level of parameter sharing to use
        k_reduce_by_layer=0,  # Going down depth, how much to reduce dim_k by
        full_attention=False, # Use full attention instead
        include_ff=True,     # Whether or not to include the Feed Forward layer
        w_o_intermediate_dim=None, # If not None, have 2 w_o matrices
        emb_dim=128,         # Embedding dimension
        causal=False,        # If you want this to be a causal Linformer
        method="learnable",  # The method of how to perform the projection
        ff_intermediate=None # Feed forward intermediate dimension
    )
    return model


def create_word_tokenizer():
    """Create a simple word-level tokenizer"""
    tokenizer = Tokenizer(WordLevel())
    tokenizer.pre_tokenizer = Whitespace()
    return tokenizer


def create_bpe_tokenizer():
    """Create a BPE tokenizer with trainer"""
    tokenizer = Tokenizer(BPE())
    trainer = BpeTrainer(
        vocab_size=30000,
        min_frequency=2,
        special_tokens=["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]"],
    )
    return tokenizer, trainer


def train_bpe_tokenizer(tokenizer, trainer, text):
    """Train BPE tokenizer on input text"""
    tokenizer.train_from_iterator([text], trainer=trainer)
    return tokenizer


def load_bpe_tokenizer(path):
    """Load a saved BPE tokenizer"""
    return Tokenizer.from_file(path)


def process_input(text, tokenizer, model):
    """Process a single line of text into a vector"""
    # Tokenize input
    encoding = tokenizer.encode(text)
    input_ids = encoding.ids[:700]  # Truncate to max length
    
    # Pad sequence if needed
    if len(input_ids) < 700:
        input_ids = input_ids + [0] * (700 - len(input_ids))
    
    # Convert to tensor and get embedding
    input_tensor = torch.tensor(input_ids).unsqueeze(0)  # Add batch dimension
    with torch.no_grad():
        embeddings = model(input_tensor)

    # Average pooling over sequence length
    embeddings = embeddings.mean(dim=1).squeeze(0)
    return embeddings.numpy()


def process_log_file(text, tokenizer, model):
    """Process log file line by line"""
    lines = text.strip().split("\n")
    vectors = []

    for line in lines:
        if line.strip():
            vector = process_input(line, tokenizer, model)
            vectors.append(vector)

    return lines, vectors


def main():
    parser = argparse.ArgumentParser(description="Vectorize log data using Linformer")
    parser.add_argument(
        "-bpe",
        type=str,
        help="Path to BPE tokenizer JSON file or to save new BPE tokenizer",
    )
    args = parser.parse_args()

    # Read input text
    text = sys.stdin.read()

    # Initialize model
    model = create_linformer_model()

    # Handle tokenizer initialization
    if args.bpe:
        if args.bpe.endswith(".json") and os.path.exists(args.bpe):
            # Load existing BPE tokenizer
            tokenizer = load_bpe_tokenizer(args.bpe)
        else:
            # Create and train new BPE tokenizer
            tokenizer, trainer = create_bpe_tokenizer()
            tokenizer = train_bpe_tokenizer(tokenizer, trainer, text)
            # Save the trained tokenizer
            tokenizer.save(args.bpe)
    else:
        # Use default word tokenizer
        tokenizer = create_word_tokenizer()

    # Process the input text line by line
    lines, vectors = process_log_file(text, tokenizer, model)

    # Convert vectors to list format for proper serialization
    vectors_list = [v.tolist() for v in vectors]

    # Create DataFrame
    df = pd.DataFrame({"text": lines, "vector": vectors_list})

    # Write to parquet file using pyarrow
    import pyarrow as pa
    import pyarrow.parquet as pq

    # Convert pandas DataFrame to Arrow Table
    table = pa.Table.from_pandas(df)

    # Write to a temporary buffer first
    buffer = pa.BufferOutputStream()
    pq.write_table(table, buffer)

    # Write the buffer contents to stdout
    sys.stdout.buffer.write(buffer.getvalue().to_pybytes())


if __name__ == "__main__":
    main()
