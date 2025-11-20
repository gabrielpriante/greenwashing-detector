"""
Basic tests for the greenwashing terms database.

These tests verify the integrity of the data structure and ensure
that the JSON loads correctly.
"""

import json
import unittest
from pathlib import Path


class TestIndustryTermsData(unittest.TestCase):
    """Test the industry greenwashing terms JSON data."""
    
    @classmethod
    def setUpClass(cls):
        """Load the JSON data once for all tests."""
        data_path = Path(__file__).parent.parent / "data" / "industry_greenwashing_terms.json"
        with open(data_path, 'r', encoding='utf-8') as f:
            cls.data = json.load(f)
    
    def test_json_loads_correctly(self):
        """Test that the JSON file loads without errors."""
        self.assertIsNotNone(self.data)
        self.assertIsInstance(self.data, dict)
    
    def test_has_expected_industries(self):
        """Test that all expected industries are present."""
        expected_industries = ['Food', 'Beauty_Cosmetics', 'Fashion', 
                              'Electronics', 'Home_Goods', 'Automotive']
        self.assertEqual(set(self.data.keys()), set(expected_industries))
    
    def test_each_industry_has_categories(self):
        """Test that each industry has at least one category."""
        for industry, categories in self.data.items():
            self.assertIsInstance(categories, dict, 
                                f"{industry} should have categories as a dict")
            self.assertGreater(len(categories), 0, 
                             f"{industry} should have at least one category")
    
    def test_categories_have_required_structure(self):
        """Test that each category has the required structure with terms, rationale, and source."""
        for industry, categories in self.data.items():
            for category, category_data in categories.items():
                self.assertIsInstance(category_data, dict,
                                    f"{industry}.{category} should be a dict")
                self.assertIn('terms', category_data,
                            f"{industry}.{category} should have 'terms' field")
                self.assertIn('rationale', category_data,
                            f"{industry}.{category} should have 'rationale' field")
                self.assertIn('source', category_data,
                            f"{industry}.{category} should have 'source' field")
    
    def test_terms_are_arrays(self):
        """Test that all terms fields contain arrays."""
        for industry, categories in self.data.items():
            for category, category_data in categories.items():
                self.assertIsInstance(category_data['terms'], list,
                                    f"{industry}.{category}.terms should be a list")
    
    def test_terms_are_strings(self):
        """Test that all terms in arrays are strings."""
        for industry, categories in self.data.items():
            for category, category_data in categories.items():
                for term in category_data['terms']:
                    self.assertIsInstance(term, str,
                                        f"All terms in {industry}.{category} should be strings")
    
    def test_no_empty_term_arrays(self):
        """Test that no category has an empty terms array."""
        for industry, categories in self.data.items():
            for category, category_data in categories.items():
                self.assertGreater(len(category_data['terms']), 0,
                                 f"{industry}.{category} should have at least one term")
    
    def test_rationale_and_source_are_strings(self):
        """Test that rationale and source fields are strings."""
        for industry, categories in self.data.items():
            for category, category_data in categories.items():
                self.assertIsInstance(category_data['rationale'], str,
                                    f"{industry}.{category}.rationale should be a string")
                self.assertIsInstance(category_data['source'], str,
                                    f"{industry}.{category}.source should be a string")
    
    def test_total_term_count(self):
        """Test that the total number of terms is reasonable."""
        total_terms = 0
        for categories in self.data.values():
            for category_data in categories.values():
                total_terms += len(category_data['terms'])
        
        # We expect around 264 terms based on the original data
        self.assertGreater(total_terms, 200, "Should have at least 200 terms total")
        self.assertLess(total_terms, 500, "Should have less than 500 terms total")


if __name__ == '__main__':
    unittest.main()
