"""
Tests for analytics metrics module.
"""

import unittest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add src to path
src_dir = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_dir))

from analytics.metrics import (
    issuance_overview,
    aggregation_by_country,
    aggregation_by_year,
    aggregation_by_category,
    top_n_concentration,
    herfindahl_index,
    data_coverage_report,
    portfolio_summary_table,
)


class TestIssuanceOverview(unittest.TestCase):
    """Test issuance_overview function."""
    
    def setUp(self):
        """Create test data."""
        self.df = pd.DataFrame({
            'text': ['text1', 'text2', 'text3', 'text4'],
            'score': [10, 20, 30, 40],
            'country': ['USA', 'UK', 'USA', None],
            'year': [2020, 2021, 2022, 2023],
            'amount': [100, 200, 300, 400],
            'issuer': ['CompanyA', 'CompanyB', 'CompanyA', 'CompanyC']
        })
    
    def test_basic_overview(self):
        """Test basic overview metrics."""
        result = issuance_overview(self.df)
        
        self.assertEqual(result['total_records'], 4)
        self.assertEqual(result['total_amount'], 1000)
        self.assertEqual(result['avg_amount'], 250)
        self.assertEqual(result['year_range'], '2020-2023')
        self.assertEqual(result['unique_issuers'], 3)
    
    def test_missing_data_percentage(self):
        """Test missing data percentage calculation."""
        result = issuance_overview(self.df)
        
        self.assertIn('missing_data_pct', result)
        self.assertEqual(result['missing_data_pct']['country'], 25.0)
        self.assertEqual(result['missing_data_pct']['year'], 0.0)
    
    def test_minimal_dataframe(self):
        """Test with minimal DataFrame."""
        df_min = pd.DataFrame({'text': ['a', 'b', 'c']})
        result = issuance_overview(df_min)
        
        self.assertEqual(result['total_records'], 3)
        self.assertNotIn('total_amount', result)
        self.assertNotIn('year_range', result)


class TestAggregationByCountry(unittest.TestCase):
    """Test aggregation_by_country function."""
    
    def setUp(self):
        """Create test data."""
        self.df = pd.DataFrame({
            'country': ['USA', 'UK', 'USA', 'China', 'UK', 'USA'],
            'amount': [100, 200, 150, 300, 250, 200]
        })
    
    def test_aggregation_with_amount(self):
        """Test country aggregation with amount column."""
        result = aggregation_by_country(self.df)
        
        # Check structure
        self.assertIn('country', result.columns)
        self.assertIn('count', result.columns)
        self.assertIn('total_amount', result.columns)
        self.assertIn('share_of_total', result.columns)
        
        # Check values - USA should be first (3 records)
        self.assertEqual(result.iloc[0]['country'], 'USA')
        self.assertEqual(result.iloc[0]['count'], 3)
        self.assertEqual(result.iloc[0]['total_amount'], 450)
        
        # Check shares sum to 100
        self.assertAlmostEqual(result['share_of_total'].sum(), 100.0, places=1)
    
    def test_aggregation_without_amount(self):
        """Test country aggregation without amount column."""
        df_no_amount = self.df.drop(columns=['amount'])
        result = aggregation_by_country(df_no_amount)
        
        self.assertIn('share_of_total', result.columns)
        self.assertNotIn('total_amount', result.columns)
    
    def test_missing_country_column(self):
        """Test error when country column is missing."""
        df_no_country = pd.DataFrame({'text': ['a', 'b']})
        
        with self.assertRaises(KeyError):
            aggregation_by_country(df_no_country)
    
    def test_sorted_descending(self):
        """Test results are sorted by count descending."""
        result = aggregation_by_country(self.df)
        
        # Check counts are in descending order
        counts = result['count'].tolist()
        self.assertEqual(counts, sorted(counts, reverse=True))


class TestAggregationByYear(unittest.TestCase):
    """Test aggregation_by_year function."""
    
    def setUp(self):
        """Create test data."""
        self.df = pd.DataFrame({
            'year': [2020, 2021, 2021, 2022, 2022, 2022],
            'amount': [100, 200, 150, 300, 250, 200]
        })
    
    def test_aggregation_with_amount(self):
        """Test year aggregation with YoY growth."""
        result = aggregation_by_year(self.df)
        
        # Check structure
        self.assertIn('year', result.columns)
        self.assertIn('count', result.columns)
        self.assertIn('total_amount', result.columns)
        self.assertIn('yoy_growth_pct', result.columns)
        
        # Check year order (ascending)
        years = result['year'].tolist()
        self.assertEqual(years, sorted(years))
        
        # Check first year has NaN for YoY growth
        self.assertTrue(pd.isna(result.iloc[0]['yoy_growth_pct']))
    
    def test_yoy_growth_calculation(self):
        """Test year-over-year growth calculation."""
        result = aggregation_by_year(self.df)
        
        # 2021: 350 (from 100 = 250% growth)
        # 2022: 750 (from 350 = ~114% growth)
        self.assertAlmostEqual(result.iloc[1]['yoy_growth_pct'], 250.0, places=1)
    
    def test_missing_year_column(self):
        """Test error when year column is missing."""
        df_no_year = pd.DataFrame({'text': ['a', 'b']})
        
        with self.assertRaises(KeyError):
            aggregation_by_year(df_no_year)


