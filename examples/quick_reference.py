"""
Quick Reference: Print a concise list of greenwashing terms by industry.
This script outputs a simplified view suitable for quick reference.
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from industry_terms import load_industry_terms


def print_quick_reference():
    """Print a quick reference guide of all greenwashing terms"""
    
    print("="*80)
    print("GREENWASHING TERMS QUICK REFERENCE GUIDE".center(80))
    print("Common Marketing Terms That May Indicate Greenwashing".center(80))
    print("="*80)
    print()
    
    all_terms = load_industry_terms()
    
    for industry_name, categories in all_terms.items():
        # Print industry header
        display_name = industry_name.replace('_', '/')
        print(f"\n{'─'*80}")
        print(f"  {display_name.upper()}")
        print(f"{'─'*80}")
        
        # Count total terms for this industry
        total = sum(len(terms) for terms in categories.values())
        print(f"  ({total} terms)")
        print()
        
        # Print each category
        for category_name, terms in categories.items():
            category_display = category_name.replace('_', ' ').title()
            print(f"  • {category_display}:")
            
            # Print terms in columns (3 per row for readability)
            for i in range(0, len(terms), 3):
                row_terms = terms[i:i+3]
                formatted_row = "    - " + " | ".join(f"{term:<25}" for term in row_terms)
                print(formatted_row.rstrip())
            print()
    
    print("="*80)
    print(f"Total: {sum(sum(len(t) for t in c.values()) for c in all_terms.values())} terms across {len(all_terms)} industries")
    print("="*80)
    print("\nWHY THESE TERMS ARE PROBLEMATIC:")
    print("  • Often vague and lack specific, measurable criteria")
    print("  • May not have regulatory or industry standard definitions")
    print("  • Can mislead consumers about actual environmental impact")
    print("  • Often used without third-party verification")
    print("  • May highlight one positive aspect while ignoring negatives")
    print("\nHOW TO USE RESPONSIBLY:")
    print("  • Provide specific data and metrics")
    print("  • Get third-party certification")
    print("  • Be transparent about full lifecycle impact")
    print("  • Support claims with evidence")
    print("  • Avoid exaggeration")
    print()
    print("For detailed information, see: INDUSTRY_TERMS.md")
    print("="*80)


if __name__ == "__main__":
    print_quick_reference()
