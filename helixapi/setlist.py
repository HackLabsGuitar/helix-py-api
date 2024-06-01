from helixapi.utils.item_base import ItemBase
from helixapi.presets import Presets

class Setlist(ItemBase):
    def __init__(self, data: dict, index: int, set_active_callback=None, metadata: dict = {}):
        super().__init__(cls=Setlist, data=data, metadata=metadata, setlist_index=index)
        self.index = index
        self._active = False
        self._set_active_callback = set_active_callback
        self._presets = Presets(data=data, setlist_index=index)
        
    @property
    def presets(self):
        """
        Get the presets for this setlist.

        Returns:
            Presets: The presets for this setlist.
        """
        return self._presets

    @property
    def name(self) -> str:
        """
        Get the name of the setlist.

        Returns:
            str: The name of the setlist.
        """
        return self._get_data("name")

    @name.setter
    def name(self, value: str) -> None:
        """
        Set the name of the setlist.
        
        Args:
            value (str): The name to set for the setlist.
        
        Raises:
            ValueError: If the name length exceeds the maximum allowed length.
        """
        if len(value) > 16:
            raise ValueError("Name must be 16 characters or fewer.")
        self._set_data("name", value)

    def import_setlist(self, file_path=None):
        """
        Import a setlist from a file.

        Args:
            file_path (str, optional): The path to the file to import. Defaults to None.

        Raises:
            Exception: If the file path is not specified or the file type is incorrect.
        """
        self._import_file(file_path=file_path)

    def export_setlist(self, file_path=None):
        """
        Export a setlist to a file.

        Args:
            file_path (str, optional): The path to the file to export. Defaults to None.

        Raises:
            Exception: If the file path is not specified or the file type is incorrect.
        """
        self._export_file(file_path=file_path)

    def reset_setlist(self):
        """
        Reset the setlist to its default state.
        """
        self.import_setlist()
        self.name = f"SETLIST {self.index + 1}"

    @property
    def active(self):
        """
        Get the active state of the setlist.
        
        Returns:
            bool: True if the setlist is active, False otherwise.
        """
        return self._active

    @active.setter
    def active(self, value):
        """
        Set the active state of the setlist.
        
        Args:
            value (bool): True to set the setlist as active, False otherwise.
        """
        if value and self._set_active_callback:
            self._set_active_callback(self.index)
        self._active = value
