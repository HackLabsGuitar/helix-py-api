import logging
import re
from .settings import Settings

class Standards:
    _standards_cache = None

    def __init__(self) -> None:
        if Standards._standards_cache is None:
            settings = Settings()
            Standards._standards_cache = settings.standards
            logging.debug("Loaded standards: %s", Standards._standards_cache)

    def apply(self, item_name: str, item_type: str) -> str:
        """
        Apply standardization rules to an item name based on its type.

        Args:
            item_name (str): The name of the item to standardize.
            item_type (str): The type of the item.

        Returns:
            str: The standardized item name.

        Example:
            standards = Standards()
            new_name = standards.apply("Preset 1", "preset")
            print(new_name)
        """
        standards = Standards._standards_cache.get(item_type, {})
        casing = standards.get('casing', '').lower()
        replacements = standards.get('replacements', {})

        # Apply replacements
        for replace_key, replace_values in replacements.items():
            for replace_value in replace_values:
                item_name = re.sub(replace_value, replace_key, item_name, flags=re.IGNORECASE)

        # Apply casing
        if casing == 'uppercase':
            item_name = item_name.upper()
        elif casing == 'lowercase':
            item_name = item_name.lower()
        elif casing == 'titlecase':
            item_name = item_name.title()

        logging.debug("Standardized item name: %s", item_name)
        return item_name
