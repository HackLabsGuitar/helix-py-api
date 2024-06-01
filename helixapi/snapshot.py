from helixapi.utils.item_base import ItemBase
from enum import Enum

class LEDColor(Enum):
    """Available LED colors for Helix snapshots."""
    AUTO = 0
    WHITE = 1
    RED = 2
    DARK_ORANGE = 3
    LIGHT_ORANGE = 4
    YELLOW = 5
    GREEN = 6
    TURQUOISE = 7
    BLUE = 8
    VIOLET = 9
    PINK = 10
    OFF = 11

class Snapshot(ItemBase):
    """
    Represents a Helix snapshot for a given preset. This contains specific metadata (index, name).
    """

    def __init__(self, data: dict, setlist_index: int, preset_index: int, index: int, get_active_callback=None, set_active_callback=None, metadata: dict = {}) -> None:
        """
        Initialize the Snapshot class.

        Args:
            data (dict): The data structure representing the snapshot.
            setlist_index (int): Index of the setlist containing this snapshot.
            preset_index (int): Index of the preset containing this snapshot.
            index (int): Index of this snapshot within its preset.
            get_active_callback (callable): Callback function to get the active snapshot.
            set_active_callback (callable): Callback function to set the active snapshot.
            metadata (dict, optional): Additional metadata for the snapshot. Defaults to {}.

        Examples:
        ``` py
        snapshot = Snapshot(data, setlist_index=0, preset_index=1, index=2)
        ```
        """
        super().__init__(cls=Snapshot, data=data, metadata=metadata, setlist_index=setlist_index, preset_index=preset_index, snapshot_index=index)
        self.index = index
        self._get_active_callback = get_active_callback
        self._set_active_callback = set_active_callback

    @property
    def name(self) -> str:
        """
        Get the name of the snapshot.

        Returns:
            str: The name of the snapshot.

        Examples:
        ``` py
        snapshot.name
        ```
        """
        return self._get_data("name")

    @name.setter
    def name(self, value: str) -> None:
        """
        Set the name of the snapshot.

        Args:
            value (str): The name to set for the snapshot.

        Raises:
            ValueError: If the name length exceeds the maximum allowed length.

        Examples:
        ``` py
        snapshot.name = "Clean Tone"
        ```
        """
        if len(value) > 16:
            raise ValueError("Name must be 16 characters or fewer.")
        self._set_data("name", value)

    @property
    def ledcolor(self) -> LEDColor:
        """
        Get the LED color of the snapshot.

        Returns:
            LEDColor: The LED color of the snapshot.

        Examples:
        ``` py
        prnit(snapshot.ledcolor)
        ```
        """
        return self._get_data("ledcolor")

    @ledcolor.setter
    def ledcolor(self, value: LEDColor) -> None:
        """
        Set the LED color of the snapshot.

        Args:
            value (LEDColor): The LED color to set for the snapshot.

        Raises:
            ValueError: If the value is not a valid LEDColor enum.

        Examples:
        ``` py
        snapshot.ledcolor = LEDColor.RED
        ```
        """
        if not isinstance(value, LEDColor):
            raise ValueError("Invalid LED color value.")
        self._set_data("ledcolor", value)

    @property
    def active(self) -> bool:
        """
        Check if the snapshot is active.

        Returns:
            bool: True if the snapshot is active, False otherwise.
        """
        if self._get_active_callback:
            return self._get_active_callback() == self.index
        return False

    @active.setter
    def active(self, value: bool) -> None:
        """
        Set the snapshot as active.

        Args:
            value (bool): True to set the snapshot as active, False otherwise.
        """
        if value and self._set_active_callback:
            self._set_active_callback(self.index)
