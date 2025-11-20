"""
Tests for the industry_terms module functions.

These tests verify that the API functions work correctly with the data.
"""

import sys
from pathlib import Path
import unittest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from industry_terms import (
    get_all_industries,
    get_terms_for_industry,
    get_all_terms_for_industry,
    get_summary_statistics
)


class TestIndustryTermsAPI(unittest.TestCase):
    """Test the industry_terms module API functions."""
    
    def test_get_all_industries(self):
        """Test that get_all_industries returns expected industries."""
        industries = get_all_industries()
        self.assertIsInstance(industries, list)
        self.assertEqual(len(industries), 6)
        self.assertIn('Food', industries)
        self.assertIn('Beauty_Cosmetics', industries)
        self.assertIn('Fashion', industries)
        self.assertIn('Electronics', industries)
        self.assertIn('Home_Goods', industries)
        self.assertIn('Automotive', industries)
    
    def test_get_terms_for_industry_valid(self):
        """Test getting terms for a valid industry."""
        food_terms = get_terms_for_industry('Food')
        self.assertIsNotNone(food_terms)
        self.assertIsInstance(food_terms, dict)
        self.assertGreater(len(food_terms), 0)
    
    def test_get_terms_for_industry_invalid(self):
        """Test getting terms for an invalid industry returns None."""
        result = get_terms_for_industry('NonExistent')
        self.assertIsNone(result)
    
    def test_get_all_terms_for_industry(self):
        """Test getting all terms as a flat list for an industry."""
        food_terms = get_all_terms_for_industry('Food')
        self.assertIsInstance(food_terms, list)
        self.assertGreater(len(food_terms), 0)
        # Check that all items are strings
        for term in food_terms:
            self.assertIsInstance(term, str)
    
    def test_get_all_terms_for_invalid_industry(self):
        """Test getting terms for invalid industry returns empty list."""
        terms = get_all_terms_for_industry('NonExistent')
        self.assertEqual(terms, [])
    
    def test_get_summary_statistics(self):
        """Test that summary statistics returns expected data."""
        stats = get_summary_statistics()
        self.assertIsInstance(stats, dict)
        self.assertIn('total_industries', stats)
        self.assertIn('total_terms', stats)
        self.assertIn('average_terms_per_industry', stats)
        self.assertIn('terms_per_industry', stats)
        
        self.assertEqual(stats['total_industries'], 6)
        self.assertGreater(stats['total_terms'], 200)
        self.assertGreater(stats['average_terms_per_industry'], 30)
    
    def test_terms_per_industry_in_stats(self):
        """Test that terms_per_industry has correct structure."""
        stats = get_summary_statistics()
        terms_per_industry = stats['terms_per_industry']
        
        self.assertIsInstance(terms_per_industry, dict)
        self.assertEqual(len(terms_per_industry), 6)
        
        for industry, count in terms_per_industry.items():
            self.assertIsInstance(count, int)
            self.assertGreater(count, 0)


if __name__ == '__main__':
    unittest.main()
