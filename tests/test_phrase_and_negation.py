"""
Tests for phrase matching with word boundaries and negation handling.

These tests verify that the greenwashing detector properly:
1. Matches phrases with word boundaries (not naive substring matching)
2. Detects negation and excludes negated terms from scoring
3. Returns both matched_terms and negated_terms in results
"""

import sys
from pathlib import Path
import unittest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from greenwashing_scoring import simple_greenwashing_score


class TestPhraseMatching(unittest.TestCase):
    """Test phrase matching with word boundaries."""
    
    def test_phrase_with_word_boundaries(self):
        """Test that 'carbon neutral' is detected as a complete phrase."""
        text = "Our product is carbon neutral and sustainable"
        result = simple_greenwashing_score(text)
        
        self.assertIn('carbon neutral', result['matched_terms'])
        self.assertIn('sustainable', result['matched_terms'])
        # Score: carbon neutral (4) + sustainable (2) = 6 * 10 = 60
        self.assertEqual(result['score'], 60)
    
    def test_phrase_not_matched_without_word_boundary(self):
        """Test that 'carbonneutral' (no space) is NOT matched."""
        text = "We are carbonneutral in our operations"
        result = simple_greenwashing_score(text)
        
        # Should not match because there's no word boundary
        self.assertNotIn('carbon neutral', result['matched_terms'])
        self.assertEqual(result['score'], 0)
    
    def test_net_zero_phrase_detection(self):
        """Test that 'net zero' is detected as a phrase."""
        text = "We achieved net zero last year"
        result = simple_greenwashing_score(text)
        
        self.assertIn('net zero', result['matched_terms'])
        # Score: net zero (4) = 4 * 10 = 40
        self.assertEqual(result['score'], 40)
    
    def test_climate_positive_phrase_detection(self):
        """Test that 'climate positive' is detected as a phrase."""
        text = "Our initiative is climate positive"
        result = simple_greenwashing_score(text)
        
        self.assertIn('climate positive', result['matched_terms'])
        # Score: climate positive (4) = 4 * 10 = 40
        self.assertEqual(result['score'], 40)
    
    def test_plastic_free_phrase_detection(self):
        """Test that 'plastic free' is detected as a phrase."""
        text = "This packaging is plastic free"
        result = simple_greenwashing_score(text)
        
        self.assertIn('plastic free', result['matched_terms'])
        # Score: plastic free (3) = 3 * 10 = 30
        self.assertEqual(result['score'], 30)
    
    def test_biodegradable_single_word(self):
        """Test that single word 'biodegradable' is detected."""
        text = "Made from biodegradable materials"
        result = simple_greenwashing_score(text)
        
        self.assertIn('biodegradable', result['matched_terms'])
        # Score: biodegradable (2) = 2 * 10 = 20
        self.assertEqual(result['score'], 20)
    
    def test_case_insensitive_matching(self):
        """Test that matching is case insensitive."""
        text = "CARBON NEUTRAL and Carbon Neutral and carbon neutral"
        result = simple_greenwashing_score(text)
        
        # Should match despite different cases
        self.assertIn('carbon neutral', result['matched_terms'])
        # Should only count once despite multiple occurrences
        self.assertEqual(len(result['matched_terms']), 1)
    
    def test_multi_word_phrase_eco_friendly(self):
        """Test that 'eco friendly' (after cleaning 'eco-friendly') is matched."""
        text = "This is an eco-friendly product"
        result = simple_greenwashing_score(text)
        
        # After cleaning, 'eco-friendly' becomes 'eco friendly'
        self.assertIn('eco friendly', result['matched_terms'])
        # Score: eco friendly (2) = 2 * 10 = 20
        self.assertEqual(result['score'], 20)


