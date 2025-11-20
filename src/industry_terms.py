"""
Industry-specific greenwashing terms and phrases.

This module provides access to categorized greenwashing terms organized by industry.
Use these terms to better understand common greenwashing patterns in different sectors.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional


def load_industry_terms() -> Dict[str, Dict[str, Dict]]:
    """
    Load industry-specific greenwashing terms from the JSON data file.
    
    Returns:
        Dictionary with industry names as keys and categorized terms with metadata as values.
    """
    data_path = Path(__file__).parent.parent / "data" / "industry_greenwashing_terms.json"
    
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_all_industries() -> List[str]:
    """
    Get a list of all available industries.
    
    Returns:
        List of industry names.
    """
    terms = load_industry_terms()
    return list(terms.keys())


def get_terms_for_industry(industry: str) -> Optional[Dict[str, Dict]]:
    """
    Get all categorized terms for a specific industry.
    
    Args:
        industry: Name of the industry (e.g., "Food", "Beauty_Cosmetics", "Fashion")
    
    Returns:
        Dictionary of categorized terms with metadata for the industry, or None if industry not found.
    """
    terms = load_industry_terms()
    return terms.get(industry)


def get_all_terms_for_industry(industry: str) -> List[str]:
    """
    Get all terms for an industry as a flat list (all categories combined).
    
    Args:
        industry: Name of the industry
    
    Returns:
        Flat list of all terms for the industry.
    """
    industry_data = get_terms_for_industry(industry)
    if not industry_data:
        return []
    
    all_terms = []
    for category_data in industry_data.values():
        # Extract terms from the new structure
        if isinstance(category_data, dict) and 'terms' in category_data:
            all_terms.extend(category_data['terms'])
        elif isinstance(category_data, list):
            # Backward compatibility
            all_terms.extend(category_data)
    
    return all_terms


def print_industry_terms(industry: str, show_categories: bool = True) -> None:
    """
    Print all greenwashing terms for a specific industry in a formatted way.
    
    Args:
        industry: Name of the industry
        show_categories: Whether to show category headers (default: True)
    """
    industry_data = get_terms_for_industry(industry)
    
    if not industry_data:
        print(f"Industry '{industry}' not found.")
        print(f"Available industries: {', '.join(get_all_industries())}")
        return
    
    print(f"\n{'='*70}")
    print(f"Greenwashing Terms for {industry.replace('_', '/')}")
    print(f"{'='*70}\n")
    
    for category, category_data in industry_data.items():
        # Extract terms from the new structure
        if isinstance(category_data, dict) and 'terms' in category_data:
            terms = category_data['terms']
            rationale = category_data.get('rationale', '')
            source = category_data.get('source', '')
        elif isinstance(category_data, list):
            # Backward compatibility
            terms = category_data
            rationale = ''
            source = ''
        else:
            continue
            
        if show_categories:
            print(f"{category.replace('_', ' ').title()}:")
            if rationale:
                print(f"  Rationale: {rationale}")
            if source:
                print(f"  Source: {source}")
            for term in terms:
                print(f"  • {term}")
            print()
        else:
            for term in terms:
                print(f"  • {term}")
    
    # Calculate total terms
    total_terms = 0
    for category_data in industry_data.values():
        if isinstance(category_data, dict) and 'terms' in category_data:
            total_terms += len(category_data['terms'])
        elif isinstance(category_data, list):
            total_terms += len(category_data)
    
    print(f"\nTotal terms: {total_terms}")


def print_all_industry_terms(show_categories: bool = True) -> None:
    """
    Print greenwashing terms for all industries.
    
    Args:
        show_categories: Whether to show category headers (default: True)
    """
    industries = get_all_industries()
    
    for i, industry in enumerate(industries):
        print_industry_terms(industry, show_categories)
        
        # Add separator between industries (but not after the last one)
        if i < len(industries) - 1:
            print("\n" + "~"*70 + "\n")


def get_summary_statistics() -> Dict[str, int]:
    """
    Get summary statistics about the greenwashing terms database.
    
    Returns:
        Dictionary with statistics (total industries, total terms, etc.)
    """
    all_terms = load_industry_terms()
    
    total_industries = len(all_terms)
    total_terms = 0
    terms_per_industry = {}
    
    for industry, categories in all_terms.items():
        industry_term_count = 0
        for category_data in categories.values():
            if isinstance(category_data, dict) and 'terms' in category_data:
                industry_term_count += len(category_data['terms'])
            elif isinstance(category_data, list):
                industry_term_count += len(category_data)
        total_terms += industry_term_count
        terms_per_industry[industry] = industry_term_count
    
    return {
        "total_industries": total_industries,
        "total_terms": total_terms,
        "average_terms_per_industry": total_terms / total_industries if total_industries > 0 else 0,
        "terms_per_industry": terms_per_industry
    }


def print_summary() -> None:
    """
    Print a summary of the greenwashing terms database.
    """
    stats = get_summary_statistics()
    
    print("\n" + "="*70)
    print("Greenwashing Terms Database Summary")
    print("="*70 + "\n")
    
    print(f"Total Industries: {stats['total_industries']}")
    print(f"Total Terms: {stats['total_terms']}")
    print(f"Average Terms per Industry: {stats['average_terms_per_industry']:.1f}\n")
    
    print("Terms by Industry:")
    for industry, count in sorted(stats['terms_per_industry'].items(), key=lambda x: x[1], reverse=True):
        print(f"  • {industry.replace('_', '/')}: {count} terms")
    print()


if __name__ == "__main__":
    # When run as a script, display all terms organized by industry
    print_summary()
    print_all_industry_terms(show_categories=True)
