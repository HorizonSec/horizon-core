"""
Configuration management utilities.

This module provides utilities for loading and managing configuration
from various sources (files, environment variables, etc.).
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
import yaml


class Config:
    """Configuration manager."""

    def __init__(self, data: Optional[Dict[str, Any]] = None):
        """
        Initialize configuration.

        Args:
            data: Initial configuration data
        """
        self._data = data or {}

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Args:
            key: Configuration key (supports dot notation, e.g., 'server.port')
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key.split(".")
        value = self._data

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.

        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split(".")
        data = self._data

        for k in keys[:-1]:
            if k not in data or not isinstance(data[k], dict):
                data[k] = {}
            data = data[k]

        data[keys[-1]] = value

    def update(self, data: Dict[str, Any]) -> None:
        """
        Update configuration with new data.

        Args:
            data: Dictionary to merge into configuration
        """
        self._deep_update(self._data, data)

    def _deep_update(self, target: Dict, source: Dict) -> None:
        """Deep update of nested dictionaries."""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_update(target[key], value)
            else:
                target[key] = value

    def to_dict(self) -> Dict[str, Any]:
        """
        Get configuration as dictionary.

        Returns:
            Configuration dictionary
        """
        return self._data.copy()

    def __getitem__(self, key: str) -> Any:
        """Get configuration value using bracket notation."""
        return self.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        """Set configuration value using bracket notation."""
        self.set(key, value)


def load_config(filepath: Path) -> Config:
    """
    Load configuration from a file.

    Supports JSON and YAML formats (determined by file extension).

    Args:
        filepath: Path to configuration file

    Returns:
        Config object

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file format is not supported
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"Configuration file not found: {filepath}")

    suffix = filepath.suffix.lower()

    if suffix == ".json":
        with open(filepath, "r") as f:
            data = json.load(f)
    elif suffix in [".yaml", ".yml"]:
        with open(filepath, "r") as f:
            data = yaml.safe_load(f)
    else:
        raise ValueError(f"Unsupported configuration file format: {suffix}")

    return Config(data)


def load_config_with_env(
    filepath: Optional[Path] = None,
    env_prefix: str = "HORIZON_",
) -> Config:
    """
    Load configuration from file and environment variables.

    Environment variables with the specified prefix will override
    file configuration. Nested keys can be specified with double
    underscores (e.g., HORIZON_SERVER__PORT=8080 -> server.port).

    Args:
        filepath: Optional path to configuration file
        env_prefix: Prefix for environment variables

    Returns:
        Config object
    """
    # Load from file if provided
    if filepath:
        config = load_config(filepath)
    else:
        config = Config()

    # Override with environment variables
    for key, value in os.environ.items():
        if key.startswith(env_prefix):
            # Remove prefix and convert to lowercase
            config_key = key[len(env_prefix):].lower()
            # Replace double underscores with dots for nested keys
            config_key = config_key.replace("__", ".")

            # Try to parse as JSON for complex types
            try:
                parsed_value = json.loads(value)
            except (json.JSONDecodeError, ValueError):
                # Keep as string if not valid JSON
                parsed_value = value

            config.set(config_key, parsed_value)

    return config
