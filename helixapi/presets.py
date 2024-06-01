from typing import List
from .utils.collection_base import CollectionBase
from .preset import Preset
from .utils.constants import MAX_PRESETS
from .midi import MIDI

class Presets(CollectionBase):
    """
    Represents a collection of Helix presets for a given setlist.
    """
    def __init__(self, data: dict=None, setlist_index: int=None):
        """
        Initialize the Presets class.

        Args:
            data (dict): The data structure representing the setlist.
            setlist_index (int): Index of the setlist containing this preset.

        Examples:
        ``` py
        setlist = Setlist(data, index=0)
        ```
        """
        self._midi = MIDI()

        super().__init__(cls=Preset, items=[Preset(data=data, setlist_index=setlist_index, index=i, set_active_callback=self._set_active_preset) for i in range(MAX_PRESETS)])
        
        self._setlist_index = setlist_index
        self._active_index = 0  # Set the first preset as active initially

        # Ensure the initial active preset is correctly marked as active
        if self._items:
            self._items[self._active_index].active = True
            self._set_active_preset(self._active_index)

    def _set_active_preset(self, index):
        self._active_index = index
        self._midi.commands.change_to_preset(index)

    @property
    def active_index(self):
        """
        Get the index of the active preset.

        Returns:
            int: The index of the active preset.
        """
        return self._active_index

    @active_index.setter
    def active_index(self, index):
        """
        Set the index of the active preset.

        Args:
            index (int): The index of the preset to set as active.
        """
        self._set_active_preset(index)

    @property
    def active_item(self):
        """
        Get the active preset.
        
        Returns:
            Preset: The active preset.
        """
        return self._active_item

    @active_item.setter
    def active_item(self, item):
        """
        Set the active preset.
        
        Args:
            item (Preset): The preset to set as active.
        """
        self._active_item = item
        self._set_active_preset(item.index)

    def export_presets(self, file_path=None):
        """
        Export presets to a single file.

        Args:
            file_path (str): The path to the file to export presets to. 
            
        Returns:
            None
        """
        self._export_files(file_path)

    def import_presets(self, file_paths: List[str]):
        """
        Import presets from multiple files.

        
        !!! note

            
            Preset order will follow the order of the provided file_paths (i.e. the first file path will be preset 1, etc)

        Args:
            file_paths (List[str]): List of file paths to import presets from.

        Returns:
            None
        """
        self._import_files(file_paths)