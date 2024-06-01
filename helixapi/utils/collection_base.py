import logging
import copy
import os
from .files import Files, FileType
from .constants import MAX_SETLISTS, MAX_PRESETS

class CollectionBase:
    def _export_files(self, file_path, generic_names=False):
        if not FileType.get_member_by_name(self._cls_name) in [FileType.SETLIST, FileType.PRESET]:
            raise Exception(f'Export is only supported setlist or preset.')
        
        filetype = FileType.get_member_by_name(self._cls_name).name.lower()
        fileextension = FileType.get_member_by_name(self._cls_name).value.lower()

        for index, item in enumerate(self._items):
            if generic_names:
                export_path = os.path.abspath(os.path.join(file_path, f"{filetype}_{index}.{fileextension}"))
            else:       
                export_path = Files._get_unique_filename(os.path.abspath(os.path.join(file_path, f"{item.name}.{fileextension}")))
            item._export_file(export_path)
    
    def _import_files(self, file_paths):
        if not FileType.get_member_by_name(self._cls_name) in [FileType.SETLIST, FileType.PRESET]:
            raise Exception(f'Import is only supported setlist or preset.')

        max_items = MAX_SETLISTS if self._cls_name == 'setlist' else MAX_PRESETS
        if len(file_paths) > max_items:
            raise Exception(f"Number of items to import exceeds maximum ({max_items})")

        for index, item in enumerate(self._items):
            if index >= len(file_paths):
                break
            item._import_file(file_paths[index])

    def __init__(self, cls=None, items=None):
        self._items = items if items else []
        self.__active_index = 0

        # set class name to blank if cls is None
        if cls is None:
            self._cls_name = ''
        else:
            self._cls_name = cls.__name__.lower()

    def __getitem__(self, index):
        return self._items[index]

    def __setitem__(self, index, value):
        self._items[index] = value

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __contains__(self, item):
        return item in self._items

    def swap(self, index1, index2):
        """
        Swap the items at the two specified indices.

        Args:
            index1 (int): The first index.
            index2 (int): The second index.

        Examples:
        ``` py
        helix.setlists.swap(1, 2)
        ```

        Returns:
            None
        """
        self._items[index1], self._items[index2] = self._items[index2], self._items[index1]

    def move(self, from_index, to_index):
        """
        Move the item from one index to another, shifting other items as needed.

        Args:
            from_index (int): The index of the item to move.
            to_index (int): The index where the item should be moved.

        Examples:
        ``` py
        helix.setlists.move(1, 2)
        ```

        Returns:
            None
        """
        item = self._items.pop(from_index)
        self._items.insert(to_index, item)

    def clone(self, source_index, target_index):
        """
        Clone an item from the source index and overwrite the item at the target index.

        Args:
            source_index (int): The index of the item to clone.
            target_index (int): The index where the cloned item should be stored.

        Examples:
        ``` py
        helix.setlists.clone(1, 2)
        ```

        Returns:
            None
        """
        # Make sure source_index and target_index are valid
        if not (0 <= source_index < len(self._items)):
            raise IndexError("Source index out of range")
        if not (0 <= target_index < len(self._items)):
            raise IndexError("Target index out of range")

        # Deep copy the source item and overwrite the target item
        self._items[target_index] = copy.deepcopy(self._items[source_index])

    @property
    def _active_index(self):
        return self.__active_index

    @_active_index.setter
    def _active_index(self, index):
        if self.__active_index != index:
            if 0 <= self.__active_index < len(self._items):
                # Deactivate the previous active item
                self._items[self.__active_index].active = False
            self.__active_index = index
            if 0 <= self.__active_index < len(self._items):
                # Activate the new active item
                self._items[self.__active_index].active = True

    @property
    def _active_item(self):
        return self._items[self.__active_index]

    @_active_item.setter
    def _active_item(self, item):
        if item in self._items:
            self._active_index = self._items.index(item)
