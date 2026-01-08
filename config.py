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

        # Use defaults if no config file exists (zero-config mode)
        if not self.config_path.exists():
            print("ℹ️  No config.yml found, using default settings")
            self.config = self._get_defaults()
        else:
            self.config = self._load_config()

        self._validate_config()

    def _get_defaults(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            'telegram': {
                'bot_token': os.environ.get('TELEGRAM_BOT_TOKEN', '')
            },
            'rules': {
                'max_links_per_week': 3,
                'require_context': True,
                'min_context_length': 30,
                'count_per_link': True
            },
            'messages': {
                'rate_limit': "⚠️ You've hit your weekly limit ({max} X links per week)",
                'no_context': "⚠️ X links require context (minimum {min} characters)",
                'approaching_limit': "ℹ️ You have {remaining} X link(s) remaining this week"
            }
        }

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)

        # Merge with defaults to handle missing fields
        defaults = self._get_defaults()

        # Merge telegram section
        if 'telegram' not in config:
            config['telegram'] = defaults['telegram']

        # Merge rules section
        if 'rules' not in config:
            config['rules'] = defaults['rules']
        else:
            for key, value in defaults['rules'].items():
                if key not in config['rules']:
                    config['rules'][key] = value

        # Merge messages section
        if 'messages' not in config:
            config['messages'] = defaults['messages']
        else:
            for key, value in defaults['messages'].items():
                if key not in config['messages']:
                    config['messages'][key] = value

        return config

    def _validate_config(self):
        """Validate required configuration fields."""
        # Validate bot token (allow env variable override)
        bot_token = os.environ.get('TELEGRAM_BOT_TOKEN') or self.config['telegram']['bot_token']
        if bot_token == "YOUR_BOT_TOKEN_HERE" or not bot_token:
            raise ValueError(
                "\n❌ Bot token not configured!\n\n"
                "Quick fix:\n"
                "  Option 1: export TELEGRAM_BOT_TOKEN='your_token_here'\n"
                "  Option 2: Run ./setup.sh for interactive setup\n"
                "  Option 3: Edit config.yml and replace YOUR_BOT_TOKEN_HERE\n\n"
                "Get your token from: https://t.me/BotFather\n"
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
