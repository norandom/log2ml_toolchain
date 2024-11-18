#!/usr/bin/env python3

import torch
from linformer_pytorch import LinformerLM
from tokenizers import Tokenizer
from tokenizers.models import WordLevel, BPE
from tokenizers.pre_tokenizers import Whitespace
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
        checkpoint_level="C0",  # What checkpoint level to use
        parameter_sharing="layerwise",  # What level of parameter sharing to use
        k_reduce_by_layer=0,  # Going down depth, how much to reduce dim_k by
        full_attention=False,  # Use full attention instead
        include_ff=True,      # Whether or not to include the Feed Forward layer
        w_o_intermediate_dim=None,  # If not None, have 2 w_o matrices
        emb_dim=128,          # Embedding dimension
        causal=False,         # If you want this to be a causal Linformer
        method="learnable",   # The method of how to perform the projection
        ff_intermediate=None  # Feed forward intermediate dimension
    )
    return model


def create_word_tokenizer():
    """Create a simple word-level tokenizer with a basic vocabulary"""
    # Create a basic vocabulary with special tokens
    vocab = {
        "[PAD]": 0,
        "[UNK]": 1,
        "[CLS]": 2,
        "[SEP]": 3,
        "[MASK]": 4,
    }
    tokenizer = Tokenizer(WordLevel(vocab=vocab, unk_token="[UNK]"))
    tokenizer.pre_tokenizer = Whitespace()
    return tokenizer


def create_bpe_tokenizer():
    """Create and configure a BPE tokenizer"""
    tokenizer = Tokenizer(BPE())
    trainer = BpeTrainer(
        vocab_size=30000,
        min_frequency=2,
        special_tokens=["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]"],
    )
    return tokenizer, trainer


def train_bpe_tokenizer(tokenizer, trainer, text):
    """Train a BPE tokenizer on the given text"""
    tokenizer.train_from_iterator([text], trainer=trainer)
    return tokenizer


def process_input(text, tokenizer, model):
    """Process a single text input through the tokenizer and model"""
    # Tokenize the input
    encoding = tokenizer.encode(text)
    input_ids = encoding.ids[:700]  # Truncate to max length
    # Pad sequence if needed
    if len(input_ids) < 700:
        input_ids = input_ids + [0] * (700 - len(input_ids))
    # Convert to tensor and get embeddings
    input_tensor = torch.tensor(input_ids).unsqueeze(0)  # Add batch dimension
    with torch.no_grad():
        # Get the embeddings from the token embedding layer
        embeddings = model.to_token_emb(input_tensor)
        # Apply positional embeddings
        embeddings = model.pos_emb(embeddings)
        # Get the mean pooled representation
        embeddings = embeddings.mean(dim=1).squeeze(0)
    return embeddings


if __name__ == "__main__":
    print("This module provides vectorization utilities for the Log2ML toolchain.")
    print("It is not meant to be run directly.")
