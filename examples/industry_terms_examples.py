"""
Example script showing how to use the industry-specific greenwashing terms.

This script demonstrates various ways to access and use the categorized
greenwashing terms for different industries.
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from industry_terms import (
    get_all_industries,
    get_terms_for_industry,
    get_all_terms_for_industry,
    print_industry_terms,
    print_summary,
    get_summary_statistics
)


def example_1_list_all_industries():
    """Example 1: Get a list of all available industries"""
    print("\n" + "="*70)
    print("Example 1: List All Industries")
    print("="*70 + "\n")
    
    industries = get_all_industries()
    print(f"Available industries ({len(industries)}):")
    for industry in industries:
        print(f"  • {industry.replace('_', '/')}")


def example_2_get_food_terms():
    """Example 2: Get all terms for the Food industry"""
    print("\n" + "="*70)
    print("Example 2: Get Food Industry Terms")
    print("="*70 + "\n")
    
    food_terms = get_terms_for_industry('Food')
    
    if food_terms:
        print("Food industry categories:")
        for category, category_data in food_terms.items():
            # Handle new structure with metadata
            if isinstance(category_data, dict) and 'terms' in category_data:
                terms = category_data['terms']
            else:
                terms = category_data
            
            print(f"\n{category.replace('_', ' ').title()} ({len(terms)} terms):")
            # Show first 5 terms as examples
            for term in terms[:5]:
                print(f"  • {term}")
            if len(terms) > 5:
                print(f"  ... and {len(terms) - 5} more")


def example_3_check_text_for_greenwashing():
    """Example 3: Check sample texts for greenwashing terms"""
    print("\n" + "="*70)
    print("Example 3: Check Sample Texts for Greenwashing")
    print("="*70 + "\n")
    
    sample_texts = {
        "Food": "Our 100% natural, chemical-free snack is sustainably sourced and eco-friendly!",
        "Beauty_Cosmetics": "This clean beauty formula is toxin-free and made with botanical ingredients.",
        "Fashion": "Sustainable style meets eco-fashion in our organic cotton, ethically made clothing.",
        "Electronics": "Our green tech device features energy-efficient design with recyclable materials.",
        "Home_Goods": "Natural cleaning power in an eco-friendly, biodegradable formula for green living.",
        "Automotive": "Experience our eco-friendly vehicle with low emissions and sustainable interior."
    }
    
    for industry, text in sample_texts.items():
        print(f"\nIndustry: {industry.replace('_', '/')}")
        print(f"Sample text: \"{text}\"")
        
        # Get all terms for this industry
        all_terms = get_all_terms_for_industry(industry)
        
        # Find matching terms (case-insensitive)
        text_lower = text.lower()
        matches = [term for term in all_terms if term.lower() in text_lower]
        
        print(f"Greenwashing terms found: {len(matches)}")
        for match in matches:
            print(f"  ⚠️  '{match}'")


def example_4_compare_industries():
    """Example 4: Compare term counts across industries"""
    print("\n" + "="*70)
    print("Example 4: Compare Industries")
    print("="*70 + "\n")
    
    stats = get_summary_statistics()
    
    print("Terms per industry (sorted by count):\n")
    sorted_industries = sorted(
        stats['terms_per_industry'].items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    for industry, count in sorted_industries:
        bar = "█" * (count // 3)  # Simple bar chart
        print(f"{industry.replace('_', '/'):20} {count:3} {bar}")


def example_5_search_specific_category():
    """Example 5: Search for terms in a specific category"""
    print("\n" + "="*70)
    print("Example 5: Search Specific Categories")
    print("="*70 + "\n")
    
    # Look for "packaging" related terms across all industries
    print("Packaging-related terms across all industries:\n")
    
    for industry in get_all_industries():
        industry_data = get_terms_for_industry(industry)
        if industry_data:
            for category, category_data in industry_data.items():
                if 'packaging' in category.lower():
                    # Handle new structure with metadata
                    if isinstance(category_data, dict) and 'terms' in category_data:
                        terms = category_data['terms']
                    else:
                        terms = category_data
                    
                    print(f"{industry.replace('_', '/')} - {category.replace('_', ' ').title()}:")
                    for term in terms:
                        print(f"  • {term}")
                    print()


def example_6_export_to_simple_list():
    """Example 6: Export all terms as a simple flat list"""
    print("\n" + "="*70)
    print("Example 6: Export Fashion Terms as Simple List")
    print("="*70 + "\n")
    
    fashion_terms = get_all_terms_for_industry('Fashion')
    
    print(f"All Fashion greenwashing terms ({len(fashion_terms)} total):\n")
    for i, term in enumerate(fashion_terms, 1):
        print(f"{i:3}. {term}")


def main():
    """Run all examples"""
    print("\n" + "#"*70)
    print("# Industry-Specific Greenwashing Terms - Usage Examples")
    print("#"*70)
    
    # Run all examples
    example_1_list_all_industries()
    example_2_get_food_terms()
    example_3_check_text_for_greenwashing()
    example_4_compare_industries()
    example_5_search_specific_category()
    example_6_export_to_simple_list()
    
    # Show summary at the end
    print("\n" + "#"*70)
    print("# Database Summary")
    print("#"*70)
    print_summary()
    
    print("\n" + "#"*70)
    print("# For detailed view of any industry, use:")
    print("#   from src.industry_terms import print_industry_terms")
    print("#   print_industry_terms('Food')")
    print("#"*70 + "\n")


if __name__ == "__main__":
    main()
