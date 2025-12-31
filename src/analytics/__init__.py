"""
Analytics module for portfolio-level greenwashing analysis.

This module provides metrics and aggregation functions for analyzing
batches of greenwashing detection results.
"""

from .metrics import (
    issuance_overview,
    aggregation_by_country,
    aggregation_by_year,
    aggregation_by_category,
    top_n_concentration,
    herfindahl_index,
    data_coverage_report,
    portfolio_summary_table,
)

__all__ = [
    'issuance_overview',
    'aggregation_by_country',
    'aggregation_by_year',
    'aggregation_by_category',
    'top_n_concentration',
    'herfindahl_index',
    'data_coverage_report',
    'portfolio_summary_table',
]
