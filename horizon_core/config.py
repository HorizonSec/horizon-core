"""
config.py

This module defines a lightweight configuration loader for user-defined settings.

USAGE:
------
1. Create a JSON file named 'horizon_config.json' in your current working directory.
   Example structure:
   {
     "risk_appetite": {
       "level": "medium",
       "max_investment_per_asset": 5000,
       "stop_loss_threshold": 0.1
     },
     "rules": {
       "enable_email_alerts": true,
       "enable_sms_alerts": false,
       "allow_margin_trading": false
     },
     "opt_in_features": ["daily_summary", "portfolio_rebalancing"]
   }

2. Import and call `load_config()` anywhere in your code:
   from horizon_core.config import load_config

   config = load_config()
   print(config.risk_appetite.level)

3. The loader automatically looks for 'horizon_config.json' in the current directory.
   If not found, it uses defaults defined in the dataclasses below.
"""

import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

# TODO - move these into model directory


@dataclass
class RiskAppetite:
    level: str = "low"  # valid: low, medium, high
    max_investment_per_asset: float = 1000.0
    stop_loss_threshold: float = 0.05


@dataclass
class Rules:
    enable_email_alerts: bool = False
    enable_sms_alerts: bool = False
    enable_web_hooks: bool = False
    allow_margin_trading: bool = False


@dataclass
class Config:
    risk_appetite: RiskAppetite = field(default_factory=RiskAppetite)
    rules: Rules = field(default_factory=Rules)
    opt_in_features: List[str] = field(default_factory=list)


def _load_json(path: str) -> Dict[str, Any]:
    """Loads a JSON file if it exists, otherwise returns an empty dict."""
    if not os.path.exists(path):
        print(f"Warning: Config file not found at {path}")
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_config(config_path: Optional[str] = None) -> Config:
    """
    Loads the user's configuration file from the current directory
    and returns it as a Config object.
    """

    if config_path is None:
        config_path = os.path.join(os.getcwd(), "horizon_config.json")

    user_data = _load_json(config_path)

    # Construct the config object
    risk_appetite = RiskAppetite(**user_data.get("risk_appetite", {}))
    rules = Rules(**user_data.get("rules", {}))
    opt_in_features = user_data.get("opt_in_features", [])

    return Config(risk_appetite=risk_appetite, rules=rules, opt_in_features=opt_in_features)
