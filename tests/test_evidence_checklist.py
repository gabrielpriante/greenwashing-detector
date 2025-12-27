"""
Tests for the evidence checklist module.

These tests verify that the evidence checklist is correctly generated
for environmental claims.
"""

import sys
from pathlib import Path
import unittest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from evidence_checklist import (
    get_evidence_checklist,
    get_all_evidence_items,
    format_evidence_checklist,
    CLAIM_EVIDENCE_MAPPING
)


class TestEvidenceChecklistMapping(unittest.TestCase):
    """Test the evidence checklist mapping."""
    
    def test_mapping_includes_carbon_neutral(self):
        """Test that carbon neutral has a checklist."""
        self.assertIn('carbon neutral', CLAIM_EVIDENCE_MAPPING)
        self.assertIsInstance(CLAIM_EVIDENCE_MAPPING['carbon neutral'], list)
        self.assertTrue(len(CLAIM_EVIDENCE_MAPPING['carbon neutral']) > 0)
    
    def test_mapping_includes_net_zero(self):
        """Test that net zero has a checklist."""
        self.assertIn('net zero', CLAIM_EVIDENCE_MAPPING)
        self.assertIsInstance(CLAIM_EVIDENCE_MAPPING['net zero'], list)
        self.assertTrue(len(CLAIM_EVIDENCE_MAPPING['net zero']) > 0)
    
    def test_mapping_includes_biodegradable(self):
        """Test that biodegradable has a checklist."""
        self.assertIn('biodegradable', CLAIM_EVIDENCE_MAPPING)
        self.assertIsInstance(CLAIM_EVIDENCE_MAPPING['biodegradable'], list)
        self.assertTrue(len(CLAIM_EVIDENCE_MAPPING['biodegradable']) > 0)
    
    def test_mapping_includes_compostable(self):
        """Test that compostable has a checklist."""
        self.assertIn('compostable', CLAIM_EVIDENCE_MAPPING)
        self.assertIsInstance(CLAIM_EVIDENCE_MAPPING['compostable'], list)
        self.assertTrue(len(CLAIM_EVIDENCE_MAPPING['compostable']) > 0)
    
    def test_mapping_includes_recyclable(self):
        """Test that recyclable has a checklist."""
        self.assertIn('recyclable', CLAIM_EVIDENCE_MAPPING)
        self.assertIsInstance(CLAIM_EVIDENCE_MAPPING['recyclable'], list)
        self.assertTrue(len(CLAIM_EVIDENCE_MAPPING['recyclable']) > 0)
    
    def test_mapping_includes_sustainable_sourcing(self):
        """Test that sustainable sourcing has a checklist."""
        self.assertIn('sustainable sourcing', CLAIM_EVIDENCE_MAPPING)
        self.assertIsInstance(CLAIM_EVIDENCE_MAPPING['sustainable sourcing'], list)
        self.assertTrue(len(CLAIM_EVIDENCE_MAPPING['sustainable sourcing']) > 0)
    
    def test_mapping_includes_sustainably_sourced(self):
        """Test that sustainably sourced has a checklist."""
        self.assertIn('sustainably sourced', CLAIM_EVIDENCE_MAPPING)
        self.assertIsInstance(CLAIM_EVIDENCE_MAPPING['sustainably sourced'], list)
        self.assertTrue(len(CLAIM_EVIDENCE_MAPPING['sustainably sourced']) > 0)
    
    def test_mapping_includes_zero_emissions(self):
        """Test that zero emissions has a checklist."""
        self.assertIn('zero emissions', CLAIM_EVIDENCE_MAPPING)
        self.assertIsInstance(CLAIM_EVIDENCE_MAPPING['zero emissions'], list)
        self.assertTrue(len(CLAIM_EVIDENCE_MAPPING['zero emissions']) > 0)
    
    def test_mapping_includes_non_toxic(self):
        """Test that non toxic has a checklist."""
        self.assertIn('non toxic', CLAIM_EVIDENCE_MAPPING)
        self.assertIsInstance(CLAIM_EVIDENCE_MAPPING['non toxic'], list)
        self.assertTrue(len(CLAIM_EVIDENCE_MAPPING['non toxic']) > 0)
    
    def test_mapping_includes_chemical_free(self):
        """Test that chemical free has a checklist."""
        self.assertIn('chemical free', CLAIM_EVIDENCE_MAPPING)
        self.assertIsInstance(CLAIM_EVIDENCE_MAPPING['chemical free'], list)
        self.assertTrue(len(CLAIM_EVIDENCE_MAPPING['chemical free']) > 0)
    
    def test_all_checklist_items_are_strings(self):
        """Test that all checklist items are strings."""
        for claim, items in CLAIM_EVIDENCE_MAPPING.items():
            for item in items:
                self.assertIsInstance(item, str, f"Item in '{claim}' checklist is not a string")
    
    def test_all_checklists_have_multiple_items(self):
        """Test that all checklists have multiple items (at least 3)."""
        for claim, items in CLAIM_EVIDENCE_MAPPING.items():
            self.assertGreaterEqual(len(items), 3, f"Checklist for '{claim}' has fewer than 3 items")


