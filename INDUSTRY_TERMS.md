# Industry-Specific Greenwashing Terms

This document provides categorized lists of common greenwashing terms and phrases used in marketing, organized by industry.

## Overview

The greenwashing terms database contains **264 terms** across **6 industries**:
- Food (42 terms)
- Beauty/Cosmetics (45 terms)
- Fashion (44 terms)
- Electronics (41 terms)
- Home Goods (44 terms)
- Automotive (48 terms)

## Using the Industry Terms Module

### Python API

```python
from src.industry_terms import (
    get_all_industries,
    get_terms_for_industry,
    print_industry_terms,
    print_summary
)

# Get list of all industries
industries = get_all_industries()
print(industries)
# ['Food', 'Beauty_Cosmetics', 'Fashion', 'Electronics', 'Home_Goods', 'Automotive']

# Get terms for a specific industry
food_terms = get_terms_for_industry('Food')
print(food_terms.keys())
# dict_keys(['vague_terms', 'misleading_environmental_claims', 'health_washing', ...])

# Print formatted terms for an industry
print_industry_terms('Fashion')

# Print summary of all terms
print_summary()
```

### Command Line Usage

View all categorized terms:
```bash
python src/industry_terms.py
```

## Industry Categories

### Food Industry

**Categories:**
- Vague Terms (e.g., "all natural", "pure", "clean label")
- Misleading Environmental Claims (e.g., "eco-friendly packaging", "sustainably sourced")
- Health Washing (e.g., "chemical-free", "toxin-free", "detox")
- Organic Related (e.g., "organic-inspired", "made with organic ingredients")
- Packaging Claims (e.g., "recyclable", "biodegradable", "zero waste")

**Common Examples:**
- "100% natural" - often used without clear definition
- "farm fresh" - vague term without specific standards
- "chemical-free" - scientifically impossible, everything is made of chemicals
- "sustainably sourced" - without certification or proof
- "clean label" - marketing term with no regulatory definition

### Beauty/Cosmetics Industry

**Categories:**
- Vague Terms (e.g., "natural beauty", "botanical", "clean beauty")
- Misleading Environmental Claims (e.g., "eco-friendly formula", "reef-safe")
- Chemical Claims (e.g., "chemical-free", "non-toxic", "paraben-free")
- Cruelty Free/Vegan (e.g., "cruelty-free", "not tested on animals")
- Organic/Natural (e.g., "naturally derived", "wild-harvested")
- Packaging Claims (e.g., "refillable", "zero waste beauty")

**Common Examples:**
- "clean beauty" - no standardized definition in industry
- "non-toxic" - all ingredients can be toxic at certain levels
- "botanical" - doesn't mean natural or safe
- "ocean-friendly" - vague without specific standards
- "free from harsh chemicals" - subjective term

### Fashion Industry

**Categories:**
- Vague Terms (e.g., "eco-fashion", "conscious fashion", "slow fashion")
- Material Claims (e.g., "organic cotton", "recycled materials", "bamboo fabric")
- Production Claims (e.g., "ethically made", "fair trade", "sustainably produced")
- Certification Vague (e.g., "certified sustainable", "eco-certified")
- Circular Economy (e.g., "circular fashion", "take-back program")
- Animal Welfare (e.g., "vegan leather", "cruelty-free fashion")

**Common Examples:**
- "sustainable style" - broad term without specific criteria
- "eco-fabric" - vague without material details
- "responsibly sourced" - without third-party verification
- "certified sustainable" - without naming certification body
- "vegan leather" - often made from plastic (not eco-friendly)

### Electronics Industry

**Categories:**
- Vague Terms (e.g., "green tech", "sustainable electronics")
- Energy Claims (e.g., "energy-efficient", "eco mode", "power-saving")
- Material Claims (e.g., "recycled materials", "ocean-bound plastic")
- Packaging Claims (e.g., "plastic-free packaging", "minimal packaging")
- Lifecycle Claims (e.g., "designed for longevity", "repairable", "circular economy")
- Certification Vague (e.g., "eco-certified", "green certified")

