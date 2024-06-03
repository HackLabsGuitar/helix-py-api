from helixapi.utils.item_base import ItemBase
from .snapshots import Snapshots
from .utils.settings import Settings

class Preset(ItemBase):
    """
    Represents a Helix preset for a given setlist. This contains specific metadata (index, name) and all snapshots.
    """

    def __init__(self, data: dict, setlist_index: int, index: int, set_active_callback=None, metadata: dict = {}):
        """
        Initialize the Preset class.

        Args:
            data (dict): The data structure representing the preset.
            setlist_index (int): Index of the setlist containing this preset.
            index (int): Index of this preset within its setlist.
            set_active_callback (callable): Callback function to set the active preset.
            metadata (dict, optional): Additional metadata for the preset. Defaults to {}.

        Examples:
        ``` py
        preset = Preset(data, setlist_index=0, index=1)
        ```
        """
        super().__init__(cls=Preset, data=data, metadata=metadata, setlist_index=setlist_index, preset_index=index)
        self.index = index
        self._active = False
        self._set_active_callback = set_active_callback

        # set author if not set or if overwrite is enabled
        # setting here allows us to change it later if needed
        settings = Settings()
        author = self.author
        if not author or settings.author_overwrite:
            self.author = settings.author_name

        # Load the snapshots
        self._snapshots = Snapshots(
            data=data, 
            setlist_index=setlist_index, 
            preset_index=self.index,
            get_active_callback=self._get_active_snapshot_index,
            set_active_callback=self._set_active_snapshot_index
        )

    @property
    def _active_snapshot_index(self):
        """
        Get the current snapshot of the preset.

        Returns:
            int: The index of the current snapshot.

        Examples:
        ``` py
        current_snapshot = preset.current_snapshot
        ```
        """
        return self._get_data("current_snapshot")
    
    @_active_snapshot_index.setter
    def _active_snapshot_index(self, index):
        self._set_data("current_snapshot", index)

    def _get_active_snapshot_index(self):
        return self._active_snapshot_index

    def _set_active_snapshot_index(self, index):
        self._active_snapshot_index = index

    @property
    def snapshots(self):
        """
        Get the snapshots of the preset.

        Returns:
            Snapshots: The snapshots of the preset.

        Examples:
        ``` py
        preset.snapshots
        ```
        """
        return self._snapshots

    @property
    def name(self) -> str:
        """
        Get the name of the preset.

        Returns:
            str: The name of the preset.

        Examples:
        ``` py
        preset.name
        ```
        """
        return self._get_data("name")

    @name.setter
    def name(self, value: str) -> None:
        """
        Set the name of the preset.

        Args:
            value (str): The name to set for the preset.

        Raises:
            ValueError: If the name length exceeds the maximum allowed length.

        Examples:
        ``` py
        preset.name = "Preset 1"
        ```
        """
        if len(value) > 16:
            raise ValueError("Name must be 16 characters or fewer.")
        self._set_data("name", value)

    @property
    def author(self) -> str:
        """
        Get the author of the preset.

        Returns:
            str: The author of the preset.

        Examples:
        ``` py
        preset.author
        ```
        """
        return str(self._get_data("author"))

    @author.setter
    def author(self, value: str) -> None:
        """
        Set the author of the preset.

        Args:
            value (str): The author to set for the preset.

        Raises:
            ValueError: If the author length exceeds the maximum allowed length.

        Examples:
        ``` py
        preset.author = "Me"
        ```
        """
        if len(value) > 16:
            raise ValueError("Author must be 16 characters or fewer.")
        self._set_data("author", value)

    @property
    def band(self) -> str:
        """
        Get the band of the preset.

        Returns:
            str: The band of the preset.

        Examples:
        ``` py
        preset.band
        ```
        """
        return self._get_data("band")

    @band.setter
    def band(self, value: str) -> None:
        """
        Set the band of the preset.

        Args:
            value (str): The band to set for the preset.

        Raises:
            ValueError: If the band length exceeds the maximum allowed length.

        Examples:
        ``` py
        preset.band = "My Band"
        ```
        """
        if len(value) > 16:
            raise ValueError("Band must be 16 characters or fewer.")
        self._set_data("band", value)
    @property
    def song(self) -> str:
        """
        Get the song name of the preset.

        Returns:
            str: The song name of the preset.

        Examples:
        ``` py
        preset.song
        ```
        """
        return self._get_data("song")

    @song.setter
    def song(self, value: str) -> None:
        """
        Set the song name of the preset.

        Args:
            value (str): The song name to set for the preset.

        Raises:
            ValueError: If the song name length exceeds the maximum allowed length.

        Examples:
        ``` py
        preset.song = "My Song"
        ```
        """
        if len(value) > 16:
            raise ValueError("Song name must be 16 characters or fewer.")
        self._set_data("song", value)


    def import_preset(self, file_path=None) -> None:
        """
        Import a preset from a file.

        Args:
            file_path (str): Path to the preset file to import.

        Examples:
        ``` py
        preset.import_preset("preset.hlx")
        ```

        Raises:
        Exception: If the file path is not specified or the file type is incorrect.

        Returns:
        None
        """
        self._import_file(file_path=file_path)

    def export_preset(self, file_path=None) -> None:
        """
        Export a preset to a file.

        Args:
            file_path (str): Path to export the preset file to.

        Examples:
        ``` py
        preset.export_preset("preset.hlx")
        ```

        Raises:
        Exception: If the file path is not specified or the file type is incorrect.

        Returns:
        None
        """
        self._export_file(file_path=file_path)

    def reset_preset(self) -> None:
        """
        Reset the preset to its default values.

        Examples:
        ``` py
        preset.reset_preset()
        ```

        Returns:
        None
        """
        self.import_preset()

    @property
    def active(self):
        """
        Get the preset as active.

        Returns:
            bool: True if the preset is active, False otherwise.

        Examples:
        ``` py
        print(preset.active)
        ```
        """
        return self._active

    @active.setter
    def active(self, value):
        """
        Set the preset as active.

        Args:
            value (bool): True to set the preset as active, False otherwise.

        Examples:
        ``` py
        preset.active = True
        ```
        """
        if value and self._set_active_callback:
            self._set_active_callback(self.index)
        self._active = value
