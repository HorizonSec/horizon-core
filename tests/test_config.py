"""Tests for configuration utilities."""

import json
import tempfile
from pathlib import Path
import os
from horizon_core.config import Config, load_config, load_config_with_env


def test_config_creation():
    """Test creating a config object."""
    config = Config({"key": "value"})
    assert config.get("key") == "value"


def test_config_get_default():
    """Test getting a value with default."""
    config = Config()
    assert config.get("missing", "default") == "default"


def test_config_nested_get():
    """Test getting nested values."""
    config = Config({"server": {"port": 8080, "host": "localhost"}})
    assert config.get("server.port") == 8080
    assert config.get("server.host") == "localhost"


def test_config_set():
    """Test setting values."""
    config = Config()
    config.set("key", "value")
    assert config.get("key") == "value"


def test_config_nested_set():
    """Test setting nested values."""
    config = Config()
    config.set("server.port", 8080)
    assert config.get("server.port") == 8080


def test_config_update():
    """Test updating config."""
    config = Config({"a": 1, "b": {"c": 2}})
    config.update({"b": {"d": 3}, "e": 4})
    assert config.get("a") == 1
    assert config.get("b.c") == 2
    assert config.get("b.d") == 3
    assert config.get("e") == 4


def test_config_bracket_notation():
    """Test bracket notation."""
    config = Config()
    config["key"] = "value"
    assert config["key"] == "value"


def test_load_json_config():
    """Test loading JSON config."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"test": "value"}, f)
        filepath = f.name

    try:
        config = load_config(Path(filepath))
        assert config.get("test") == "value"
    finally:
        os.unlink(filepath)


def test_load_config_with_env_variables():
    """Test loading config with environment variables."""
    # Set environment variables
    os.environ["HORIZON_TEST_KEY"] = "test_value"
    os.environ["HORIZON_SERVER__PORT"] = "9000"

    try:
        config = load_config_with_env(env_prefix="HORIZON_")
        assert config.get("test_key") == "test_value"
        # JSON parsing converts "9000" to int 9000
        assert config.get("server.port") == 9000
    finally:
        # Clean up
        os.environ.pop("HORIZON_TEST_KEY", None)
        os.environ.pop("HORIZON_SERVER__PORT", None)


def test_config_to_dict():
    """Test converting config to dict."""
    data = {"a": 1, "b": {"c": 2}}
    config = Config(data)
    result = config.to_dict()
    assert result == data