class TestGetEvidenceChecklist(unittest.TestCase):
    """Test the get_evidence_checklist function."""
    
    def test_single_matched_term(self):
        """Test checklist generation for a single matched term."""
        matched_terms = ['carbon neutral']
        result = get_evidence_checklist(matched_terms)
        
        self.assertIsInstance(result, dict)
        self.assertIn('carbon neutral', result)
        self.assertEqual(result['carbon neutral'], CLAIM_EVIDENCE_MAPPING['carbon neutral'])
    
    def test_multiple_matched_terms(self):
        """Test checklist generation for multiple matched terms."""
        matched_terms = ['carbon neutral', 'biodegradable', 'recyclable']
        result = get_evidence_checklist(matched_terms)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 3)
        self.assertIn('carbon neutral', result)
        self.assertIn('biodegradable', result)
        self.assertIn('recyclable', result)
    
    def test_no_matched_terms(self):
        """Test checklist generation with no matched terms."""
        matched_terms = []
        result = get_evidence_checklist(matched_terms)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 0)
    
    def test_unknown_term_ignored(self):
        """Test that unknown terms are ignored."""
        matched_terms = ['carbon neutral', 'unknown term', 'biodegradable']
        result = get_evidence_checklist(matched_terms)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 2)
        self.assertIn('carbon neutral', result)
        self.assertIn('biodegradable', result)
        self.assertNotIn('unknown term', result)


class TestGetAllEvidenceItems(unittest.TestCase):
    """Test the get_all_evidence_items function."""
    
    def test_deduplicated_items(self):
        """Test that evidence items are deduplicated."""
        matched_terms = ['carbon neutral', 'net zero']
        result = get_all_evidence_items(matched_terms)
        
        self.assertIsInstance(result, list)
        # Should have unique items (some overlap between carbon neutral and net zero)
        self.assertEqual(len(result), len(set(result)))
    
    def test_sorted_output(self):
        """Test that output is sorted."""
        matched_terms = ['carbon neutral', 'biodegradable']
        result = get_all_evidence_items(matched_terms)
        
        self.assertEqual(result, sorted(result))
    
    def test_no_matched_terms(self):
        """Test with no matched terms."""
        matched_terms = []
        result = get_all_evidence_items(matched_terms)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)


class TestFormatEvidenceChecklist(unittest.TestCase):
    """Test the format_evidence_checklist function."""
    
    def test_format_single_claim(self):
        """Test formatting a single claim."""
        checklist = {
            'carbon neutral': ['Item 1', 'Item 2', 'Item 3']
        }
        result = format_evidence_checklist(checklist)
        
        self.assertIsInstance(result, str)
        self.assertIn('carbon neutral', result)
        self.assertIn('Item 1', result)
        self.assertIn('Item 2', result)
        self.assertIn('Item 3', result)
    
    def test_format_multiple_claims(self):
        """Test formatting multiple claims."""
        checklist = {
            'carbon neutral': ['Item 1', 'Item 2'],
            'biodegradable': ['Item A', 'Item B']
        }
        result = format_evidence_checklist(checklist)
        
        self.assertIsInstance(result, str)
        self.assertIn('carbon neutral', result)
        self.assertIn('biodegradable', result)
        self.assertIn('Item 1', result)
        self.assertIn('Item A', result)
    
    def test_format_empty_checklist(self):
        """Test formatting empty checklist."""
        checklist = {}
        result = format_evidence_checklist(checklist)
        
        self.assertEqual(result, "")
    
    def test_format_uses_bullets(self):
        """Test that formatting uses bullet points."""
        checklist = {
            'carbon neutral': ['Item 1']
        }
        result = format_evidence_checklist(checklist)
        
        self.assertIn('•', result)


if __name__ == '__main__':
    unittest.main()