class TestNegationHandling(unittest.TestCase):
    """Test negation detection and handling."""
    
    def test_not_eco_friendly_negated(self):
        """Test that 'not eco-friendly' does not inflate the score."""
        text = "This product is not eco-friendly"
        result = simple_greenwashing_score(text)
        
        # 'eco friendly' should be in negated_terms, not matched_terms
        self.assertIn('eco friendly', result['negated_terms'])
        self.assertNotIn('eco friendly', result['matched_terms'])
        # Score should be 0 because the term is negated
        self.assertEqual(result['score'], 0)
    
    def test_no_carbon_neutral_negated(self):
        """Test that 'no carbon neutral' is negated."""
        text = "We have no carbon neutral certification"
        result = simple_greenwashing_score(text)
        
        self.assertIn('carbon neutral', result['negated_terms'])
        self.assertNotIn('carbon neutral', result['matched_terms'])
        self.assertEqual(result['score'], 0)
    
    def test_never_sustainable_negated(self):
        """Test that 'never sustainable' is negated."""
        text = "Our practices are never sustainable enough"
        result = simple_greenwashing_score(text)
        
        self.assertIn('sustainable', result['negated_terms'])
        self.assertNotIn('sustainable', result['matched_terms'])
        self.assertEqual(result['score'], 0)
    
    def test_negation_within_three_tokens(self):
        """Test that negation works within 3 tokens before the match."""
        # One token between: "not really eco-friendly"
        text1 = "This is not really eco friendly"
        result1 = simple_greenwashing_score(text1)
        self.assertIn('eco friendly', result1['negated_terms'])
        self.assertEqual(result1['score'], 0)
        
        # Two tokens between: "not very much eco-friendly"
        text2 = "This is not very much eco friendly"
        result2 = simple_greenwashing_score(text2)
        self.assertIn('eco friendly', result2['negated_terms'])
        self.assertEqual(result2['score'], 0)
        
        # Three tokens between: "not always completely totally eco-friendly"
        text3 = "This is not always completely eco friendly"
        result3 = simple_greenwashing_score(text3)
        self.assertIn('eco friendly', result3['negated_terms'])
        self.assertEqual(result3['score'], 0)
    
    def test_negation_beyond_three_tokens_not_negated(self):
        """Test that negation beyond 3 tokens does NOT negate the match."""
        # Four tokens between negation and match
        text = "This is not always completely totally eco friendly"
        result = simple_greenwashing_score(text)
        
        # Should be matched because negation is more than 3 tokens away
        self.assertIn('eco friendly', result['matched_terms'])
        self.assertNotIn('eco friendly', result['negated_terms'])
        self.assertGreater(result['score'], 0)
    
    def test_mixed_negated_and_matched_terms(self):
        """Test that some terms can be negated while others are matched."""
        text = "We are not eco friendly but we are sustainable"
        result = simple_greenwashing_score(text)
        
        # 'eco friendly' should be negated
        self.assertIn('eco friendly', result['negated_terms'])
        self.assertNotIn('eco friendly', result['matched_terms'])
        
        # 'sustainable' should be matched
        self.assertIn('sustainable', result['matched_terms'])
        self.assertNotIn('sustainable', result['negated_terms'])
        
        # Score should only count 'sustainable' (2 * 10 = 20)
        self.assertEqual(result['score'], 20)
    
    def test_multiple_negations(self):
        """Test handling of multiple negated terms."""
        text = "We are not eco friendly and no carbon neutral"
        result = simple_greenwashing_score(text)
        
        # Both terms should be negated
        self.assertIn('eco friendly', result['negated_terms'])
        self.assertIn('carbon neutral', result['negated_terms'])
        
        # No terms should be matched
        self.assertEqual(len(result['matched_terms']), 0)
        self.assertEqual(result['score'], 0)
    
    def test_positive_term_not_affected_by_earlier_negation(self):
        """Test that a positive term is not affected by an earlier negation."""
        text = "We are not greenwashing, we are truly sustainable"
        result = simple_greenwashing_score(text)
        
        # 'sustainable' should be matched (negation is far away)
        self.assertIn('sustainable', result['matched_terms'])
        self.assertEqual(result['score'], 20)


class TestBackwardCompatibility(unittest.TestCase):
    """Test that backward compatibility is maintained."""
    
    def test_matched_keywords_still_present(self):
        """Test that 'matched_keywords' field still exists for backward compatibility."""
        text = "eco-friendly product"
        result = simple_greenwashing_score(text)
        
        # Both matched_terms and matched_keywords should be present
        self.assertIn('matched_terms', result)
        self.assertIn('matched_keywords', result)
        
        # They should have the same content
        self.assertEqual(result['matched_terms'], result['matched_keywords'])
    
    def test_negated_terms_field_present(self):
        """Test that 'negated_terms' field is always present."""
        text = "eco-friendly product"
        result = simple_greenwashing_score(text)
        
        self.assertIn('negated_terms', result)
        # Should be an empty list when there are no negations
        self.assertEqual(result['negated_terms'], [])
    
    def test_result_structure(self):
        """Test that result has all expected fields."""
        text = "not eco-friendly but sustainable"
        result = simple_greenwashing_score(text)
        
        # Check all required fields
        self.assertIn('score', result)
        self.assertIn('risk_level', result)
        self.assertIn('matched_terms', result)
        self.assertIn('negated_terms', result)
        self.assertIn('matched_keywords', result)
        
        # Verify types
        self.assertIsInstance(result['score'], int)
        self.assertIsInstance(result['risk_level'], str)
        self.assertIsInstance(result['matched_terms'], list)
        self.assertIsInstance(result['negated_terms'], list)
        self.assertIsInstance(result['matched_keywords'], list)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases for phrase matching and negation."""
    
    def test_empty_text(self):
        """Test that empty text returns empty results."""
        text = ""
        result = simple_greenwashing_score(text)
        
        self.assertEqual(result['score'], 0)
        self.assertEqual(len(result['matched_terms']), 0)
        self.assertEqual(len(result['negated_terms']), 0)
    
    def test_text_with_only_negation_words(self):
        """Test text that only contains negation words."""
        text = "not no never"
        result = simple_greenwashing_score(text)
        
        self.assertEqual(result['score'], 0)
        self.assertEqual(len(result['matched_terms']), 0)
        self.assertEqual(len(result['negated_terms']), 0)
    
    def test_punctuation_doesnt_break_matching(self):
        """Test that punctuation is handled correctly."""
        text = "eco-friendly, carbon-neutral, and plastic-free!"
        result = simple_greenwashing_score(text)
        
        # After cleaning, these should all be matched
        self.assertIn('eco friendly', result['matched_terms'])
        self.assertIn('carbon neutral', result['matched_terms'])
        self.assertIn('plastic free', result['matched_terms'])
    
    def test_negation_with_punctuation(self):
        """Test that negation works even with punctuation."""
        text = "We're not, eco-friendly"
        result = simple_greenwashing_score(text)
        
        # Should still detect negation despite comma
        self.assertIn('eco friendly', result['negated_terms'])
        self.assertEqual(result['score'], 0)


if __name__ == '__main__':
    unittest.main()
