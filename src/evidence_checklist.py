"""
Evidence Checklist Generator for Environmental Claims

This module provides mappings from environmental claims to evidence checklist items
that should be verified to substantiate those claims.
"""

from typing import Dict, List, Set

# Mapping of environmental claims to required evidence checklist items
CLAIM_EVIDENCE_MAPPING: Dict[str, List[str]] = {
    "carbon neutral": [
        "Scope definition (Scope 1, 2, 3 emissions included?)",
        "Baseline year for carbon calculations",
        "Methodology used for carbon accounting",
        "Third-party verification or audit",
        "Certification ID or registry entry",
        "Timeframe for achieving carbon neutrality",
        "Details on carbon offsets purchased (if any)",
    ],
    "net zero": [
        "Scope definition (Scope 1, 2, 3 emissions included?)",
        "Baseline year for emissions calculations",
        "Methodology and standards used (e.g., SBTi)",
        "Third-party verification or audit",
        "Certification ID or registry entry",
        "Target timeframe and interim milestones",
        "Emissions reduction vs. offset breakdown",
    ],
    "zero emissions": [
        "Scope definition (which emissions are included?)",
        "Baseline year for comparison",
        "Methodology for emissions measurement",
        "Third-party verification or audit",
        "Timeframe and context (e.g., manufacturing, use phase)",
        "Certification or testing results",
    ],
    "biodegradable": [
        "Testing standards used (e.g., ASTM D6400, EN 13432)",
        "Timeframe for biodegradation",
        "Conditions required for biodegradation",
        "Third-party certification (e.g., BPI, DIN CERTCO)",
        "Certification ID or test report",
        "Percentage of material that biodegrades",
    ],
    "compostable": [
        "Composting standards met (e.g., ASTM D6400, EN 13432)",
        "Type of composting (industrial vs. home)",
        "Timeframe for composting",
        "Third-party certification (e.g., BPI, TÜV Austria)",
        "Certification ID or test report",
        "Conditions required for proper composting",
    ],
    "recyclable": [
        "Recycling standards or codes (e.g., resin code)",
        "Infrastructure availability for recycling",
        "Percentage of material that is recyclable",
        "Third-party testing or certification",
        "Geographic limitations (where it can be recycled)",
        "Preparation requirements for recycling",
    ],
    "sustainable sourcing": [
        "Definition of 'sustainable' in this context",
        "Third-party certification (e.g., FSC, MSC, Rainforest Alliance)",
        "Certification ID and scope",
        "Percentage of materials sustainably sourced",
        "Traceability documentation",
        "Audit reports or supply chain verification",
    ],
    "sustainably sourced": [
        "Definition of 'sustainable' in this context",
        "Third-party certification (e.g., FSC, MSC, Rainforest Alliance)",
        "Certification ID and scope",
        "Percentage of materials sustainably sourced",
        "Traceability documentation",
        "Audit reports or supply chain verification",
    ],
    "non toxic": [
        "Testing standards used (e.g., ASTM, ISO)",
        "Definition of 'non-toxic' and threshold levels",
        "Third-party testing or certification",
        "Test report or certification ID",
        "Specific chemicals or substances excluded",
        "Regulatory compliance (e.g., EPA, EU regulations)",
    ],
    "chemical free": [
        "Definition of 'chemical-free' (clarification needed)",
        "List of specific chemicals excluded",
        "Testing methodology and standards",
        "Third-party testing or certification",
        "Test report or certification ID",
        "Context (synthetic chemicals, harmful chemicals, etc.)",
    ],
    "plastic free": [
        "Definition and scope (all plastic or specific types?)",
        "Testing or verification methodology",
        "Third-party certification or audit",
        "Certification ID or test report",
        "Alternative materials used",
        "Packaging vs. product distinction",
    ],
    "all natural": [
        "Definition of 'natural' used",
        "Percentage of natural ingredients",
        "Source and origin of ingredients",
        "Processing methods used",
        "Third-party certification (e.g., USDA Organic, NSF)",
        "Certification ID or documentation",
    ],
    "100 natural": [
        "Definition of 'natural' used",
        "Percentage of natural ingredients (should be 100%)",
        "Source and origin of all ingredients",
        "Processing methods used",
        "Third-party certification (e.g., USDA Organic, NSF)",
        "Certification ID or documentation",
    ],
    "eco friendly": [
        "Definition of 'eco-friendly' in this context",
        "Environmental impact assessment",
        "Third-party certification (e.g., EcoLogo, Green Seal)",
        "Certification ID or environmental report",
        "Lifecycle analysis or carbon footprint data",
        "Comparative claims substantiation",
    ],
    "environmentally friendly": [
        "Definition of 'environmentally friendly' in this context",
        "Environmental impact assessment",
        "Third-party certification (e.g., EcoLogo, Green Seal)",
        "Certification ID or environmental report",
        "Lifecycle analysis or carbon footprint data",
        "Comparative claims substantiation",
    ],
    "green": [
        "Definition of 'green' in this context",
        "Specific environmental benefits claimed",
        "Third-party certification or eco-label",
        "Certification ID or environmental documentation",
        "Lifecycle analysis or environmental impact data",
        "Substantiation of environmental claims",
    ],
    "sustainable": [
        "Definition of 'sustainable' in this context",
        "Sustainability standards or frameworks used",
        "Third-party certification or assessment",
        "Certification ID or sustainability report",
        "Metrics and targets for sustainability",
        "Lifecycle analysis or impact assessment",
    ],
    "planet friendly": [
        "Definition of 'planet friendly' in this context",
        "Environmental impact assessment",
        "Third-party certification or eco-label",
        "Certification ID or environmental report",
        "Lifecycle analysis or carbon footprint data",
        "Comparative environmental benefits",
    ],
    "climate positive": [
        "Definition and calculation methodology",
        "Baseline year and emissions data",
        "Carbon removal or offset details",
        "Third-party verification or audit",
        "Certification ID or registry entry",
        "Timeframe and ongoing monitoring",
    ],
}


def get_evidence_checklist(matched_terms: List[str]) -> Dict[str, List[str]]:
    """
    Generate evidence checklist based on matched environmental claims.
    
    Args:
        matched_terms: List of matched greenwashing terms from analysis
    
    Returns:
        Dictionary mapping each matched term to its evidence checklist items
    """
    checklist = {}
    
    for term in matched_terms:
        if term in CLAIM_EVIDENCE_MAPPING:
            checklist[term] = CLAIM_EVIDENCE_MAPPING[term]
    
    return checklist


def get_all_evidence_items(matched_terms: List[str]) -> List[str]:
    """
    Get a deduplicated flat list of all evidence items for matched terms.
    
    Args:
        matched_terms: List of matched greenwashing terms from analysis
    
    Returns:
        Deduplicated list of all evidence checklist items
    """
    all_items: Set[str] = set()
    
    for term in matched_terms:
        if term in CLAIM_EVIDENCE_MAPPING:
            all_items.update(CLAIM_EVIDENCE_MAPPING[term])
    
    return sorted(list(all_items))


def format_evidence_checklist(checklist: Dict[str, List[str]]) -> str:
    """
    Format evidence checklist as a readable string.
    
    Args:
        checklist: Dictionary mapping terms to evidence items
    
    Returns:
        Formatted string with evidence checklist
    """
    if not checklist:
        return ""
    
    output = []
    for term, items in checklist.items():
        output.append(f"\n'{term}':")
        for item in items:
            output.append(f"  • {item}")
    
    return "\n".join(output)
