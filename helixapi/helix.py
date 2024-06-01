import logging
import colorlog

from .bundle import Bundle
from .setlists import Setlists
from .utils.settings import Settings
from .midi import MIDI

class Helix:
    """
    Main entry point for interacting with Helix files and devices.

    This class provides methods for loading Helix bundle files and managing setlists.
    """

    def __init__(self, file_path=None) -> None:
        """
        Initialize the Helix class.

        Args:
            file_path (str, optional): Path to the bundle file to load. Defaults to None.

        Examples:
        ``` py
        helix = Helix()
        ```

        Returns:
            None
        """
        # Load settings
        self._settings = Settings()

        # Setup logging
        self._setup_logging(log_level=self._settings.log_level)

        self.midi = MIDI()

        # Initialize _setlists to None
        self._setlists = None

        # Load the bundle (which also loads the setlist, presets, snapshots, etc)
        self._bundle = Bundle(file_path=file_path, setlists_callback=self._reload_setlists)

    def _reload_setlists(self, bundle_data) -> None:
        """
        Reload the setlists with new bundle data.

        Args:
            bundle_data (dict): The new bundle data.

        Returns:
            None
        """
        self._setlists = Setlists(data=bundle_data)

    @property
    def setlists(self) -> Setlists:
        """
        Get the setlists for the current bundle.

        Returns:
            Setlists: The setlists for the current bundle.

        Examples:
        ``` py
        helix.setlists
        ```
        """
        return self._setlists
    
    @setlists.setter
    def setlists(self, value) -> None:
        """
        Set the setlists for the current bundle.

        Args:
            value (Setlists): The setlists to set.

        Returns:
            None
        """
        self._setlists = value
    
    @property
    def bundle(self):
        """
        Get the loaded bundle.

        Returns:
            Bundle: The loaded bundle.

        Examples:
        ``` py
        helix.bundle
        ```
        """
        return self._bundle

    def _setup_logging(self, log_level):
        """
        Set up logging for the API.

        Args:
            log_level (str): The logging level.

        Returns:
            None

        Examples:
        ``` py
        helix._setup_logging(log_level='DEBUG')
        ```
        """
        logger = logging.getLogger()
        logger.setLevel(log_level.upper() if isinstance(log_level, str) else log_level)

        # Clear all existing handlers
        logger.handlers = []

        # Create a console handler and set the level
        console_handler = colorlog.StreamHandler()
        console_handler.setLevel(log_level.upper() if isinstance(log_level, str) else log_level)

        # Define a color formatter
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )
        console_handler.setFormatter(formatter)

        # Add the console handler to the logger
        logger.addHandler(console_handler)

        logging.debug("Logging initialized")
