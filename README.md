# Greenwashing Detector

A simple, beginner-friendly Python tool for detecting potential greenwashing in marketing and product claims.

> **Disclaimer**: This tool is designed to raise awareness and assist with early screening of environmental language in corporate marketing, advertising, and public communications. It is not intended to make definitive claims about greenwashing or to analyze academic research. The analysis is based on keyword matching and may flag legitimate claims or miss sophisticated greenwashing tactics. For serious evaluation of environmental claims, please consult environmental experts and verify against recognized standards and certifications.

## What is Greenwashing?

Greenwashing occurs when companies make misleading or unsubstantiated environmental claims about their products or services. This tool uses keyword-based analysis to identify potentially misleading "green" marketing language.

## Project Purpose

This project provides a basic framework for analyzing text to detect common greenwashing patterns, including:
- Vague environmental claims without specific data
- Overuse of green-sounding buzzwords
- Misleading terms like "chemical-free" or "all natural"

**Note**: This is a simple educational tool using keyword matching. Real greenwashing detection requires verification of claims, understanding of environmental standards, and expert review.

## Project Structure

```
greenwashing-detector/
│
├── data/                          # Place your data files here (CSV, TXT, etc.)
│
├── notebooks/                     # Jupyter notebooks for analysis
│   └── greenwashing_analysis.ipynb  # Starter notebook for text analysis
│
├── src/                           # Source code modules
│   ├── __init__.py               # Package initialization
│   ├── text_cleaner.py           # Text cleaning and preprocessing utilities
│   └── scoring.py                # Keyword-based greenwashing scoring
│
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
├── LICENSE                       # Project license
└── README.md                     # This file
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/gabrielpriante/greenwashing-detector.git
   cd greenwashing-detector
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the CLI tool** (optional, for command-line usage):
   ```bash
   pip install -e .
   ```

## How to Use

### Using the Command-Line Interface (CLI)

The fastest way to analyze text is using the `greenwash` command-line tool:

#### Analyze a single text string

```bash
greenwash analyze "eco-friendly and all natural"
```

Output:
```
╭──────────────────────── Analysis Summary ────────────────────────╮
│ Text Length: 4 words                                             │
│ Greenwashing Score: 50/100                                       │
│ Risk Level: Medium                                               │
╰──────────────────────────────────────────────────────────────────╯

Matched Keywords (2):
  • eco friendly
  • all natural
```

#### Get JSON output

```bash
greenwash analyze "eco-friendly and all natural" --format json
```

#### Process a CSV file in batch mode

```bash
greenwash analyze --file products.csv --text-col description --out results.csv
```

This will:
- Read `products.csv`
- Analyze the text in the `description` column
- Add new columns: `score`, `risk_level`, `matched_terms`, `matched_count`
- Save results to `results.csv`

#### Output CSV analysis as JSON

```bash
greenwash analyze --file products.csv --text-col description --format json
```

This outputs the analysis results as JSON to stdout (useful for piping to other tools).

### Running the Jupyter Notebook

The easiest way to get started is with the interactive Jupyter notebook:

1. **Start Jupyter**:
   ```bash
   jupyter notebook
   ```

2. **Open the notebook**: Navigate to `notebooks/greenwashing_analysis.ipynb`

3. **Run the cells**: Follow the step-by-step guide to:
   - Clean and preprocess text
   - Analyze text for greenwashing keywords
   - Visualize results
   - Try your own examples

### Using the Modules in Python

You can also import and use the modules directly in your Python code:

```python
from src.text_cleaner import clean_text, extract_keywords
from src.scoring import calculate_greenwashing_score, analyze_text

# Example text
text = "Our eco-friendly product is 100% natural and chemical-free!"

# Clean the text
cleaned = clean_text(text)
print(f"Cleaned: {cleaned}")

# Analyze for greenwashing
result = calculate_greenwashing_score(text)
print(f"Score: {result['score']}/100")
print(f"Risk Level: {result['risk_level']}")

