#!/usr/bin/env python3
"""
Example: Using custom YAML configuration for greenwashing detection

This example demonstrates how to customize the greenwashing detector
by using a custom YAML configuration file.
"""

import sys
from pathlib import Path
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from greenwashing_scoring import simple_greenwashing_score
import tempfile


def main():
    test_text = "Our eco-friendly and sustainable product is 100% natural"
    temp_files = []  # Track temp files for cleanup
    
    print("=" * 70)
    print("Custom Configuration Example")
    print("=" * 70)
    print(f"\nAnalyzing: '{test_text}'\n")
    
    # Example 1: Default configuration
    print("1. Using default configuration:")
    print("-" * 70)
    result_default = simple_greenwashing_score(test_text)
    print(f"   Score: {result_default['score']}/100")
    print(f"   Risk Level: {result_default['risk_level']}")
    print(f"   Matched Keywords: {', '.join(result_default['matched_keywords'])}")
    
    # Example 2: Stricter detection (higher weights)
    print("\n2. Using stricter detection (higher keyword weights):")
    print("-" * 70)
    stricter_config = """
# Stricter configuration - flags more aggressively
keywords:
  environmental:
    eco friendly: 5
    sustainable: 5
    100 natural: 8
  
thresholds:
  low: 0
  medium: 30
  high: 60
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        f.write(stricter_config)
        stricter_path = f.name
        temp_files.append(stricter_path)
    
    result_strict = simple_greenwashing_score(test_text, stricter_path)
    print(f"   Score: {result_strict['score']}/100")
    print(f"   Risk Level: {result_strict['risk_level']}")
    print(f"   Matched Keywords: {', '.join(result_strict['matched_keywords'])}")
    print(f"   Note: Score increased from {result_default['score']} to {result_strict['score']}")
    
    # Example 3: More lenient thresholds
    print("\n3. Using more lenient thresholds:")
    print("-" * 70)
    lenient_config = """
# More lenient - requires higher scores for high risk
keywords:
  environmental:
    eco friendly: 2
    sustainable: 2
    100 natural: 3

thresholds:
  low: 0
  medium: 50
  high: 80
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        f.write(lenient_config)
        lenient_path = f.name
        temp_files.append(lenient_path)
    
    result_lenient = simple_greenwashing_score(test_text, lenient_path)
    print(f"   Score: {result_lenient['score']}/100")
    print(f"   Risk Level: {result_lenient['risk_level']}")
    print(f"   Matched Keywords: {', '.join(result_lenient['matched_keywords'])}")
    print(f"   Note: Same score ({result_lenient['score']}) now classified as '{result_lenient['risk_level']}' risk")
    
    # Example 4: Custom industry-specific keywords
    print("\n4. Custom configuration for specific industry:")
    print("-" * 70)
    custom_industry = """
# Custom keywords for a specific industry
keywords:
  fashion_specific:
    eco friendly: 2
    sustainable: 3
    ethically made: 4
    fair trade: 3
    organic cotton: 4

thresholds:
  low: 0
  medium: 30
  high: 60
"""
    
    industry_text = "Our ethically made organic cotton product"
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        f.write(custom_industry)
        industry_path = f.name
        temp_files.append(industry_path)
    
    result_industry = simple_greenwashing_score(industry_text, industry_path)
    print(f"   Text: '{industry_text}'")
    print(f"   Score: {result_industry['score']}/100")
    print(f"   Risk Level: {result_industry['risk_level']}")
    print(f"   Matched Keywords: {', '.join(result_industry['matched_keywords'])}")
    
    print("\n" + "=" * 70)
    print("Summary:")
    print("=" * 70)
    print("✓ Custom YAML configs allow you to:")
    print("  - Adjust keyword weights to be more/less strict")
    print("  - Change risk thresholds to match your standards")
    print("  - Add industry-specific keywords")
    print("  - Organize keywords by category for maintainability")
    print("\n✓ The default scoring.yml is located at: config/default_scoring.yml")
    print("✓ Create your own config and use: simple_greenwashing_score(text, 'config.yml')")
    print("=" * 70)
    
    # Clean up temporary files
    for temp_file in temp_files:
        try:
            os.unlink(temp_file)
        except OSError:
            pass


if __name__ == '__main__':
    main()