**Common Examples:**
- "green tech" - vague without specific metrics
- "energy-efficient" - needs comparison baseline
- "sustainable materials" - without specifics
- "designed for longevity" - no defined lifespan
- "environmentally certified" - without naming certification

### Home Goods Industry

**Categories:**
- Vague Terms (e.g., "eco-home", "green living", "conscious living")
- Cleaning Products (e.g., "natural cleaning", "biodegradable cleaner")
- Material Claims (e.g., "sustainable materials", "reclaimed wood")
- Production Claims (e.g., "sustainably made", "ethically produced")
- Packaging Claims (e.g., "plastic-free", "zero waste", "compostable")
- Performance Claims (e.g., "long-lasting", "built to last")

**Common Examples:**
- "green living" - marketing term without standards
- "natural cleaning" - natural doesn't mean safe or effective
- "eco-friendly materials" - vague without specifics
- "sustainably made" - without certification
- "safe for family and planet" - broad unverified claim

### Automotive Industry

**Categories:**
- Vague Terms (e.g., "eco-friendly vehicle", "green car", "clean mobility")
- Fuel/Emission Claims (e.g., "low emissions", "carbon-neutral", "zero emissions")
- Efficiency Claims (e.g., "fuel-efficient", "high fuel economy", "eco mode")
- Material Claims (e.g., "recycled materials", "vegan leather", "sustainable interior")
- Manufacturing Claims (e.g., "carbon-neutral factory", "green assembly")
- Lifecycle Claims (e.g., "recyclable vehicle", "circular economy")
- Alternative Fuels (e.g., "biofuel compatible", "renewable fuel")

**Common Examples:**
- "green car" - subjective without metrics
- "low emissions" - compared to what?
- "carbon-neutral" - without offset details
- "eco mode" - often minimal impact
- "sustainable lifecycle" - vague claim

## Why These Terms Are Problematic

1. **Vagueness**: Terms lack specific, measurable criteria
2. **No Standards**: Many terms have no regulatory or industry standards
3. **Misleading**: Implies environmental benefits without proof
4. **Partial Truth**: May highlight one aspect while ignoring others
5. **Unverifiable**: Claims made without third-party certification
6. **Irrelevant**: Uses green language for non-environmental features

## How to Identify Greenwashing

When you encounter these terms, ask:

1. **Is it specific?** Does it provide concrete data and metrics?
2. **Is it verified?** Is there third-party certification?
3. **Is it complete?** Does it tell the whole environmental story?
4. **Is it relevant?** Does it relate to actual environmental impact?
5. **Is it comparable?** Are there baselines or comparisons?

## Using These Terms Ethically

If you're in marketing, you can use environmental terms responsibly by:

1. **Being Specific**: Provide concrete data (e.g., "30% recycled content" not "eco-friendly")
2. **Getting Certified**: Use recognized third-party certifications
3. **Being Honest**: Don't exaggerate or hide negative impacts
4. **Providing Proof**: Back claims with evidence and documentation
5. **Being Transparent**: Share full lifecycle impact information

## Data Source

The data is stored in `/data/industry_greenwashing_terms.json` and can be accessed programmatically via the `src/industry_terms.py` module.

## References

- [FTC Green Guides](https://www.ftc.gov/news-events/topics/truth-advertising/green-guides)
- [ISO 14021 Environmental Labels and Declarations](https://www.iso.org/standard/66652.html)
- [TerraChoice Seven Sins of Greenwashing](https://www.ul.com/insights/sins-greenwashing)
- [Greenwashing Index](http://www.greenwashingindex.com/)

## Contributing

To add more terms or industries:
1. Edit `/data/industry_greenwashing_terms.json`
2. Follow the existing structure with categorized terms
3. Update this documentation with new categories
4. Test with `python src/industry_terms.py`
