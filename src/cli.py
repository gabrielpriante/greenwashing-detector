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
except ImportError:
    print("Error: Required packages not installed. Please run: pip install typer rich")
    sys.exit(1)

# Add src directory to path for imports
src_dir = Path(__file__).parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Import greenwashing scoring functions
from greenwashing_scoring import simple_greenwashing_score

app = typer.Typer(
    help="Greenwashing Detector CLI - Analyze text for potential greenwashing",
    no_args_is_help=True,
    invoke_without_command=False
)
console = Console()


def format_rich_report(text: str, result: dict) -> None:
    """Format and display analysis result using rich formatting."""
    word_count = len(text.split())
    
    # Create info panel
    info_text = f"""[bold]Text Length:[/bold] {word_count} words
[bold]Greenwashing Score:[/bold] {result['score']}/100
[bold]Risk Level:[/bold] {result['risk_level']}"""
    
    console.print(Panel(info_text, title="Analysis Summary", border_style="blue"))
    
    # Display matched keywords
    matched = result.get('matched_keywords', [])
    if matched:
        console.print(f"\n[bold]Matched Keywords ({len(matched)}):[/bold]")
        for keyword in matched:
            console.print(f"  • {keyword}", style="yellow")
    else:
        console.print("\n[green]No greenwashing keywords detected.[/green]")
    
    console.print()


@app.command(name="analyze")
def analyze_command(
    text: Optional[str] = typer.Argument(None, help="Text to analyze for greenwashing"),
    file: Optional[Path] = typer.Option(None, "--file", "-f", help="CSV file to process in batch mode"),
    text_col: Optional[str] = typer.Option(None, "--text-col", "-c", help="Column name containing text to analyze"),
    out: Optional[Path] = typer.Option(None, "--out", "-o", help="Output CSV file path"),
    format_type: Optional[str] = typer.Option("text", "--format", help="Output format: text or json"),
):
    """
    Analyze text or CSV file for potential greenwashing.
    
    Examples:
    
      greenwash analyze "eco-friendly and all natural"
      
      greenwash analyze --file products.csv --text-col description --out results.csv
      
      greenwash analyze --file products.csv --text-col description --format json
    """
    # Single text analysis mode
    if text and not file:
        if not text.strip():
            console.print("[red]Error: Text cannot be empty[/red]")
            raise typer.Exit(1)
        
        result = simple_greenwashing_score(text)
        
        if format_type == "json":
            output = {
                "text": text,
                "score": result['score'],
                "risk_level": result['risk_level'],
                "matched_keywords": result['matched_keywords'],
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
                
                # Check if text_col exists
                if reader.fieldnames is None:
                    console.print(f"[red]Error: CSV file is empty or invalid[/red]")
                    raise typer.Exit(1)
                
                if text_col not in reader.fieldnames:
                    console.print(f"[red]Error: Column '{text_col}' not found in CSV[/red]")
                    console.print(f"Available columns: {', '.join(reader.fieldnames)}")
                    raise typer.Exit(1)
                
                # Process rows
                results = []
                for row in reader:
                    text_value = row.get(text_col, "")
                    
                    if not text_value or not text_value.strip():
                        # Handle empty text
                        results.append({
                            **row,
                            'score': 0,
                            'risk_level': 'Low',
                            'matched_terms': '',
                            'matched_count': 0
                        })
                    else:
                        analysis = simple_greenwashing_score(text_value)
                        results.append({
                            **row,
                            'score': analysis['score'],
                            'risk_level': analysis['risk_level'],
                            'matched_terms': ', '.join(analysis['matched_keywords']),
                            'matched_count': len(analysis['matched_keywords'])
                        })
                
                # Output results
                if format_type == "json":
                    # JSON output to stdout
                    output = []
                    for result in results:
                        output.append({
                            text_col: result[text_col],
                            'score': result['score'],
                            'risk_level': result['risk_level'],
                            'matched_terms': result['matched_terms'].split(', ') if result['matched_terms'] else [],
                            'matched_count': result['matched_count']
                        })
                    console.print(json.dumps(output, indent=2))
                else:
                    # CSV output
                    if not out:
                        console.print("[red]Error: --out is required for CSV format[/red]")
                        raise typer.Exit(1)
                    
                    # Get fieldnames (original + new columns)
                    fieldnames = list(reader.fieldnames) + ['score', 'risk_level', 'matched_terms', 'matched_count']
                    
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


if __name__ == "__main__":
    app()