class TestAggregationByCategory(unittest.TestCase):
    """Test aggregation_by_category function."""
    
    def setUp(self):
        """Create test data."""
        self.df = pd.DataFrame({
            'category': ['Food', 'Beauty', 'Food', 'Fashion', 'Beauty', 'Food'],
            'amount': [100, 200, 150, 300, 250, 200]
        })
    
    def test_basic_aggregation(self):
        """Test basic category aggregation."""
        result = aggregation_by_category(self.df, 'category')
        
        # Check structure
        self.assertIn('category', result.columns)
        self.assertIn('count', result.columns)
        self.assertIn('share_of_total', result.columns)
        
        # Check Food is first (3 records)
        self.assertEqual(result.iloc[0]['category'], 'Food')
        self.assertEqual(result.iloc[0]['count'], 3)
    
    def test_missing_column(self):
        """Test error when column doesn't exist."""
        with self.assertRaises(KeyError):
            aggregation_by_category(self.df, 'nonexistent')
    
    def test_empty_after_dropna(self):
        """Test handling when all values are NA."""
        df_all_na = pd.DataFrame({
            'category': [None, None, None],
            'amount': [100, 200, 300]
        })
        
        result = aggregation_by_category(df_all_na, 'category')
        
        # Should return empty DataFrame with correct structure
        self.assertEqual(len(result), 0)
        self.assertIn('category', result.columns)


class TestTopNConcentration(unittest.TestCase):
    """Test top_n_concentration function."""
    
    def setUp(self):
        """Create test data."""
        self.df = pd.DataFrame({
            'country': ['USA'] * 50 + ['UK'] * 20 + ['China'] * 15 + ['Germany'] * 10 + ['France'] * 5,
            'amount': [100] * 100
        })
    
    def test_top_5_concentration(self):
        """Test top 5 concentration calculation."""
        result = top_n_concentration(self.df, 'country', n=5)
        
        # Check structure
        self.assertIn('top_n_items', result)
        self.assertIn('top_n_share', result)
        self.assertIn('concentration_level', result)
        
        # USA should be first
        self.assertEqual(result['top_n_items'][0], 'USA')
        
        # Share should be 100% (all 5 categories)
        self.assertEqual(result['top_n_share'], 100.0)
    
    def test_concentration_levels(self):
        """Test concentration level classification."""
        # Very high concentration (>80%)
        df_high = pd.DataFrame({
            'country': ['USA'] * 90 + ['UK'] * 10
        })
        result = top_n_concentration(df_high, 'country', n=1)
        self.assertEqual(result['concentration_level'], 'Very High')
        
        # Moderate concentration
        df_moderate = pd.DataFrame({
            'country': ['A'] * 20 + ['B'] * 20 + ['C'] * 15 + ['D'] * 15 + ['E'] * 10 + ['F'] * 10 + ['G'] * 10
        })
        result = top_n_concentration(df_moderate, 'country', n=5)
        # Top 5 = A+B+C+D+E = 80/100 = 80% (Very High, at boundary)
        self.assertIn(result['concentration_level'], ['Moderate', 'High', 'Very High'])
        
        # Low concentration
        df_low = pd.DataFrame({
            'country': list('ABCDEFGHIJ') * 10  # 10 countries, evenly distributed
        })
        result = top_n_concentration(df_low, 'country', n=5)
        # Top 5 = 50/100 = 50% (Moderate)
        self.assertIn(result['concentration_level'], ['Low', 'Moderate'])


class TestHerfindahlIndex(unittest.TestCase):
    """Test herfindahl_index function."""
    
    def test_perfect_concentration(self):
        """Test HHI with perfect concentration (one entity)."""
        df = pd.DataFrame({'country': ['USA'] * 100})
        result = herfindahl_index(df, 'country')
        
        # Should be 10000 (100^2)
        self.assertEqual(result['hhi'], 10000.0)
        self.assertEqual(result['normalized_hhi'], 1.0)
        self.assertEqual(result['interpretation'], 'Highly concentrated')
    
    def test_equal_distribution(self):
        """Test HHI with equal distribution."""
        # 10 countries with 10% each
        df = pd.DataFrame({
            'country': ['A'] * 10 + ['B'] * 10 + ['C'] * 10 + ['D'] * 10 + ['E'] * 10 +
                      ['F'] * 10 + ['G'] * 10 + ['H'] * 10 + ['I'] * 10 + ['J'] * 10
        })
        result = herfindahl_index(df, 'country')
        
        # HHI = 10 * (10^2) = 1000
        self.assertEqual(result['hhi'], 1000.0)
        self.assertEqual(result['interpretation'], 'Unconcentrated (competitive)')
    
    def test_bounded_values(self):
        """Test that HHI and normalized HHI are within expected ranges."""
        df = pd.DataFrame({
            'country': ['USA'] * 50 + ['UK'] * 30 + ['China'] * 20
        })
        result = herfindahl_index(df, 'country')
        
        # HHI should be between 0 and 10000
        self.assertGreaterEqual(result['hhi'], 0)
        self.assertLessEqual(result['hhi'], 10000)
        
        # Normalized should be between 0 and 1
        self.assertGreaterEqual(result['normalized_hhi'], 0)
        self.assertLessEqual(result['normalized_hhi'], 1)


