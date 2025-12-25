"""
Tests for greenwashing scoring with custom configurations.

These tests verify that custom YAML configs affect scoring behavior correctly.
"""

import sys
from pathlib import Path
import unittest
import tempfile

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from greenwashing_scoring import simple_greenwashing_score
from config_loader import ConfigError


class TestScoringWithConfig(unittest.TestCase):
    """Test scoring with custom configuration files."""
    
    def setUp(self):
        """Create temporary directory for test configs."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_scoring_without_config_uses_defaults(self):
        """Test that scoring without config uses hardcoded defaults."""
        text = "eco-friendly and all natural"
        result = simple_greenwashing_score(text)
        
        # Should match hardcoded behavior
        self.assertIn('score', result)
        self.assertIn('risk_level', result)
        self.assertIn('matched_keywords', result)
        self.assertGreater(result['score'], 0)
        self.assertEqual(len(result['matched_keywords']), 2)
    
    def test_custom_weights_change_score(self):
        """Test that changing weights in config changes the score."""
        text = "eco-friendly product"
        
        # Get score with default weights (eco friendly = 2)
        default_result = simple_greenwashing_score(text)
        default_score = default_result['score']
        
        # Create custom config with higher weight
        custom_config = """
keywords:
  custom:
    eco friendly: 10
thresholds:
  low: 0
  medium: 30
  high: 60
"""
        config_path = Path(self.temp_dir) / "custom_weights.yml"
        with open(config_path, 'w') as f:
            f.write(custom_config)
        
        # Get score with custom weights (eco friendly = 10)
        custom_result = simple_greenwashing_score(text, str(config_path))
        custom_score = custom_result['score']
        
        # Custom score should be higher
        self.assertGreater(custom_score, default_score)
        self.assertEqual(custom_score, 100)  # 10 * 10 = 100 (capped at 100)
    
    def test_custom_thresholds_change_risk_level(self):
        """Test that changing thresholds changes the risk level."""
        text = "eco-friendly and sustainable"
        # With default weights, this scores: (2+2)*10 = 40
        
        # Config with default thresholds (medium at 30)
        default_result = simple_greenwashing_score(text)
        self.assertEqual(default_result['risk_level'], 'Medium')
        
        # Config with higher medium threshold (medium at 50)
        high_threshold_config = """
keywords:
  generic:
    eco friendly: 2
    sustainable: 2
thresholds:
  low: 0
  medium: 50
  high: 80
"""
        config_path = Path(self.temp_dir) / "high_threshold.yml"
        with open(config_path, 'w') as f:
            f.write(high_threshold_config)
        
        custom_result = simple_greenwashing_score(text, str(config_path))
        # Score is 40, which is < 50, so should be Low risk now
        self.assertEqual(custom_result['risk_level'], 'Low')
    
    def test_custom_keywords_detected(self):
        """Test that custom keywords are detected."""
        text = "this is my special green term"
        
        # Default config won't match "special green term"
        default_result = simple_greenwashing_score(text)
        self.assertNotIn('special green term', default_result['matched_keywords'])
        
        # Custom config with new keyword
        custom_config = """
keywords:
  custom:
    special green term: 5
thresholds:
  low: 0
  medium: 30
  high: 60
"""
        config_path = Path(self.temp_dir) / "custom_keywords.yml"
        with open(config_path, 'w') as f:
            f.write(custom_config)
        
        custom_result = simple_greenwashing_score(text, str(config_path))
        self.assertIn('special green term', custom_result['matched_keywords'])
        self.assertEqual(custom_result['score'], 50)  # 5 * 10 = 50
    
    def test_invalid_config_raises_error(self):
        """Test that invalid config file raises ConfigError."""
        text = "eco-friendly"
        
        # Create invalid config
        invalid_config = """
this is not valid yaml structure
"""
        config_path = Path(self.temp_dir) / "invalid.yml"
        with open(config_path, 'w') as f:
            f.write(invalid_config)
        
        with self.assertRaises(ConfigError):
            simple_greenwashing_score(text, str(config_path))
    
    def test_nonexistent_config_raises_error(self):
        """Test that nonexistent config file raises ConfigError."""
        text = "eco-friendly"
        
        with self.assertRaises(ConfigError):
            simple_greenwashing_score(text, "/nonexistent/config.yml")
    
    def test_empty_text_with_config(self):
        """Test that empty text returns zero score with custom config."""
        custom_config = """
keywords:
  custom:
    eco friendly: 5
thresholds:
  low: 0
  medium: 30
  high: 60
"""
        config_path = Path(self.temp_dir) / "custom.yml"
        with open(config_path, 'w') as f:
            f.write(custom_config)
        
        result = simple_greenwashing_score("", str(config_path))
        
        self.assertEqual(result['score'], 0)
        self.assertEqual(result['risk_level'], 'Low')
        self.assertEqual(len(result['matched_keywords']), 0)
    
    def test_multiple_categories_in_config(self):
        """Test that keywords from multiple categories work correctly."""
        text = "eco-friendly and chemical-free product"
        
        custom_config = """
keywords:
  category1:
    eco friendly: 3
  category2:
    chemical free: 4
thresholds:
  low: 0
  medium: 30
  high: 60
"""
        config_path = Path(self.temp_dir) / "multi_cat.yml"
        with open(config_path, 'w') as f:
            f.write(custom_config)
        
        result = simple_greenwashing_score(text, str(config_path))
        
        # Should find both keywords
        self.assertEqual(len(result['matched_keywords']), 2)
        self.assertIn('eco friendly', result['matched_keywords'])
        self.assertIn('chemical free', result['matched_keywords'])
        # Score: (3 + 4) * 10 = 70
        self.assertEqual(result['score'], 70)
        self.assertEqual(result['risk_level'], 'High')
    
    def test_threshold_boundary_conditions(self):
        """Test risk levels at exact threshold boundaries."""
        # Create config with known thresholds
        config_content = """
keywords:
  test:
    test keyword: 3
thresholds:
  low: 0
  medium: 30
  high: 60
"""
        config_path = Path(self.temp_dir) / "boundary.yml"
        with open(config_path, 'w') as f:
            f.write(config_content)
        
        # Test at exactly medium threshold (score = 30)
        # Need weight * 10 = 30, so weight = 3
        result = simple_greenwashing_score("test keyword", str(config_path))
        self.assertEqual(result['score'], 30)
        self.assertEqual(result['risk_level'], 'Medium')
        
        # Test just below medium threshold
        config_content_29 = """
keywords:
  test:
    test keyword: 2
thresholds:
  low: 0
  medium: 30
  high: 60
"""
        config_path_29 = Path(self.temp_dir) / "boundary_29.yml"
        with open(config_path_29, 'w') as f:
            f.write(config_content_29)
        
        result_29 = simple_greenwashing_score("test keyword", str(config_path_29))
        self.assertEqual(result_29['score'], 20)
        self.assertEqual(result_29['risk_level'], 'Low')


if __name__ == '__main__':
    unittest.main()
