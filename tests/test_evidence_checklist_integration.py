"""
Tests for evidence checklist integration.

These tests verify that the evidence checklist is correctly integrated
into the greenwashing scoring and CLI output.
"""

import sys
from pathlib import Path
import unittest
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from greenwashing_scoring import simple_greenwashing_score


class TestEvidenceChecklistIntegration(unittest.TestCase):
    """Test integration of evidence checklist with greenwashing scoring."""
    
    def test_scoring_includes_evidence_checklist_field(self):
        """Test that scoring result includes evidence_checklist field."""
        text = "eco-friendly product"
        result = simple_greenwashing_score(text)
        
        self.assertIn('evidence_checklist', result)
        self.assertIsInstance(result['evidence_checklist'], dict)
    
    def test_evidence_checklist_empty_when_no_matches(self):
        """Test that evidence checklist is empty when no claims detected."""
        text = "regular product with no claims"
        result = simple_greenwashing_score(text)
        
        self.assertEqual(len(result['evidence_checklist']), 0)
    
    def test_evidence_checklist_populated_for_carbon_neutral(self):
        """Test that evidence checklist is populated for carbon neutral claim."""
        text = "our carbon neutral product"
        result = simple_greenwashing_score(text)
        
        self.assertIn('carbon neutral', result['evidence_checklist'])
        self.assertIsInstance(result['evidence_checklist']['carbon neutral'], list)
        self.assertTrue(len(result['evidence_checklist']['carbon neutral']) > 0)
    
    def test_evidence_checklist_populated_for_biodegradable(self):
        """Test that evidence checklist is populated for biodegradable claim."""
        text = "biodegradable packaging"
        result = simple_greenwashing_score(text)
        
        self.assertIn('biodegradable', result['evidence_checklist'])
        self.assertIsInstance(result['evidence_checklist']['biodegradable'], list)
        self.assertTrue(len(result['evidence_checklist']['biodegradable']) > 0)
    
    def test_evidence_checklist_multiple_claims(self):
        """Test evidence checklist with multiple claims."""
        text = "carbon neutral and biodegradable product"
        result = simple_greenwashing_score(text)
        
        self.assertEqual(len(result['evidence_checklist']), 2)
        self.assertIn('carbon neutral', result['evidence_checklist'])
        self.assertIn('biodegradable', result['evidence_checklist'])
    
    def test_evidence_checklist_with_negated_terms(self):
        """Test that negated terms do not appear in evidence checklist."""
        text = "not carbon neutral but biodegradable"
        result = simple_greenwashing_score(text)
        
        # carbon neutral should be negated, only biodegradable should be in checklist
        self.assertNotIn('carbon neutral', result['evidence_checklist'])
        self.assertIn('biodegradable', result['evidence_checklist'])
    
    def test_evidence_checklist_for_net_zero(self):
        """Test evidence checklist for net zero claim."""
        text = "net zero emissions by 2030"
        result = simple_greenwashing_score(text)
        
        self.assertIn('net zero', result['evidence_checklist'])
        self.assertTrue(len(result['evidence_checklist']['net zero']) > 0)
    
    def test_evidence_checklist_for_recyclable(self):
        """Test evidence checklist for recyclable claim."""
        text = "100% recyclable materials"
        result = simple_greenwashing_score(text)
        
        # Note: 'recyclable' is not in default keywords, so won't appear
        # This test documents current behavior
        self.assertNotIn('recyclable', result['matched_terms'])
        self.assertEqual(len(result['evidence_checklist']), 0)
    
    def test_evidence_checklist_for_chemical_free(self):
        """Test evidence checklist for chemical free claim."""
        text = "chemical-free product"
        result = simple_greenwashing_score(text)
        
        self.assertIn('chemical free', result['evidence_checklist'])
        self.assertTrue(len(result['evidence_checklist']['chemical free']) > 0)
    
    def test_evidence_checklist_for_all_natural(self):
        """Test evidence checklist for all natural claim."""
        text = "all natural ingredients"
        result = simple_greenwashing_score(text)
        
        self.assertIn('all natural', result['evidence_checklist'])
        self.assertTrue(len(result['evidence_checklist']['all natural']) > 0)
    
    def test_evidence_checklist_with_eco_friendly(self):
        """Test evidence checklist for eco-friendly claim."""
        text = "eco-friendly product"
        result = simple_greenwashing_score(text)
        
        self.assertIn('eco friendly', result['evidence_checklist'])
        self.assertTrue(len(result['evidence_checklist']['eco friendly']) > 0)
    
    def test_evidence_checklist_with_sustainable(self):
        """Test evidence checklist for sustainable claim."""
        text = "sustainable product"
        result = simple_greenwashing_score(text)
        
        self.assertIn('sustainable', result['evidence_checklist'])
        self.assertTrue(len(result['evidence_checklist']['sustainable']) > 0)


class TestEvidenceChecklistWithConfig(unittest.TestCase):
    """Test evidence checklist with custom configuration."""
    
    def test_evidence_checklist_with_custom_config(self):
        """Test that evidence checklist works with custom config."""
        import tempfile
        
        text = "carbon neutral product"
        
        # Create custom config
        custom_config = """
keywords:
  custom:
    carbon neutral: 5
thresholds:
  low: 0
  medium: 30
  high: 60
"""
        temp_dir = tempfile.mkdtemp()
        config_path = Path(temp_dir) / "custom.yml"
        with open(config_path, 'w') as f:
            f.write(custom_config)
        
        try:
            result = simple_greenwashing_score(text, str(config_path))
            
            # Evidence checklist should still work
            self.assertIn('evidence_checklist', result)
            self.assertIn('carbon neutral', result['evidence_checklist'])
        finally:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)


class TestBackwardCompatibility(unittest.TestCase):
    """Test that adding evidence checklist maintains backward compatibility."""
    
    def test_all_original_fields_present(self):
        """Test that all original fields are still present."""
        text = "eco-friendly product"
        result = simple_greenwashing_score(text)
        
        # Original fields
        self.assertIn('score', result)
        self.assertIn('risk_level', result)
        self.assertIn('matched_terms', result)
        self.assertIn('matched_keywords', result)
        self.assertIn('negated_terms', result)
        
        # New field
        self.assertIn('evidence_checklist', result)
    
    def test_matched_keywords_unchanged(self):
        """Test that matched_keywords behavior is unchanged."""
        text = "eco-friendly and sustainable"
        result = simple_greenwashing_score(text)
        
        # matched_keywords and matched_terms should be the same
        self.assertEqual(result['matched_keywords'], result['matched_terms'])


if __name__ == '__main__':
    unittest.main()
