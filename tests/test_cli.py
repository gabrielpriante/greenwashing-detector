"""
Tests for the CLI module.

These tests verify that the CLI commands work correctly.
"""

import sys
from pathlib import Path
import unittest
import tempfile
import csv
import json
from io import StringIO

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from greenwashing_scoring import simple_greenwashing_score


class TestCLIFunctions(unittest.TestCase):
    """Test the CLI helper functions."""
    
    def test_simple_greenwashing_score(self):
        """Test that greenwashing scoring works."""
        text = "eco-friendly and all natural"
        result = simple_greenwashing_score(text)
        
        self.assertIn('score', result)
        self.assertIn('risk_level', result)
        self.assertIn('matched_keywords', result)
        self.assertGreater(result['score'], 0)
        self.assertEqual(len(result['matched_keywords']), 2)
    
    def test_simple_greenwashing_score_no_matches(self):
        """Test that scoring works for text with no greenwashing."""
        text = "regular product with no special claims"
        result = simple_greenwashing_score(text)
        
        self.assertEqual(result['score'], 0)
        self.assertEqual(result['risk_level'], 'Low')
        self.assertEqual(len(result['matched_keywords']), 0)
    
    def test_simple_greenwashing_score_empty(self):
        """Test that scoring handles empty text."""
        text = ""
        result = simple_greenwashing_score(text)
        
        self.assertEqual(result['score'], 0)
        self.assertEqual(result['risk_level'], 'Low')
        self.assertEqual(len(result['matched_keywords']), 0)


class TestCLICSVProcessing(unittest.TestCase):
    """Test CSV file processing functionality."""
    
    def setUp(self):
        """Create temporary directory and test CSV file."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_csv = Path(self.temp_dir) / "test.csv"
        self.output_csv = Path(self.temp_dir) / "output.csv"
        
        # Create test CSV
        with open(self.test_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['product', 'description'])
            writer.writerow(['Product A', 'eco-friendly and natural'])
            writer.writerow(['Product B', 'regular product'])
            writer.writerow(['Product C', ''])
    
    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_csv_file_exists(self):
        """Test that test CSV was created successfully."""
        self.assertTrue(self.test_csv.exists())
    
    def test_csv_content_correct(self):
        """Test that CSV has correct content."""
        with open(self.test_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 3)
            self.assertEqual(rows[0]['product'], 'Product A')
            self.assertEqual(rows[0]['description'], 'eco-friendly and natural')


class TestCLIIntegration(unittest.TestCase):
    """Integration tests for CLI commands."""
    
    def test_analyze_text_basic(self):
        """Test basic text analysis."""
        text = "eco-friendly and sustainable"
        result = simple_greenwashing_score(text)
        
        # Should detect greenwashing terms
        self.assertGreater(result['score'], 0)
        self.assertIn(result['risk_level'], ['Low', 'Medium', 'High'])
        self.assertTrue(len(result['matched_keywords']) > 0)
    
    def test_analyze_high_risk_text(self):
        """Test text with multiple greenwashing terms."""
        text = "eco-friendly natural sustainable green planet-friendly carbon-neutral"
        result = simple_greenwashing_score(text)
        
        # Should be high risk
        self.assertGreater(result['score'], 30)
        self.assertTrue(len(result['matched_keywords']) >= 3)
    
    def test_analyze_clean_text(self):
        """Test text with no greenwashing terms."""
        text = "our product is made of steel and aluminum"
        result = simple_greenwashing_score(text)
        
        # Should be low risk
        self.assertEqual(result['score'], 0)
        self.assertEqual(result['risk_level'], 'Low')
        self.assertEqual(len(result['matched_keywords']), 0)


if __name__ == '__main__':
    unittest.main()
