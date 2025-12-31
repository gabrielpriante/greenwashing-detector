# Portfolio Analytics Metrics

## Overview

The portfolio analytics module provides comprehensive metrics and diagnostics for analyzing batches of greenwashing detection results. This document explains each metric in plain English and states their limitations.

## Core Metrics

### 1. Issuance Overview

**What it does**: Provides a high-level summary of the analyzed portfolio.

**Metrics included**:
- **Total Records**: Count of all analyzed items
- **Total Amount**: Sum of all amounts (if amount column exists)
- **Average Amount**: Mean amount per record
- **Year Range**: Time span covered by the data
- **Unique Issuers**: Number of distinct entities/organizations
- **Missing Data Percentage**: For each key field (country, year, amount, issuer)

**Interpretation**: Use this to understand the scope and completeness of your dataset.

**Limitations**:
- Missing data percentages only cover specified fields
- Does not validate data quality or accuracy
- Assumes year/amount fields are correctly formatted

### 2. Aggregation by Country

**What it does**: Groups records by country and calculates totals and shares.

**Metrics included**:
- **Count**: Number of records per country
- **Total Amount**: Sum of amounts per country (if available)
- **Share of Total**: Percentage contribution to global total

**Interpretation**: Identifies geographic concentration and distribution patterns.

**Limitations**:
- Country names must be standardized (e.g., "USA" vs "United States")
- Records with missing country data are excluded
- Does not account for population, GDP, or other normalization factors
- Potential reporting bias: countries with better data collection may appear more prominent

### 3. Aggregation by Year

**What it does**: Groups records by year with year-over-year growth rates.

**Metrics included**:
- **Count**: Number of records per year
- **Total Amount**: Sum of amounts per year (if available)
- **YoY Growth %**: Year-over-year percentage change

**Interpretation**: Shows temporal trends and growth patterns.

**Limitations**:
- Growth rates can be misleading if early years have very low baseline
- Missing years in the data are not interpolated
- First year has no growth calculation (NaN)
- Does not account for data collection improvements over time
- Reporting lag: recent years may be incomplete

### 4. Aggregation by Category

**What it does**: Generic aggregation function for any categorical field (e.g., project type, certification, currency, issuer type).

**Metrics included**:
- **Count**: Number of records per category
- **Total Amount**: Sum of amounts per category (if available)
- **Share of Total**: Percentage contribution

**Interpretation**: Understand distribution across any dimension in your data.

**Limitations**:
- Category values must be consistent (no typos or variations)
- Records with missing values in the specified column are excluded
- Does not handle hierarchical categories

## Concentration & Coverage Diagnostics

### 5. Top-N Concentration

**What it does**: Calculates what percentage of total activity is concentrated in the top N entities/countries/categories.

**Metrics included**:
- **Top N Items**: List of top N items by count or amount
- **Top N Share**: Percentage of total represented by top N
- **Concentration Level**: Qualitative assessment (Low/Moderate/High/Very High)

**Thresholds**:
- Very High: ≥80%
- High: 60-79%
- Moderate: 40-59%
- Low: <40%

**Interpretation**: High concentration means a few entities dominate the portfolio. Low concentration indicates more balanced distribution.

**Limitations**:
- Thresholds are somewhat arbitrary and may not apply to all contexts
- Does not indicate whether concentration is problematic
- Small sample sizes can produce misleading concentration metrics

### 6. Herfindahl-Hirschman Index (HHI)

**What it does**: Calculates a standard measure of market concentration.

**Formula**: Sum of squared market shares (on 0-10,000 scale)

**Interpretation**:
- **HHI < 1,500**: Unconcentrated (competitive)
- **HHI 1,500-2,500**: Moderately concentrated
- **HHI > 2,500**: Highly concentrated

**Example**: If one entity has 100% share, HHI = 10,000. If 10 entities each have 10% share, HHI = 1,000.

**Limitations**:
- Thresholds based on traditional antitrust analysis, may not apply directly to environmental data
- Sensitive to number of categories (more categories generally = lower HHI)
- Does not indicate cause or desirability of concentration
- Normalized HHI (0-1 scale) helps compare across different datasets

### 7. Data Coverage Report

**What it does**: Shows completeness of each field in the dataset.

**Metrics included**:
- **Column Name**: Name of the field
- **Non-null Count**: How many records have data
- **Non-null %**: Percentage of records with data
- **Below Threshold**: Flag if coverage < 80% (customizable)
- **Notes**: Special annotations (e.g., "Complete coverage", "No data")

**Interpretation**: Identifies data quality issues and coverage gaps.

**Limitations**:
- Only checks for presence of data, not accuracy or validity
- 80% threshold is arbitrary; appropriate threshold depends on use case
- Empty strings or invalid data may still be counted as "present"

## Portfolio Summary Table

**What it does**: Combines headline metrics, concentration analysis, and top categories into a single export-ready table.

**Use case**: Executive summary or report attachment.

**Included metrics**:
- Total records, amounts, year ranges
- Top-N concentration for key dimensions
- HHI for key dimensions
- Top items in each category
- Data quality indicators

**Interpretation**: Provides a one-page overview suitable for presentations or reports.

**Limitations**:
- Summary nature means detail is lost
- Automatically includes whatever columns exist; may not be tailored to specific needs
- Interpretation requires context about the data source and collection method

## General Limitations and Cautions

### Reporting Bias
- Data reflects what is reported, not necessarily what exists
- Some countries, industries, or time periods may have better reporting infrastructure
- Concentration metrics may reflect reporting patterns rather than actual distribution

### Coverage Bias
- Missing data is not random; certain types of entities may be systematically excluded
- Low coverage fields can produce misleading aggregations

### Temporal Issues
- Data collection practices change over time
- Recent years may appear lower due to reporting lag
- Historical data may be less complete

### Currency and Units
- Amount fields assume consistent units
- No currency conversion is performed
- Inflation not accounted for in multi-year comparisons

### Causality
- These metrics are descriptive, not explanatory
- High concentration does not imply good or bad outcomes
- Trends do not indicate causes

## Educational Context

These metrics are designed for:
- **Portfolio screening**: Initial assessment of datasets
- **Transparency**: Understanding data characteristics and limitations
- **Educational purposes**: Learning about concentration and distribution

These metrics are **NOT suitable for**:
- Investment advice or decisions
- Regulatory compliance determinations
- Legal proceedings
- Academic research without additional validation

## Best Practices

1. **Always check data coverage first**: Low coverage invalidates many metrics
2. **Use multiple metrics**: Don't rely on a single measure
3. **Consider context**: Geographic/industry norms matter
4. **Verify data quality**: These functions do not validate input data
5. **Document assumptions**: Note any data cleaning or preprocessing
6. **State limitations**: Be clear about what metrics can and cannot show

## Support and Further Information

For implementation details, see the source code in `src/analytics/metrics.py`.

For usage examples, see the test suite in `tests/test_analytics.py`.

For command-line usage, run: `greenwash summary --help`
