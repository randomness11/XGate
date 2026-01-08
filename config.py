"""
Configuration loader and validator for X link moderation bot.
Loads settings from config.yml file.
"""

import os
import yaml
from typing import Dict, Any
from pathlib import Path


class Config:
    """Configuration manager for the bot."""

    def __init__(self, config_path: str = "config.yml"):
        """Load and validate configuration from YAML file."""
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self._validate_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}\n"
                "Please create config.yml from the template."
            )

        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def _validate_config(self):
        """Validate required configuration fields."""
        required_fields = {
            'telegram': ['bot_token'],
            'rules': ['max_links_per_week', 'require_context', 'min_context_length'],
            'messages': ['rate_limit', 'no_context', 'approaching_limit']
        }

        for section, fields in required_fields.items():
            if section not in self.config:
                raise ValueError(f"Missing required section: {section}")

            for field in fields:
                if field not in self.config[section]:
                    raise ValueError(f"Missing required field: {section}.{field}")

        # Validate bot token (allow env variable override)
        bot_token = os.environ.get('TELEGRAM_BOT_TOKEN') or self.config['telegram']['bot_token']
        if bot_token == "YOUR_BOT_TOKEN_HERE" or not bot_token:
            raise ValueError(
                "Please set a valid bot_token in config.yml or TELEGRAM_BOT_TOKEN environment variable\n"
                "Get your bot token from @BotFather on Telegram"
            )

    @property
    def bot_token(self) -> str:
        """Get Telegram bot token (supports env variable override)."""
        return os.environ.get('TELEGRAM_BOT_TOKEN') or self.config['telegram']['bot_token']

    @property
    def max_links_per_week(self) -> int:
        """Get maximum links allowed per week."""
        return int(self.config['rules']['max_links_per_week'])

    @property
    def require_context(self) -> bool:
        """Check if context is required with links."""
        return bool(self.config['rules']['require_context'])

    @property
    def min_context_length(self) -> int:
        """Get minimum context length required."""
        return int(self.config['rules']['min_context_length'])

    @property
    def count_per_link(self) -> bool:
        """Check if each link counts individually."""
        return self.config['rules'].get('count_per_link', True)

    @property
    def rate_limit_message(self) -> str:
        """Get rate limit violation message."""
        return str(self.config['messages']['rate_limit'])

    @property
    def no_context_message(self) -> str:
        """Get no context violation message."""
        return str(self.config['messages']['no_context'])

    @property
    def approaching_limit_message(self) -> str:
        """Get approaching limit warning message."""
        return str(self.config['messages']['approaching_limit'])

    def reload(self):
        """Reload configuration from file."""
        self.config = self._load_config()
        self._validate_config()
