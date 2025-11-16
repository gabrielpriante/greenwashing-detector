# Greenwashing Detector

A simple, beginner-friendly Python tool for detecting potential greenwashing in marketing and product claims.

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

## How to Use

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

Contributions are welcome! Some ways to help:
- Add more greenwashing keywords
- Improve the scoring algorithm
- Add example datasets
- Enhance documentation
- Report bugs or suggest features

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