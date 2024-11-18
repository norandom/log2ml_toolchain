import sys
import os
import unittest
import tempfile
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from io import StringIO, BytesIO

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tools.vectorizer import (
    create_word_tokenizer,
    create_bpe_tokenizer,
    process_input,
    create_linformer_model,
)


class TestVectorizer(unittest.TestCase):
    def setUp(self):
        self.sample_log = (
            "[2024-03-18 10:15:23] INFO [system.service] Service started successfully"
        )
        self.model = create_linformer_model()

    def test_word_tokenizer(self):
        """Test word-level tokenization"""
        tokenizer = create_word_tokenizer()
        vector = process_input(self.sample_log, tokenizer, self.model)

        # Check vector shape and type
        self.assertIsInstance(vector, np.ndarray)
        self.assertEqual(vector.shape, (30000,))  # Based on model config

        # Check if vector contains valid numerical values
        self.assertFalse(np.any(np.isnan(vector)))
        self.assertFalse(np.any(np.isinf(vector)))

    def test_bpe_tokenizer(self):
        """Test BPE tokenization"""
        tokenizer, trainer = create_bpe_tokenizer()
        tokenizer.train_from_iterator([self.sample_log], trainer=trainer)
        vector = process_input(self.sample_log, tokenizer, self.model)

        # Check vector shape and type
        self.assertIsInstance(vector, np.ndarray)
        self.assertEqual(vector.shape, (30000,))  # Based on model config

        # Check if vector contains valid numerical values
        self.assertFalse(np.any(np.isnan(vector)))
        self.assertFalse(np.any(np.isinf(vector)))

    def test_save_load_bpe_tokenizer(self):
        """Test saving and loading BPE tokenizer"""
        with tempfile.NamedTemporaryFile(suffix=".json") as tmp:
            # Create and save tokenizer
            tokenizer, trainer = create_bpe_tokenizer()
            tokenizer.train_from_iterator([self.sample_log], trainer=trainer)
            tokenizer.save(tmp.name)

            # Load tokenizer and verify it works
            loaded_tokenizer = tokenizer.from_file(tmp.name)
            vector = process_input(self.sample_log, loaded_tokenizer, self.model)

            self.assertEqual(vector.shape, (30000,))

    def test_parquet_output(self):
        """Test Parquet file output format"""
        # Redirect stdout to capture Parquet output
        stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            # Create test data
            tokenizer = create_word_tokenizer()
            vector = process_input(self.sample_log, tokenizer, self.model)

            # Create DataFrame
            df = pd.DataFrame(
                {"text": [self.sample_log], "vector": [vector.tolist()]}
            )

            # Write to Parquet
            buffer = BytesIO()
            table = pa.Table.from_pandas(df)
            pq.write_table(table, buffer)

            # Read back and verify
            buffer.seek(0)
            df_read = pq.read_table(buffer).to_pandas()

            self.assertEqual(df_read["text"][0], self.sample_log)
            self.assertEqual(len(df_read["vector"][0]), 30000)

        finally:
            sys.stdout = stdout


if __name__ == "__main__":
    unittest.main()
