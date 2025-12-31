"""
Portfolio-level metrics for greenwashing analysis.

This module provides functions to compute interpretable portfolio-style
summaries from validated greenwashing detection data.

All functions consume a validated DataFrame and return DataFrames or
dictionaries - no file I/O is performed within core functions.
"""

from typing import Dict, Any, Optional, List
import pandas as pd
import numpy as np


def issuance_overview(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate overview statistics for the analyzed portfolio.
    
    Args:
        df: Validated DataFrame with greenwashing analysis results
        
    Returns:
        Dictionary containing:
        - total_records: Total number of analyzed items
        - total_amount: Total amount if 'amount' column exists
        - year_range: Range of years if 'year' column exists
        - unique_issuers: Count of unique issuers if 'issuer' column exists
        - missing_data: Percentage of missing values for key fields
        
    Assumptions:
        - DataFrame may have optional columns: amount, year, issuer, country
        - All metrics handle missing columns gracefully
    """
    overview = {
        'total_records': len(df),
    }
    
    # Total amount if available
    if 'amount' in df.columns:
        overview['total_amount'] = df['amount'].sum()
        overview['avg_amount'] = df['amount'].mean(skipna=True)
    
    # Year range if available
    if 'year' in df.columns:
        valid_years = df['year'].dropna()
        if len(valid_years) > 0:
            overview['year_min'] = int(valid_years.min())
            overview['year_max'] = int(valid_years.max())
            overview['year_range'] = f"{overview['year_min']}-{overview['year_max']}"
    
    # Unique issuers if available
    if 'issuer' in df.columns:
        overview['unique_issuers'] = df['issuer'].nunique()
    
    # Missing data percentages for key fields
    missing_data = {}
    for col in ['country', 'year', 'amount', 'issuer']:
        if col in df.columns:
            missing_pct = (df[col].isna().sum() / len(df)) * 100
            missing_data[col] = round(missing_pct, 2)
    
    overview['missing_data_pct'] = missing_data
    
    return overview


def aggregation_by_country(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate analysis results by country.
    
    Args:
        df: DataFrame with at least a 'country' column
        
    Returns:
        DataFrame with columns:
        - country: Country name
        - count: Number of records
        - total_amount: Sum of amounts (if amount column exists)
        - share_of_total: Percentage of global total
        
        Sorted by count descending.
        
    Raises:
        KeyError: If 'country' column does not exist
    """
    if 'country' not in df.columns:
        raise KeyError("DataFrame must contain 'country' column")
    
    # Drop NA values in country
    df_valid = df[df['country'].notna()].copy()
    
    # Group by country
    agg_dict = {'country': 'size'}
    
    if 'amount' in df.columns:
        result = df_valid.groupby('country').agg(
            count=('country', 'size'),
            total_amount=('amount', 'sum')
        ).reset_index()
        
        # Calculate share of total
        total_amount = result['total_amount'].sum()
        if total_amount > 0:
            result['share_of_total'] = (result['total_amount'] / total_amount * 100).round(2)
        else:
            result['share_of_total'] = 0.0
    else:
        result = df_valid.groupby('country').size().reset_index(name='count')
        
        # Calculate share based on count
        total_count = result['count'].sum()
        if total_count > 0:
            result['share_of_total'] = (result['count'] / total_count * 100).round(2)
        else:
            result['share_of_total'] = 0.0
    
    # Sort by count descending
    result = result.sort_values('count', ascending=False).reset_index(drop=True)
    
    return result


def aggregation_by_year(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate analysis results by year with year-over-year growth.
    
    Args:
        df: DataFrame with at least a 'year' column
        
    Returns:
        DataFrame with columns:
        - year: Year
        - count: Number of records
        - total_amount: Sum of amounts (if amount column exists)
        - yoy_growth_pct: Year-over-year growth rate
        
        Sorted by year ascending. YoY growth handles missing years safely.
        
    Raises:
        KeyError: If 'year' column does not exist
    """
    if 'year' not in df.columns:
        raise KeyError("DataFrame must contain 'year' column")
    
    # Drop NA values and convert to int
    df_valid = df[df['year'].notna()].copy()
    # Use Int64 for nullable integers to handle float inputs like 2021.0
    df_valid['year'] = pd.to_numeric(df_valid['year'], errors='coerce').astype('Int64')
    
    # Group by year
    if 'amount' in df.columns:
        result = df_valid.groupby('year').agg(
            count=('year', 'size'),
            total_amount=('amount', 'sum')
        ).reset_index()
        
        # Calculate YoY growth based on amount
        result['yoy_growth_pct'] = result['total_amount'].pct_change() * 100
    else:
        result = df_valid.groupby('year').size().reset_index(name='count')
        
        # Calculate YoY growth based on count
        result['yoy_growth_pct'] = result['count'].pct_change() * 100
    
    # Round growth percentages
    result['yoy_growth_pct'] = result['yoy_growth_pct'].round(2)
    
    # Sort by year
    result = result.sort_values('year').reset_index(drop=True)
    
    return result


def aggregation_by_category(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Generic aggregation helper for any categorical column.
    
    Args:
        df: DataFrame with the specified column
        column_name: Name of the column to aggregate by
        
    Returns:
        DataFrame with columns:
        - {column_name}: Category values
        - count: Number of records
        - total_amount: Sum of amounts (if amount column exists)
        - share_of_total: Percentage share
        
        Sorted by count descending.
        
    Raises:
        KeyError: If column_name does not exist in DataFrame
    """
    if column_name not in df.columns:
        raise KeyError(f"DataFrame must contain '{column_name}' column")
    
    # Drop NA values
    df_valid = df[df[column_name].notna()].copy()
    
    if len(df_valid) == 0:
        # Return empty DataFrame with expected structure
        if 'amount' in df.columns:
            return pd.DataFrame(columns=[column_name, 'count', 'total_amount', 'share_of_total'])
        else:
            return pd.DataFrame(columns=[column_name, 'count', 'share_of_total'])
    
    # Group by category
    if 'amount' in df.columns:
        result = df_valid.groupby(column_name).agg(
            count=(column_name, 'size'),
            total_amount=('amount', 'sum')
        ).reset_index()
        
        # Calculate share of total
        total_amount = result['total_amount'].sum()
        if total_amount > 0:
            result['share_of_total'] = (result['total_amount'] / total_amount * 100).round(2)
        else:
            result['share_of_total'] = 0.0
    else:
        result = df_valid.groupby(column_name).size().reset_index(name='count')
        
        # Calculate share based on count
        total_count = result['count'].sum()
        if total_count > 0:
            result['share_of_total'] = (result['count'] / total_count * 100).round(2)
        else:
            result['share_of_total'] = 0.0
    
    # Sort by count descending
    result = result.sort_values('count', ascending=False).reset_index(drop=True)
    
    return result


def top_n_concentration(
    df: pd.DataFrame, 
    column_name: str, 
    n: int = 5, 
    by: str = 'count'
) -> Dict[str, Any]:
    """
    Calculate top-N concentration metrics.
    
    Args:
        df: DataFrame with the specified column
        column_name: Column to analyze concentration
        n: Number of top items to consider (default: 5)
        by: Metric to use for ranking - 'count' or 'amount'
        
    Returns:
        Dictionary containing:
        - top_n_items: List of top N items
        - top_n_share: Percentage share of top N items
        - concentration_level: Qualitative assessment
        
    Example:
        Top 5 countries represent 80% of total records (High concentration)
    """
    if column_name not in df.columns:
        raise KeyError(f"DataFrame must contain '{column_name}' column")
    
    # Get aggregation
    agg_df = aggregation_by_category(df, column_name)
    
    if len(agg_df) == 0:
        return {
            'top_n_items': [],
            'top_n_share': 0.0,
            'concentration_level': 'No data'
        }
    
    # Take top N
    top_n_df = agg_df.head(n)
    
    # Calculate share
    if by == 'amount' and 'total_amount' in agg_df.columns:
        top_n_share = top_n_df['total_amount'].sum() / agg_df['total_amount'].sum() * 100
    else:
        top_n_share = top_n_df['count'].sum() / agg_df['count'].sum() * 100
    
    top_n_share = round(top_n_share, 2)
    
    # Determine concentration level
    if top_n_share >= 80:
        concentration_level = 'Very High'
    elif top_n_share >= 60:
        concentration_level = 'High'
    elif top_n_share >= 40:
        concentration_level = 'Moderate'
    else:
        concentration_level = 'Low'
    
    return {
        'top_n_items': top_n_df[column_name].tolist(),
        'top_n_share': top_n_share,
        'concentration_level': concentration_level,
        'n': len(top_n_df)
    }


def herfindahl_index(df: pd.DataFrame, column_name: str, by: str = 'count') -> Dict[str, Any]:
    """
    Calculate Herfindahl-Hirschman Index (HHI) for concentration measurement.
    
    The HHI is a standard measure of market concentration, calculated as the
    sum of squared market shares. Higher values indicate higher concentration.
    
    Args:
        df: DataFrame with the specified column
        column_name: Column to analyze concentration
        by: Metric to use - 'count' or 'amount'
        
    Returns:
        Dictionary containing:
        - hhi: Herfindahl index (0-10000 scale)
        - normalized_hhi: Normalized HHI (0-1 scale)
        - interpretation: Qualitative interpretation
        
    Notes:
        HHI interpretation (traditional scale):
        - < 1500: Unconcentrated (competitive)
        - 1500-2500: Moderate concentration
        - > 2500: High concentration
    """
    if column_name not in df.columns:
        raise KeyError(f"DataFrame must contain '{column_name}' column")
    
    # Get aggregation
    agg_df = aggregation_by_category(df, column_name)
    
    if len(agg_df) == 0:
        return {
            'hhi': 0.0,
            'normalized_hhi': 0.0,
            'interpretation': 'No data'
        }
    
    # Calculate HHI using share percentages (0-100 scale)
    # Standard HHI uses shares squared, summed
    shares = agg_df['share_of_total'].values
    hhi = np.sum(shares ** 2)
    
    # Normalized HHI (0-1 scale)
    # Max HHI = 10000 (one entity has 100% share)
    normalized_hhi = hhi / 10000
    
    # Interpretation
    if hhi > 2500:
        interpretation = 'Highly concentrated'
    elif hhi > 1500:
        interpretation = 'Moderately concentrated'
    else:
        interpretation = 'Unconcentrated (competitive)'
    
    return {
        'hhi': round(hhi, 2),
        'normalized_hhi': round(normalized_hhi, 4),
        'interpretation': interpretation,
        'num_categories': len(agg_df)
    }


def data_coverage_report(df: pd.DataFrame, threshold: float = 80.0) -> pd.DataFrame:
    """
    Generate field-level data coverage report.
    
    Args:
        df: DataFrame to analyze
        threshold: Percentage threshold for flagging low coverage (default: 80%)
        
    Returns:
        DataFrame with columns:
        - column_name: Name of the column
        - non_null_count: Number of non-null values
        - non_null_pct: Percentage of non-null values
        - below_threshold: Flag if coverage is below threshold
        - notes: Additional notes about coverage
        
        Sorted by non_null_pct descending.
    """
    coverage_data = []
    
    for col in df.columns:
        non_null_count = df[col].notna().sum()
        non_null_pct = (non_null_count / len(df)) * 100
        below_threshold = non_null_pct < threshold
        
        # Generate notes
        notes = []
        if below_threshold:
            notes.append(f"Below {threshold}% threshold")
        if non_null_pct == 0:
            notes.append("No data")
        elif non_null_pct == 100:
            notes.append("Complete coverage")
        
        notes_str = '; '.join(notes) if notes else ''
        
        coverage_data.append({
            'column_name': col,
            'non_null_count': non_null_count,
            'non_null_pct': round(non_null_pct, 2),
            'below_threshold': below_threshold,
            'notes': notes_str
        })
    
    result = pd.DataFrame(coverage_data)
    result = result.sort_values('non_null_pct', ascending=False).reset_index(drop=True)
    
    return result


def portfolio_summary_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a comprehensive, export-ready portfolio summary table.
    
    Combines headline totals, concentration metrics, and top categories
    into a single presentation-ready DataFrame.
    
    Args:
        df: Validated DataFrame with analysis results
        
    Returns:
        DataFrame with summary metrics in a clean, tabular format
        with columns: metric, value, notes
        
    Note:
        This function returns tables only - no plotting.
        Handles missing optional columns gracefully.
    """
    summary_rows = []
    
    # Overview metrics
    overview = issuance_overview(df)
    
    summary_rows.append({
        'metric': 'Total Records',
        'value': str(overview['total_records']),
        'notes': 'Total number of analyzed items'
    })
    
    if 'total_amount' in overview:
        summary_rows.append({
            'metric': 'Total Amount',
            'value': f"{overview['total_amount']:,.2f}",
            'notes': 'Sum of all amounts'
        })
        summary_rows.append({
            'metric': 'Average Amount',
            'value': f"{overview['avg_amount']:,.2f}",
            'notes': 'Mean amount per record'
        })
    
    if 'year_range' in overview:
        summary_rows.append({
            'metric': 'Year Range',
            'value': overview['year_range'],
            'notes': f"From {overview['year_min']} to {overview['year_max']}"
        })
    
    if 'unique_issuers' in overview:
        summary_rows.append({
            'metric': 'Unique Issuers',
            'value': str(overview['unique_issuers']),
            'notes': 'Number of distinct issuers'
        })
    
    # Concentration metrics for available columns
    for col in ['country', 'issuer', 'year']:
        if col in df.columns and df[col].notna().sum() > 0:
            try:
                top5 = top_n_concentration(df, col, n=5)
                summary_rows.append({
                    'metric': f'Top 5 {col.title()} Concentration',
                    'value': f"{top5['top_n_share']}%",
                    'notes': f"{top5['concentration_level']} - {', '.join(map(str, top5['top_n_items'][:3]))}"
                })
                
                hhi = herfindahl_index(df, col)
                summary_rows.append({
                    'metric': f'{col.title()} HHI',
                    'value': str(hhi['hhi']),
                    'notes': hhi['interpretation']
                })
            except Exception:
                # Skip if aggregation fails
                pass
    
    # Top categories
    for col in ['country', 'risk_level', 'category', 'project_type']:
        if col in df.columns and df[col].notna().sum() > 0:
            try:
                agg = aggregation_by_category(df, col)
                if len(agg) > 0:
                    top_item = agg.iloc[0]
                    summary_rows.append({
                        'metric': f'Top {col.title()}',
                        'value': str(top_item[col]),
                        'notes': f"{top_item['count']} records ({top_item['share_of_total']}%)"
                    })
            except Exception:
                # Skip if aggregation fails
                pass
    
    # Data quality
    missing = overview.get('missing_data_pct', {})
    if missing:
        summary_rows.append({
            'metric': 'Data Quality',
            'value': 'See coverage report',
            'notes': f"Missing data in key fields: {len([k for k, v in missing.items() if v > 20])} fields >20%"
        })
    
    result = pd.DataFrame(summary_rows)
    return result
