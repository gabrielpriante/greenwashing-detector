#!/usr/bin/env python3
"""
CLI for Greenwashing Detector

Provides command-line interface for analyzing text and CSV files
for potential greenwashing content.
"""

import sys
from pathlib import Path
from typing import Optional
import csv
import json

try:
    import typer
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    import pandas as pd
except ImportError:
    print("Error: Required packages not installed. Please run: pip install -r requirements.txt")
    sys.exit(1)

# Add src directory to path for imports
src_dir = Path(__file__).parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Import greenwashing scoring functions
from greenwashing_scoring import simple_greenwashing_score

# Import analytics functions
try:
    from analytics.metrics import (
        issuance_overview,
        aggregation_by_country,
        aggregation_by_year,
        aggregation_by_category,
        data_coverage_report,
        portfolio_summary_table,
    )
except ImportError:
    # Analytics module not available
    pass

app = typer.Typer(
    help="Greenwashing Detector CLI - Analyze text for potential greenwashing",
    no_args_is_help=True,
    invoke_without_command=False
)
console = Console()


def get_matched_terms(result: dict) -> list:
    """
    Extract matched terms from result with backward compatibility fallback.
    
    Args:
        result: The scoring result dictionary
    
    Returns:
        List of matched terms
    """
    return result.get('matched_terms', result.get('matched_keywords', []))


def format_rich_report(text: str, result: dict) -> None:
    """Format and display analysis result using rich formatting."""
    word_count = len(text.split())
    
    # Create info panel
    info_text = f"""[bold]Text Length:[/bold] {word_count} words
[bold]Greenwashing Score:[/bold] {result['score']}/100
[bold]Risk Level:[/bold] {result['risk_level']}"""
    
    console.print(Panel(info_text, title="Analysis Summary", border_style="blue"))
    
    # Display matched keywords
    matched = get_matched_terms(result)
    if matched:
        console.print(f"\n[bold]Matched Keywords ({len(matched)}):[/bold]")
        for keyword in matched:
            console.print(f"  • {keyword}", style="yellow")
    else:
        console.print("\n[green]No greenwashing keywords detected.[/green]")
    
    # Display negated terms
    negated = result.get('negated_terms', [])
    if negated:
        console.print(f"\n[bold]Negated Terms ({len(negated)}):[/bold]")
        console.print("[dim](These terms were found but negated, so they don't count toward the score)[/dim]")
        for keyword in negated:
            console.print(f"  • {keyword}", style="cyan")
    
    # Display evidence checklist
    evidence_checklist = result.get('evidence_checklist', {})
    if evidence_checklist:
        console.print(f"\n[bold]Suggested evidence to look for:[/bold]")
        for claim, items in evidence_checklist.items():
            console.print(f"\n[yellow]'{claim}':[/yellow]")
            for item in items:
                console.print(f"  • {item}", style="dim")
    
    console.print()


