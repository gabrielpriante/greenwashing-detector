"""
Tests for config_loader module.

These tests verify that YAML config loading and validation work correctly.
"""

import sys
from pathlib import Path
import unittest
import tempfile
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from config_loader import load_config, get_default_config, ConfigError


class TestConfigLoader(unittest.TestCase):
    """Test the config loader functionality."""
    
    def setUp(self):
        """Create temporary directory for test configs."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_load_default_config(self):
        """Test loading the default config file."""
        config = load_config()
        
        self.assertIn('keywords', config)
        self.assertIn('thresholds', config)
        self.assertIsInstance(config['keywords'], dict)
        self.assertIsInstance(config['thresholds'], dict)
        
        # Check some expected keywords
        self.assertIn('eco friendly', config['keywords'])
        self.assertIn('green', config['keywords'])
        
        # Check thresholds
        self.assertIn('low', config['thresholds'])
        self.assertIn('medium', config['thresholds'])
        self.assertIn('high', config['thresholds'])
    
    def test_load_custom_config(self):
        """Test loading a custom config file."""
        custom_config = """
keywords:
  category1:
    test keyword: 5
    another keyword: 3
thresholds:
  low: 0
  medium: 40
  high: 70
"""
        config_path = Path(self.temp_dir) / "custom.yml"
        with open(config_path, 'w') as f:
            f.write(custom_config)
        
        config = load_config(str(config_path))
        
        self.assertEqual(config['keywords']['test keyword'], 5)
        self.assertEqual(config['keywords']['another keyword'], 3)
        self.assertEqual(config['thresholds']['medium'], 40)
        self.assertEqual(config['thresholds']['high'], 70)
    
    def test_missing_config_file(self):
        """Test that missing config file raises ConfigError."""
        with self.assertRaises(ConfigError) as context:
            load_config("/nonexistent/path/to/config.yml")
        
        self.assertIn("not found", str(context.exception))
    
    def test_invalid_yaml(self):
        """Test that invalid YAML raises ConfigError."""
        invalid_yaml = """
keywords: [unclosed bracket
thresholds:
  low: 0
"""
        config_path = Path(self.temp_dir) / "invalid.yml"
        with open(config_path, 'w') as f:
            f.write(invalid_yaml)
        
        with self.assertRaises(ConfigError) as context:
            load_config(str(config_path))
        
        # Should raise error due to YAML parsing or missing thresholds
        self.assertTrue(
            "parse" in str(context.exception).lower() or
            "keywords" in str(context.exception).lower()
        )
    
    def test_missing_keywords_section(self):
        """Test that config without keywords section raises ConfigError."""
        no_keywords = """
thresholds:
  low: 0
  medium: 30
  high: 60
"""
        config_path = Path(self.temp_dir) / "no_keywords.yml"
        with open(config_path, 'w') as f:
            f.write(no_keywords)
        
        with self.assertRaises(ConfigError) as context:
            load_config(str(config_path))
        
        self.assertIn("keywords", str(context.exception))
    
    def test_missing_thresholds_section(self):
        """Test that config without thresholds section raises ConfigError."""
        no_thresholds = """
keywords:
  category1:
    keyword1: 2
"""
        config_path = Path(self.temp_dir) / "no_thresholds.yml"
        with open(config_path, 'w') as f:
            f.write(no_thresholds)
        
        with self.assertRaises(ConfigError) as context:
            load_config(str(config_path))
        
        self.assertIn("thresholds", str(context.exception))
    
    def test_negative_weight(self):
        """Test that negative weight raises ConfigError."""
        negative_weight = """
keywords:
  category1:
    bad keyword: -5
thresholds:
  low: 0
  medium: 30
  high: 60
"""
        config_path = Path(self.temp_dir) / "negative.yml"
        with open(config_path, 'w') as f:
            f.write(negative_weight)
        
        with self.assertRaises(ConfigError) as context:
            load_config(str(config_path))
        
        self.assertIn("non-negative", str(context.exception))
    
    def test_invalid_threshold_order(self):
        """Test that invalid threshold order raises ConfigError."""
        wrong_order = """
keywords:
  category1:
    keyword1: 2
thresholds:
  low: 0
  medium: 70
  high: 40
"""
        config_path = Path(self.temp_dir) / "wrong_order.yml"
        with open(config_path, 'w') as f:
            f.write(wrong_order)
        
        with self.assertRaises(ConfigError) as context:
            load_config(str(config_path))
        
        self.assertIn("ascending order", str(context.exception))
    
    def test_missing_threshold_keys(self):
        """Test that missing threshold keys raise ConfigError."""
        missing_high = """
keywords:
  category1:
    keyword1: 2
thresholds:
  low: 0
  medium: 30
"""
        config_path = Path(self.temp_dir) / "missing_high.yml"
        with open(config_path, 'w') as f:
            f.write(missing_high)
        
        with self.assertRaises(ConfigError) as context:
            load_config(str(config_path))
        
        self.assertIn("high", str(context.exception))
    
    def test_multiple_categories_flattened(self):
        """Test that keywords from multiple categories are flattened correctly."""
        multi_category = """
keywords:
  category1:
    keyword1: 2
    keyword2: 3
  category2:
    keyword3: 4
    keyword4: 1
thresholds:
  low: 0
  medium: 30
  high: 60
"""
        config_path = Path(self.temp_dir) / "multi_cat.yml"
        with open(config_path, 'w') as f:
            f.write(multi_category)
        
        config = load_config(str(config_path))
        
        # All keywords should be in the flattened dict
        self.assertEqual(len(config['keywords']), 4)
        self.assertEqual(config['keywords']['keyword1'], 2)
        self.assertEqual(config['keywords']['keyword3'], 4)
    
    def test_get_default_config(self):
        """Test that get_default_config returns expected structure."""
        config = get_default_config()
        
        self.assertIn('keywords', config)
        self.assertIn('thresholds', config)
        
        # Check it contains expected keywords
        self.assertIn('eco friendly', config['keywords'])
        self.assertIn('sustainable', config['keywords'])
        
        # Check thresholds
        self.assertEqual(config['thresholds']['low'], 0)
        self.assertEqual(config['thresholds']['medium'], 30)
        self.assertEqual(config['thresholds']['high'], 60)
    
    def test_empty_keywords(self):
        """Test that empty keywords section raises ConfigError."""
        empty_keywords = """
keywords:
  category1: {}
thresholds:
  low: 0
  medium: 30
  high: 60
"""
        config_path = Path(self.temp_dir) / "empty_keywords.yml"
        with open(config_path, 'w') as f:
            f.write(empty_keywords)
        
        with self.assertRaises(ConfigError) as context:
            load_config(str(config_path))
        
        self.assertIn("at least one keyword", str(context.exception))


if __name__ == '__main__':
    unittest.main()