# Get a detailed report
print(analyze_text(text))
```

## Features

### Command-Line Interface (`greenwash` CLI)
- Analyze single text strings with rich formatted output
- Batch process CSV files with greenwashing scores
- JSON output for integration with other tools
- Error handling for missing files, columns, and empty text
- Clean terminal output using Rich library

### Text Cleaning (`text_cleaner.py`)
- Remove URLs, emails, and special characters
- Convert to lowercase
- Remove stopwords (optional)
- Extract keywords
- Tokenize text

### Greenwashing Scoring (`scoring.py`)
- Keyword-based detection of common greenwashing terms
- Weighted scoring system (higher weights for more suspicious terms)
- Normalized scores to account for text length
- Risk level categorization (Low/Medium/High)
- Detailed reporting of matched keywords

### Jupyter Notebook
- Interactive text analysis
- Sample product claims to analyze
- Visualizations of results
- Educational content about greenwashing

## Keyword Categories

The detector looks for two types of problematic terms:

1. **Common greenwashing keywords**: eco-friendly, natural, sustainable, green, organic, etc.
2. **Vague/misleading terms**: chemical-free, all natural, safe for planet, etc.

Each keyword has a weight based on how often it's misused in greenwashing. You can view and modify these in `src/scoring.py`.

### Industry-Specific Greenwashing Terms

This project includes a comprehensive database of **264 greenwashing terms** organized by **6 industries**:
- **Food** (42 terms): vague terms, misleading environmental claims, health washing, organic-related, packaging claims
- **Beauty/Cosmetics** (45 terms): vague terms, misleading environmental claims, chemical claims, cruelty-free/vegan, organic/natural, packaging claims
- **Fashion** (44 terms): vague terms, material claims, production claims, certification vague, circular economy, animal welfare
- **Electronics** (41 terms): vague terms, energy claims, material claims, packaging claims, lifecycle claims
- **Home Goods** (44 terms): vague terms, cleaning products, material claims, production claims, packaging claims, performance claims
- **Automotive** (48 terms): vague terms, fuel/emission claims, efficiency claims, material claims, manufacturing claims, lifecycle claims, alternative fuels

To use industry-specific terms:
```python
from src.industry_terms import print_industry_terms, get_terms_for_industry

# View all terms for an industry
print_industry_terms('Food')

# Get terms programmatically
food_terms = get_terms_for_industry('Food')
```

For a complete guide, see [INDUSTRY_TERMS.md](INDUSTRY_TERMS.md) or run:
```bash
python src/industry_terms.py
python examples/industry_terms_examples.py
```

## Example Output

```
Greenwashing Detection Report
==================================================

Text Length: 15 words
Greenwashing Score: 26.67/100
Risk Level: High

Matched Keywords (4):
  - 'eco-friendly': appeared 1x (weight: 3, contribution: 3)
  - 'natural': appeared 1x (weight: 3, contribution: 3)
  - 'chemical-free': appeared 1x (weight: 3, contribution: 3) [VAGUE]
  - 'green': appeared 1x (weight: 3, contribution: 3)

Total Raw Score: 12
```

## Limitations

This is a **basic educational tool** with important limitations:

- ✗ Does not verify if environmental claims are true
- ✗ Cannot detect sophisticated greenwashing tactics
- ✗ Doesn't understand context or nuance
- ✗ May flag legitimate environmental claims
- ✗ Only works with English text
- ✗ Based on simple keyword matching, not machine learning

For production use, you would need:
- Fact-checking against environmental databases
- Understanding of industry-specific regulations
- Natural language understanding (NLP/ML models)
- Expert domain knowledge
- Certification verification

## Intended Use

This tool is most relevant for **exploratory analysis of corporate sustainability language** in:

- **Corporate marketing materials**: Product descriptions, advertisements, packaging claims
- **Company communications**: Press releases, sustainability reports, websites
- **Public filings**: Corporate disclosures and environmental statements
- **Social media**: Brand posts and campaigns with environmental messaging

**Not suitable for**:
- Academic research requiring rigorous methodology
- Legal proceedings or formal complaints
- Making definitive determinations of greenwashing
- Analyzing peer-reviewed scientific literature

The tool serves as a **starting point for awareness and discussion**, helping to identify language patterns that may warrant further investigation by qualified experts.

## Next Steps / Improvements

To expand this project, consider:

1. **Add more data**: Create a dataset of real greenwashing examples
2. **Expand keywords**: Add industry-specific terms and phrases
3. **Context analysis**: Look for supporting evidence in claims
4. **Certification checking**: Verify mentions of environmental certifications
5. **Export functionality**: Save analysis results to files
6. **Web interface**: Create a simple Flask/Streamlit app
7. **Comparative analysis**: Compare claims across similar products

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

Quick ways to help:
- Suggest greenwashing terms with sources
- Improve documentation
- Report bugs or issues
- Add test coverage

## Testing

The project includes a basic test suite to verify data integrity:

```bash
# Run all tests
python -m unittest discover tests -v

# Run specific test file
python -m unittest tests.test_industry_terms_data -v
```

Tests verify:
- JSON structure integrity
- All industries have required categories
- Terms are properly formatted
- API functions work correctly

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This is an educational project for learning about greenwashing and text analysis
- Keywords based on common greenwashing patterns identified by environmental organizations
- Built with Python, NLTK, pandas, and Jupyter

## Resources

To learn more about greenwashing:
- [FTC Green Guides](https://www.ftc.gov/news-events/topics/truth-advertising/green-guides)
- [Greenwashing Index](http://www.greenwashingindex.com/)
- [TerraChoice Seven Sins of Greenwashing](https://www.ul.com/insights/sins-greenwashing)