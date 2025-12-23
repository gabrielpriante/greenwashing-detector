from setuptools import setup, find_packages

setup(
    name="greenwashing-detector",
    version="0.1.0",
    description="A tool for detecting potential greenwashing in text",
    author="Gabriel Priante",
    packages=find_packages(),
    package_dir={"": "."},
    py_modules=["src.cli", "src.greenwashing_scoring", "src.text_cleaning", "src.industry_terms"],
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "scikit-learn>=1.3.0",
        "nltk>=3.8.0",
        "typer>=0.9.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "greenwash=src.cli:app",
        ],
    },
    python_requires=">=3.8",
)
