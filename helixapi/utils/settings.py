"""
Settings module for loading configuration settings from settings.yaml.
"""
import os
import yaml
import logging
from typing import Dict, Any

DEFAULT_LOG_LEVEL = logging.INFO

class Settings:
    """Class for managing configuration settings."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Settings, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        settings_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'settings.yaml'))
        if not hasattr(self, 'initialized'):
            self.settings = self._load_settings(settings_file)
            self.initialized = True

    def _load_settings(self, settings_file: str) -> Dict[str, Any]:
        """
        Load settings from the specified YAML file.

        Args:
            settings_file (str): Path to the settings file.

        Returns:
            dict: Dictionary containing the loaded settings.
        """
        with open(settings_file, 'r') as file:
            return yaml.safe_load(file)

    @property
    def log_level(self) -> int:
        """
        Get the logging level from the settings.

        Returns:
            int: The logging level.
        """
        return self.settings.get("log_level", DEFAULT_LOG_LEVEL)
    
    @property
    def author_name(self) -> str:
        """
        Get the author name from the settings.

        The value here will be written in the preset. This is typically only used at the CustomTone website.

        Returns:
            str: The author name.
        """
        name  = self.settings.get("author", {}).get("name", "")
        if not isinstance(name, str):
            return ""
        return name


    @property
    def author_overwrite(self) -> bool:
        """
        Get the author overwrite setting from the settings.

        when true, this will overwrite existing author names in the preset.
        When false, the author name will only be written if it is not already set.

        Returns:
            bool: True if the author name should be overwritten, False otherwise.
        """
        value = self.settings.get("author", {}).get("overwrite", False)
        if not isinstance(value, bool):
            return False
        return value

    @property
    def midi_targets(self) -> list:
        """
        Get the midi target port names from the settings.

        Returns:
            list: A list of midi target port names.
        """
        return self.settings.get("midi", {}).get("targets", [])

    @property
    def standards(self) -> dict:
        """
        Get the standards settings from the settings.

        Returns:
            dict: A dictionary of standards settings.
        """
        return self.settings.get("standards", {})
