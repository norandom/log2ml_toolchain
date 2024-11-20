import unittest

from log2ml.vectorizer.vectorizer import (
    create_bpe_tokenizer,
    create_linformer_model,
    create_word_tokenizer,
    process_input,
)


class TestVectorizer(unittest.TestCase):
    """Test cases for the vectorizer module"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_text = "This is a test message for the vectorizer"
        self.model = create_linformer_model()

    def test_word_tokenizer(self):
        """Test word tokenizer creation and usage"""
        tokenizer = create_word_tokenizer()
        self.assertIsNotNone(tokenizer)
        encoding = tokenizer.encode(self.test_text)
        self.assertGreater(len(encoding.ids), 0)

    def test_bpe_tokenizer(self):
        """Test BPE tokenizer creation and training"""
        tokenizer, trainer = create_bpe_tokenizer()
        self.assertIsNotNone(tokenizer)
        self.assertIsNotNone(trainer)

    def test_process_input(self):
        """Test input processing through tokenizer and model"""
        tokenizer = create_word_tokenizer()
        vector = process_input(self.test_text, tokenizer, self.model)
        # Check embedding dimension (matches model config)
        self.assertEqual(vector.shape[0], 128)


if __name__ == "__main__":
    unittest.main()
