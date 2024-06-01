from .utils.collection_base import CollectionBase
from .snapshot import Snapshot
from .utils.constants import MAX_SNAPSHOTS
from .midi import MIDI

    
class Snapshots(CollectionBase):
    """
    Represents a collection of Helix snapshots for a given preset.
    """
    def __init__(self, data: dict=None, setlist_index: int=None, preset_index: int=None, get_active_callback=None, set_active_callback=None):
        """
        Initialize the Snapshots class.

        Args:
            data (dict): The data structure representing the setlist.
            setlist_index (int): Index of the setlist containing this snapshot.
            preset_index (int): Index of the preset containing this snapshot.
            get_active_callback (callable): Callback function to get the active snapshot index.
            set_active_callback (callable): Callback function to set the active snapshot index.

        Examples:
        ``` py
        setlist = Setlist(data, index=0)
        ```
        """
        self._midi = MIDI()
        super().__init__()
        self._setlist_index = setlist_index
        self._preset_index = preset_index
        self._get_active_callback = get_active_callback
        self._set_active_callback = set_active_callback

        self._items = [
            Snapshot(
                data=data, 
                index=i, 
                setlist_index=setlist_index, 
                preset_index=preset_index, 
                get_active_callback=self._get_active_index,
                set_active_callback=self._set_active_snapshot
            ) 
            for i in range(MAX_SNAPSHOTS)
        ]

    @property
    def active_index(self):
        """
        Get the index of the active snapshot.

        Returns:
            int: The index of the active snapshot.
        """
        return self._get_active_index()

    @active_index.setter
    def active_index(self, index):
        """
        Set the index of the active snapshot.

        Args:
            index (int): The index of the snapshot to set as active.
        """
        self._set_active_index(index)

    @property
    def active_item(self):
        """
        Get the active snapshot.

        Returns:
            Snapshot: The active snapshot.
        """
        return self._items[self.active_index]

    @active_item.setter
    def active_item(self, item):
        """
        Set the active snapshot.

        Args:
            item (Snapshot): The snapshot to set as active.
        """
        self._set_active_index(self._items.index(item))

    def _get_active_index(self):
        """
        Get the index of the active snapshot.

        Returns:
            int: The index of the active snapshot.
        """
        if self._get_active_callback:
            return self._get_active_callback()
        else:
            return 0

    def _set_active_index(self, index):
        """
        Set the index of the active snapshot.

        Args:
            index (int): The index of the snapshot to set as active.
        """
        if self._set_active_callback:
            self._set_active_callback(index)
        
        # Update the active state of snapshots
        for snapshot in self._items:
            snapshot._active = snapshot.index == index

        self._midi.commands.change_to_snapshot(index)

    def _set_active_snapshot(self, index):
        """
        Callback to set the active snapshot.

        Args:
            index (int): The index of the snapshot to set as active.
        """
        self._set_active_index(index)
