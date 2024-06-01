from typing import List
from .utils.collection_base import CollectionBase
from .setlist import Setlist
from .utils.constants import MAX_SETLISTS
from .midi import MIDI

class Setlists(CollectionBase):
    """
    Represents a collection of Helix setlists.
    """
    def __init__(self, data: dict=None):
        self._midi = MIDI()
        
        super().__init__(cls=Setlist, items=[Setlist(data=data, index=i, set_active_callback=self._set_active_setlist) for i in range(MAX_SETLISTS)])
        
        self._set_active_setlist(0)  # Set the first setlist as active initially

        # Ensure the initial active setlist is correctly marked as active
        if self._items:
            self._items[self._active_index].active = True
            
    def _set_active_setlist(self, index):
        self._active_index = index
        self._midi.commands.change_to_setlist(self._active_index)

    @property
    def active_index(self):
        """
        Get the index of the active setlist.

        Returns:
            int: The index of the active setlist.
        """
        return self._active_index

    @active_index.setter
    def active_index(self, index):
        """
        Set the index of the active setlist.

        Args:
            index (int): The index of the setlist to set as active.
        """
        self._set_active_setlist(index)

    @property
    def active_item(self):
        """
        Get the active setlist.
        
        Returns:
            Setlist: The active setlist.
        """
        return self._active_item

    @active_item.setter
    def active_item(self, item):
        """
        Set the active setlist.
        
        Args:
            item (Setlist): The setlist to set as active.
        """
        self._active_item = item
        self._set_active_setlist(item.index)

    def export_setlists(self, file_path=None):
        """
        Export each setlist to individual files.
        
        Args:
            file_path (str): The path to export the setlists to.

        Examples:
        ``` py
        setlists.export_setlists(file_path="/path/to/setlists")
        ```

        Returns:
            None
        """
        self._export_files(file_path)

    def import_setlists(self, file_paths: List[str]):
        """
        Import each setlist from individual files.

        !!! note

            
            Setlist order will follow the order of the provided file_paths (i.e. the first file path will be setlist 1, etc)

        Args:
            file_paths (List[str]): The paths to import the setlists from.

        Examples:
        ``` py
        setlists.import_setlists(file_paths=["/path/to/setlist1", "/path/to/setlist2"])
        ```

        Returns:
            None
        """
        self._import_files(file_paths)