class TestDataCoverageReport(unittest.TestCase):
    """Test data_coverage_report function."""
    
    def setUp(self):
        """Create test data."""
        self.df = pd.DataFrame({
            'complete_col': [1, 2, 3, 4, 5],
            'partial_col': [1, 2, None, 4, None],
            'empty_col': [None, None, None, None, None],
            'high_coverage': [1, 2, 3, 4, None]
        })
    
    def test_coverage_calculation(self):
        """Test coverage percentage calculation."""
        result = data_coverage_report(self.df)
        
        # Check structure
        self.assertIn('column_name', result.columns)
        self.assertIn('non_null_count', result.columns)
        self.assertIn('non_null_pct', result.columns)
        self.assertIn('below_threshold', result.columns)
        self.assertIn('notes', result.columns)
        
        # Find specific columns
        complete = result[result['column_name'] == 'complete_col'].iloc[0]
        partial = result[result['column_name'] == 'partial_col'].iloc[0]
        empty = result[result['column_name'] == 'empty_col'].iloc[0]
        
        # Check calculations
        self.assertEqual(complete['non_null_pct'], 100.0)
        self.assertEqual(partial['non_null_pct'], 60.0)
        self.assertEqual(empty['non_null_pct'], 0.0)
    
    def test_below_threshold_flag(self):
        """Test below threshold flagging."""
        result = data_coverage_report(self.df, threshold=80.0)
        
        # partial_col (60%) should be flagged
        partial = result[result['column_name'] == 'partial_col'].iloc[0]
        self.assertTrue(partial['below_threshold'])
        
        # complete_col (100%) should not be flagged
        complete = result[result['column_name'] == 'complete_col'].iloc[0]
        self.assertFalse(complete['below_threshold'])
    
    def test_sorted_by_coverage(self):
        """Test results are sorted by coverage descending."""
        result = data_coverage_report(self.df)
        
        # Check percentages are in descending order
        pcts = result['non_null_pct'].tolist()
        self.assertEqual(pcts, sorted(pcts, reverse=True))


class TestPortfolioSummaryTable(unittest.TestCase):
    """Test portfolio_summary_table function."""
    
    def setUp(self):
        """Create test data."""
        self.df = pd.DataFrame({
            'text': ['text1', 'text2', 'text3', 'text4', 'text5'],
            'score': [10, 20, 30, 40, 50],
            'country': ['USA', 'UK', 'USA', 'China', 'USA'],
            'year': [2020, 2021, 2022, 2023, 2022],
            'amount': [100, 200, 300, 400, 500],
            'issuer': ['CompanyA', 'CompanyB', 'CompanyA', 'CompanyC', 'CompanyD'],
            'risk_level': ['Low', 'Medium', 'High', 'High', 'Medium']
        })
    
    def test_summary_structure(self):
        """Test summary table has correct structure."""
        result = portfolio_summary_table(self.df)
        
        # Check columns
        self.assertIn('metric', result.columns)
        self.assertIn('value', result.columns)
        self.assertIn('notes', result.columns)
        
        # Check has some rows
        self.assertGreater(len(result), 0)
    
    def test_summary_contains_key_metrics(self):
        """Test summary contains expected metrics."""
        result = portfolio_summary_table(self.df)
        
        metrics = result['metric'].tolist()
        
        # Should have total records
        self.assertTrue(any('Total Records' in m for m in metrics))
        
        # Should have amount metrics
        self.assertTrue(any('Total Amount' in m for m in metrics))
    
    def test_minimal_dataframe(self):
        """Test with minimal DataFrame."""
        df_min = pd.DataFrame({'text': ['a', 'b', 'c']})
        result = portfolio_summary_table(df_min)
        
        # Should still return valid DataFrame
        self.assertIsInstance(result, pd.DataFrame)
        self.assertGreater(len(result), 0)
    
    def test_no_plotting(self):
        """Verify function returns only tables, no plots."""
        result = portfolio_summary_table(self.df)
        
        # Should return DataFrame, not matplotlib figure
        self.assertIsInstance(result, pd.DataFrame)


if __name__ == '__main__':
    unittest.main()
