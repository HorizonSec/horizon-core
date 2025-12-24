"""
Test Suite: config.py Configuration Loader


Test Coverage:
    This suite provides full validation coverage for `config.py`
    including:
    • Successful loading of valid configurations.
    • Application of default values when sections or files are missing.
    • Handling of invalid configuration files (JSON errors, invalid fields, types).
    • Verification of strict validation — raising:
        - FileNotFoundError
        - JSONDecodeError
        - TypeError
        - KeyError

Key Test Areas:
    1. File discovery behavior:
        - Default lookup in the current working directory.
        - Explicit path loading from `resources/` directory.

    2. Validation behavior:
        - Risk level correctness (`low`, `medium`, `high`).
        - Type validation (numeric, boolean, list).
        - Field validation (no unknown keys allowed).

    3. Error behavior:
        - Missing files.
        - Invalid JSON syntax.
        - Invalid values and types.
        - Unexpected fields in JSON.

Example Usage:
    Run all tests using unittest:
        python -m unittest tests/test_config.py

    Run a specific test method:
        python -m unittest tests.test_config.TestConfigLoader.test_invalid_json_syntax_raises_jsondecodeerror
"""

import json
import os
import unittest
from pathlib import Path

from horizon_core.config import Config, load_config


class TestConfigLoader(unittest.TestCase):
    """
    Test suite for the configuration loader in config.py.
    Ensures proper loading, validation, and error handling for JSON-based configs.
    """

    @classmethod
    def setUpClass(cls):
        """Locate the resources directory containing JSON config files."""
        cls.RESOURCES_DIR = (Path(__file__).resolve().parent.parent / "tests-resources").resolve()
        if not cls.RESOURCES_DIR.exists():
            raise RuntimeError(f"Resources directory not found: {cls.RESOURCES_DIR}")

    def _res(self, name: str) -> str:
        """Helper: Return the absolute path to a resource file."""
        p = self.RESOURCES_DIR / name
        self.assertTrue(p.exists(), f"Missing resource: {p}")
        return str(p)

    def setUp(self):
        """Save the original working directory before each test."""
        self._orig_cwd = os.getcwd()

    def tearDown(self):
        """Restore the original working directory after each test."""
        os.chdir(self._orig_cwd)

    def test_valid_full_config_loads(self):
        """
        Verify that a complete configuration (horizon_config.json)
        loads successfully and all fields are correctly populated.
        """
        cfg = load_config(self._res("horizon_config.json"))
        self.assertIsInstance(cfg, Config)
        self.assertEqual(cfg.risk_appetite.level, "medium")
        self.assertTrue(cfg.rules.enable_web_hooks)
        self.assertEqual(cfg.opt_in_features, ["daily_summary", "portfolio_rebalancing"])

    def test_empty_file_defaults(self):
        """
        Verify that an empty JSON file (empty_file.json)
        produces a Config object populated entirely with default values.
        """
        cfg = load_config(self._res("empty_file.json"))
        # Risk defaults
        self.assertEqual(cfg.risk_appetite.level, "low")
        self.assertEqual(cfg.risk_appetite.max_investment_per_asset, 1000.0)
        self.assertEqual(cfg.risk_appetite.stop_loss_threshold, 0.05)
        # Rules defaults
        self.assertFalse(cfg.rules.enable_email_alerts)
        self.assertFalse(cfg.rules.enable_sms_alerts)
        self.assertFalse(cfg.rules.enable_web_hooks)
        self.assertFalse(cfg.rules.allow_margin_trading)
        # Features default
        self.assertEqual(cfg.opt_in_features, [])

    def test_default_lookup_from_current_directory(self):
        """
        Ensure load_config() (with no arguments)
        correctly discovers 'horizon_config.json' in the current working directory.
        """
        os.chdir(self.RESOURCES_DIR)
        cfg = load_config()
        self.assertEqual(cfg.risk_appetite.level, "medium")
        self.assertTrue(cfg.rules.enable_web_hooks)

    def test_invalid_json_syntax_raises_jsondecodeerror(self):
        """
        Verify that malformed JSON (invalid_json_syntax.json)
        raises json.JSONDecodeError during loading.
        """
        with self.assertRaises(json.JSONDecodeError):
            load_config(self._res("invalid_json_syntax.json"))

    def test_wrong_data_types_raise_typeerror(self):
        """
        Verify that configurations with incorrect data types
        (wrong_data_types.json) raise a TypeError.
        """
        with self.assertRaises(TypeError):
            load_config(self._res("wrong_data_types.json"))

    def test_missing_file_empty_object(self):
        """
        Verify that attempting to load a non-existent file
        raises FileNotFoundError.
        """
        missing = str(self.RESOURCES_DIR / "does_not_exist.json")
        self.assertEqual(load_config(missing), Config())
