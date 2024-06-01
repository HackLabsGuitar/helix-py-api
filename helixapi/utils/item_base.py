"""Base module for models in the API."""
import logging
from .data_manager import DataManager
from .files import FileType, Files, TemplatePath
from .standards import Standards

class ItemBase:
    def __init__(self, cls, data, metadata, setlist_index=None, preset_index=None, snapshot_index=None):
        self._cls_name = cls.__name__.lower()
        self._data_manager = DataManager(cls=cls, data=data, metadata=metadata, setlist_index=setlist_index, preset_index=preset_index, snapshot_index=snapshot_index)
        self._standards = Standards()

    def _get_data(self, key):
        return self._data_manager.get_data(key)

    def _set_data(self, key, value):
        self._data_manager.set_data(key, value)

    def _export_file(self, file_path=None):
        """
        Export the current item to a file.

        Args:
            file_path (str): Path to export the bundle file to.

        Raises:
            Exception: If the file path is not specified or the file type is incorrect.
        """
        if not FileType.exists_by_name(self._cls_name):
            raise Exception(f'Export is only supported for bundle, setlist, or preset.')

        logging.debug(f"Exporting {self._cls_name}: {file_path}")

        if not file_path:
            raise Exception('File path must be specified.')
        
        Files._export_file(file_path=file_path, data=self._get_data(key='root'), metadata=self._data_manager.metadata)

    def _import_file(self, file_path=None):
        """
        Import an item from a file.

        Args:
            file_path (str): Path to the item file to import.

        Raises:
            Exception: If the file path is not specified or the file type is incorrect.
        """
        if not FileType.exists_by_name(self._cls_name):
            raise Exception(f'Import is only supported for bundle, setlist, or preset.')

        logging.debug(f"Importing {self._cls_name}: {file_path}")

        if not file_path:
            # use template
            data, metadata = Files._import_file(TemplatePath.get_by_file_type_name(self._cls_name))
        else:
            data, metadata = Files._import_file(file_path)

        # Assign the relevant parts of the data and metadata
        if self._cls_name in ['setlist', 'preset']:
            self._set_data('root', data)
        else:
            raise Exception(f'Unsupported file type: {self._cls_name}')

        # Assign metadata
        self._data_manager.metadata = metadata

    def standardize(self):
        """
        Standardize the name of the item based on the loaded standards.

        """
        item_name = self._get_data("name")
        standardized_name = self._standards.apply(item_name, self._cls_name)
        self._set_data("name", standardized_name)