@app.command(name="analyze")
def analyze_command(
    text: Optional[str] = typer.Argument(None, help="Text to analyze for greenwashing"),
    file: Optional[Path] = typer.Option(None, "--file", "-f", help="CSV file to process in batch mode"),
    text_col: Optional[str] = typer.Option(None, "--text-col", "-c", help="Column name containing text to analyze"),
    out: Optional[Path] = typer.Option(None, "--out", "-o", help="Output CSV file path"),
    format_type: Optional[str] = typer.Option("text", "--format", help="Output format: text or json"),
    config: Optional[Path] = typer.Option(None, "--config", help="Path to custom YAML config file"),
):
    """
    Analyze text or CSV file for potential greenwashing.
    
    Examples:
    
      greenwash analyze "eco-friendly and all natural"
      
      greenwash analyze --file products.csv --text-col description --out results.csv
      
      greenwash analyze --file products.csv --text-col description --format json
      
      greenwash analyze "eco-friendly" --config custom_config.yml
    """
    # Validate config file if provided
    config_path = None
    if config:
        if not config.exists():
            console.print(f"[red]Error: Config file not found: {config}[/red]")
            raise typer.Exit(1)
        config_path = str(config)
    
    # Single text analysis mode
    if text and not file:
        if not text.strip():
            console.print("[red]Error: Text cannot be empty[/red]")
            raise typer.Exit(1)
        
        try:
            result = simple_greenwashing_score(text, config_path)
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise typer.Exit(1)
        
        if format_type == "json":
            matched = get_matched_terms(result)
            output = {
                "text": text,
                "score": result['score'],
                "risk_level": result['risk_level'],
                "matched_terms": matched,
                "matched_keywords": matched,  # Backward compatibility
                "negated_terms": result.get('negated_terms', []),
                "evidence_checklist": result.get('evidence_checklist', {}),
            }
            console.print(json.dumps(output, indent=2))
        else:
            format_rich_report(text, result)
        
        return
    
    # CSV batch mode
    if file:
        if not text_col:
            console.print("[red]Error: --text-col is required when using --file[/red]")
            raise typer.Exit(1)
        
        if not file.exists():
            console.print(f"[red]Error: File not found: {file}[/red]")
            raise typer.Exit(1)
        
        try:
            with open(file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                # Check if text_col exists and capture fieldnames
                if reader.fieldnames is None:
                    console.print(f"[red]Error: CSV file is empty or invalid[/red]")
                    raise typer.Exit(1)
                
                # Capture fieldnames before consuming the reader
                original_fieldnames = list(reader.fieldnames)
                
                if text_col not in original_fieldnames:
                    console.print(f"[red]Error: Column '{text_col}' not found in CSV[/red]")
                    console.print(f"Available columns: {', '.join(original_fieldnames)}")
                    raise typer.Exit(1)
                
                # Process rows
                results = []
                for row in reader:
                    text_value = row.get(text_col, "")
                    
                    if not text_value or not text_value.strip():
                        # Handle empty text
                        matched_str = ''
                        results.append({
                            **row,
                            'score': 0,
                            'risk_level': 'Low',
                            'matched_terms': matched_str,
                            'matched_keywords': matched_str,  # Backward compatibility
                            'matched_count': 0,
                            'negated_terms': '',
                            'evidence_checklist': ''
                        })
                    else:
                        try:
                            analysis = simple_greenwashing_score(text_value, config_path)
                        except Exception as e:
                            console.print(f"[red]Error processing row: {e}[/red]")
                            raise typer.Exit(1)
                        matched_str = ', '.join(get_matched_terms(analysis))
                        # Format evidence checklist for CSV
                        evidence_dict = analysis.get('evidence_checklist', {})
                        evidence_str = json.dumps(evidence_dict) if evidence_dict else ''
                        results.append({
                            **row,
                            'score': analysis['score'],
                            'risk_level': analysis['risk_level'],
                            'matched_terms': matched_str,
                            'matched_keywords': matched_str,  # Backward compatibility
                            'matched_count': len(get_matched_terms(analysis)),
                            'negated_terms': ', '.join(analysis.get('negated_terms', [])),
                            'evidence_checklist': evidence_str
                        })
                
                # Output results
                if format_type == "json":
                    # JSON output to stdout
                    output = []
                    for result in results:
                        matched_list = result['matched_terms'].split(', ') if result['matched_terms'] else []
                        evidence_dict = json.loads(result['evidence_checklist']) if result['evidence_checklist'] else {}
                        output.append({
                            text_col: result[text_col],
                            'score': result['score'],
                            'risk_level': result['risk_level'],
                            'matched_terms': matched_list,
                            'matched_keywords': matched_list,  # Backward compatibility
                            'matched_count': result['matched_count'],
                            'negated_terms': result['negated_terms'].split(', ') if result['negated_terms'] else [],
                            'evidence_checklist': evidence_dict
                        })
                    console.print(json.dumps(output, indent=2))
                else:
                    # CSV output
                    if not out:
                        console.print("[red]Error: --out is required for CSV format[/red]")
                        raise typer.Exit(1)
                    
                    # Get fieldnames (original + new columns)
                    fieldnames = original_fieldnames + ['score', 'risk_level', 'matched_terms', 'matched_keywords', 'matched_count', 'negated_terms', 'evidence_checklist']
                    
                    with open(out, 'w', encoding='utf-8', newline='') as outfile:
                        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(results)
                    
                    console.print(f"[green]✓ Processed {len(results)} rows[/green]")
                    console.print(f"[green]✓ Results saved to: {out}[/green]")
        
        except csv.Error as e:
            console.print(f"[red]Error reading CSV file: {e}[/red]")
            raise typer.Exit(1)
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            raise typer.Exit(1)
        
        return
    
    # No arguments provided
    console.print("[yellow]No input provided. Use --help for usage information.[/yellow]")
    raise typer.Exit(1)


@app.command(name="version", hidden=True)
def version_command():
    """Show version information."""
    console.print("greenwashing-detector version 0.1.0")


@app.command(name="summary")
def summary_command(
    file: Path = typer.Argument(..., help="CSV file to analyze"),
    output_dir: Optional[Path] = typer.Option(None, "--output-dir", "-o", help="Output directory for reports (default: ./outputs)"),
):
    """
    Generate portfolio-level analytics summary from CSV data.
    
    This command analyzes a CSV file containing greenwashing detection results
    and generates comprehensive portfolio metrics including:
    - Overview statistics (total records, year ranges, etc.)
    - Concentration analysis by country, year, and other dimensions
    - Data coverage report showing completeness of fields
    
    Examples:
    
      greenwash summary data/processed/green_bonds.csv
      
      greenwash summary results.csv --output-dir reports/
    """
    # Check if analytics module is available
    try:
        from analytics.metrics import (
            issuance_overview,
            data_coverage_report,
            portfolio_summary_table,
        )
    except ImportError:
        console.print("[red]Error: Analytics module not available[/red]")
        raise typer.Exit(1)
    
    # Validate input file
    if not file.exists():
        console.print(f"[red]Error: File not found: {file}[/red]")
        raise typer.Exit(1)
    
    # Set output directory
    if output_dir is None:
        output_dir = Path("./outputs")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Load CSV file
        console.print(f"[blue]Loading data from {file}...[/blue]")
        df = pd.read_csv(file)
        
        if len(df) == 0:
            console.print("[yellow]Warning: CSV file is empty[/yellow]")
            raise typer.Exit(1)
        
        console.print(f"[green]✓ Loaded {len(df)} records[/green]\n")
        
        # Generate overview
        console.print("[bold blue]Portfolio Overview[/bold blue]")
        console.print("=" * 60)
        
        overview = issuance_overview(df)
        
        # Display overview in console
        console.print(f"Total Records: {overview['total_records']}")
        
        if 'total_amount' in overview:
            console.print(f"Total Amount: {overview['total_amount']:,.2f}")
            console.print(f"Average Amount: {overview['avg_amount']:,.2f}")
        
        if 'year_range' in overview:
            console.print(f"Year Range: {overview['year_range']}")
        
        if 'unique_issuers' in overview:
            console.print(f"Unique Issuers: {overview['unique_issuers']}")
        
        # Missing data
        if overview.get('missing_data_pct'):
            console.print("\n[bold]Data Completeness:[/bold]")
            for field, pct in overview['missing_data_pct'].items():
                status = "[green]✓[/green]" if pct < 20 else "[yellow]⚠[/yellow]" if pct < 50 else "[red]✗[/red]"
                console.print(f"  {status} {field}: {100-pct:.1f}% complete")
        
        console.print()
        
        # Generate portfolio summary table
        console.print("[bold blue]Generating Portfolio Summary...[/bold blue]")
        summary_table = portfolio_summary_table(df)
        summary_output = output_dir / "portfolio_summary.csv"
        summary_table.to_csv(summary_output, index=False)
        console.print(f"[green]✓ Portfolio summary saved to: {summary_output}[/green]")
        
        # Display summary table in console
        if len(summary_table) > 0:
            console.print("\n[bold]Key Metrics:[/bold]")
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("Metric", style="dim")
            table.add_column("Value", style="magenta")
            table.add_column("Notes", style="dim")
            
            for _, row in summary_table.head(10).iterrows():
                table.add_row(str(row['metric']), str(row['value']), str(row['notes']))
            
            console.print(table)
        
        # Generate data coverage report
        console.print("\n[bold blue]Generating Data Coverage Report...[/bold blue]")
        coverage = data_coverage_report(df, threshold=80.0)
        coverage_output = output_dir / "data_coverage_report.csv"
        coverage.to_csv(coverage_output, index=False)
        console.print(f"[green]✓ Coverage report saved to: {coverage_output}[/green]")
        
        # Display critical coverage issues
        low_coverage = coverage[coverage['below_threshold'] == True]
        if len(low_coverage) > 0:
            console.print("\n[yellow]⚠ Fields with <80% coverage:[/yellow]")
            for _, row in low_coverage.iterrows():
                console.print(f"  • {row['column_name']}: {row['non_null_pct']:.1f}%")
        else:
            console.print("\n[green]✓ All fields have ≥80% coverage[/green]")
        
        console.print(f"\n[bold green]Summary complete![/bold green]")
        console.print(f"Reports saved to: {output_dir.absolute()}")
        
    except pd.errors.EmptyDataError:
        console.print("[red]Error: CSV file is empty or invalid[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error processing file: {e}[/red]")
        import traceback
        console.print(traceback.format_exc())
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
