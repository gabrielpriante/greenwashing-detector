"""
Config loader for greenwashing scoring.

This module provides functionality to load and validate YAML configuration files
for greenwashing detection scoring.
"""

import os
from pathlib import Path
from typing import Dict, Optional, Any

try:
    import yaml
except ImportError:
    raise ImportError(
        "PyYAML is required for config loading. "
        "Please install it with: pip install pyyaml"
    )


class ConfigError(Exception):
    """Exception raised for configuration-related errors."""
    pass


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load and validate greenwashing scoring configuration from YAML file.
    
    Args:
        config_path: Path to the YAML config file. If None, loads default config.
    
    Returns:
        Dictionary containing validated configuration with 'keywords' and 'thresholds'.
    
    Raises:
        ConfigError: If config file is missing, invalid, or has incorrect structure.
    """
    # Determine config file path
    if config_path is None:
        # Use default config
        current_dir = Path(__file__).parent.parent
        config_path = current_dir / 'config' / 'default_scoring.yml'
    else:
        config_path = Path(config_path)
    
    # Check if file exists
    if not config_path.exists():
        raise ConfigError(
            f"Config file not found: {config_path}\n"
            f"Please ensure the file exists or use the default config."
        )
    
    # Load YAML file
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ConfigError(
            f"Failed to parse YAML config file: {config_path}\n"
            f"Error: {e}"
        )
    except Exception as e:
        raise ConfigError(
            f"Failed to read config file: {config_path}\n"
            f"Error: {e}"
        )
    
    # Validate config structure
    if not isinstance(config, dict):
        raise ConfigError(
            f"Config file must contain a YAML dictionary. "
            f"Got: {type(config).__name__}"
        )
    
    # Validate required keys
    if 'keywords' not in config:
        raise ConfigError(
            "Config file must contain 'keywords' section"
        )
    
    if 'thresholds' not in config:
        raise ConfigError(
            "Config file must contain 'thresholds' section"
        )
    
    # Validate keywords structure
    if not isinstance(config['keywords'], dict):
        raise ConfigError(
            f"'keywords' must be a dictionary. "
            f"Got: {type(config['keywords']).__name__}"
        )
    
    # Flatten keywords from categories into a single dict
    flat_keywords = {}
    for category, keywords in config['keywords'].items():
        if not isinstance(keywords, dict):
            raise ConfigError(
                f"Category '{category}' in 'keywords' must be a dictionary. "
                f"Got: {type(keywords).__name__}"
            )
        
        for keyword, weight in keywords.items():
            if not isinstance(keyword, str):
                raise ConfigError(
                    f"Keyword must be a string. Got: {type(keyword).__name__}"
                )
            
            if not isinstance(weight, (int, float)):
                raise ConfigError(
                    f"Weight for keyword '{keyword}' must be a number. "
                    f"Got: {type(weight).__name__}"
                )
            
            if weight < 0:
                raise ConfigError(
                    f"Weight for keyword '{keyword}' must be non-negative. "
                    f"Got: {weight}"
                )
            
            flat_keywords[keyword] = int(weight)
    
    if not flat_keywords:
        raise ConfigError(
            "Config must contain at least one keyword"
        )
    
    # Validate thresholds structure
    thresholds = config['thresholds']
    if not isinstance(thresholds, dict):
        raise ConfigError(
            f"'thresholds' must be a dictionary. "
            f"Got: {type(thresholds).__name__}"
        )
    
    required_threshold_keys = ['low', 'medium', 'high']
    for key in required_threshold_keys:
        if key not in thresholds:
            raise ConfigError(
                f"'thresholds' must contain '{key}' key"
            )
        
        if not isinstance(thresholds[key], (int, float)):
            raise ConfigError(
                f"Threshold '{key}' must be a number. "
                f"Got: {type(thresholds[key]).__name__}"
            )
    
    # Validate threshold ordering
    if not (thresholds['low'] <= thresholds['medium'] <= thresholds['high']):
        raise ConfigError(
            f"Thresholds must be in ascending order: "
            f"low ({thresholds['low']}) <= medium ({thresholds['medium']}) <= "
            f"high ({thresholds['high']})"
        )
    
    return {
        'keywords': flat_keywords,
        'thresholds': thresholds
    }


def get_default_config() -> Dict[str, Any]:
    """
    Get the default hardcoded configuration (for backward compatibility).
    
    Returns:
        Dictionary containing default keywords and thresholds.
    """
    return {
        'keywords': {
            "eco friendly": 2,
            "environmentally friendly": 2,
            "green": 1,
            "planet friendly": 2,
            "sustainable": 2,
            "sustainably sourced": 3,
            "responsibly sourced": 3,
            "carbon neutral": 4,
            "net zero": 4,
            "zero emissions": 4,
            "climate positive": 4,
            "100 natural": 3,
            "all natural": 3,
            "chemical free": 3,
            "non toxic": 2,
        },
        'thresholds': {
            'low': 0,
            'medium': 30,
            'high': 60
        }
    }
