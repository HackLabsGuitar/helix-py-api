"""
Module for managing Helix bundle files.
"""

import logging
from .utils.files import Files, FileType, TemplatePath
from .setlists import Setlists

class Bundle:
    """
    Class representing a Helix bundle file.

    This class provides methods to import and export Helix bundle files.

    !!! note

        This class is not intended to be instantiated directly.
        Please access it through an instantiated `Helix` object.
        
        Example:
        ```py
        helix = Helix()
        bundle = helix.bundle
        ```
    """

    def __init__(self, file_path=None, setlists_callback=None):
        """
        Initialize the Bundle class.

        Args:
            file_path (str, optional): Path to the bundle file to load. Defaults to None.

        Examples:
        ``` py
        bundle = Bundle()
        ```

        Returns:
            None
        """
        self._setlists_callback = setlists_callback
        self.import_bundle(file_path)

    @property
    def name(self):
        """
        Get the name of the bundle.

        Returns:
            str: The name of the bundle.
        """
        return self.metadata['meta']['name']

    @name.setter
    def name(self, value):
        """
        Set the name of the bundle.

        Args:
            value (str): The name of the bundle.
        """
        self.data['meta']['name'] = value

    def export_bundle(self, file_path=None):
        """
        Export the bundle to a file.

        Args:
            file_path (str): Path to export the bundle file to.

        Raises:
            Exception: If the file path is not specified or the file type is incorrect.
        """
        logging.debug(f"Exporting bundle: {file_path}")

        if not file_path:
            raise Exception('File path must be specified.')
        elif FileType.get_type(file_path) == FileType.BUNDLE:
            Files._export_file(file_path=file_path, data=self.data, metadata=self.metadata)
        else:
            raise Exception('File type must be a bundle.')

    def import_bundle(self, file_path=None):
        """
        Import the bundle from a file.

        Args:
            file_path (str): Path to the bundle file to import.

        Raises:
            Exception: If the file path is not specified or the file type is incorrect.
        """
        logging.debug(f"Importing bundle: {file_path}")

        if not file_path:
            self.data, self.metadata = Files._import_file(TemplatePath.BUNDLE.value)            
        elif FileType.get_type(file_path) == FileType.BUNDLE:
            self.data, self.metadata = Files._import_file(file_path)
        else:
            raise Exception('File path must be a bundle or None (to load the bundle template).')
        
        # Call the callback to notify Helix to reload setlists
        if self._setlists_callback:
            self._setlists_callback(self.data)