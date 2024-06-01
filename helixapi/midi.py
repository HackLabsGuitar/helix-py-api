import mido
import os
import yaml
import logging
from typing import List
from helixapi.utils.settings import Settings

class MIDI:
    """
    Manages all MIDI communication and target devices

    * System class - (mostly for internal use) provides methods for interacting with all MIDI output ports and sending messages.
    * Targets class - represents the desired MIDI output ports (aka targets) to use when sending commands.
    * Commands class - provides easy to use (no MIDI knowledge required) methods for sending commands to targets.

    !!! note
        The corresponding commands will automatically be called when the active setlist, preset, or snapshot changes.    
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MIDI, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        """Initialize the MIDI class with settings and devices."""
        if not hasattr(self, '_initialized'):  # Ensure the class is only initialized once
            self.system = self.System()
            self.targets = self.Targets(self.system)
            self.commands = self.Commands(self.targets)
            logging.debug("MIDI initialized with targets: %s", self.targets)
            self._initialized = True

    class System:
        """
        System class for managing MIDI output ports and sending messages.

        !!! note

            While this class is mostly for internal use, it can be used to list MIDI output ports and send messages.
            Most users should use the Commands class instead.
        """
        def __init__(self) -> None:
            self._available_ports = mido.get_output_names()

        @property
        def ports(self) -> List[str]:
            """
            Return a list of available MIDI output ports.

            Returns:
                List[str]: A list of available MIDI output ports.
            """
            logging.debug("Available MIDI ports: %s", self._available_ports)
            return self._available_ports

        def send_cc(self, port: str, channel: int, control: int, value: int) -> None:
            """
            Send a Control Change (CC) message to a MIDI target.

            Args:
                port (str): The name of the MIDI output port.
                channel (int): The MIDI channel to send the message on.
                control (int): The control number.
                value (int): The value to set the control to.
            """
            message = self._create_cc_message(channel, control, value)
            logging.debug("Sending CC message: %s", message)
            self._send_message(port, message)

        def send_pc(self, port: str, channel: int, program: int) -> None:
            """
            Send a Program Change (PC) message to a MIDI target.

            Args:
                port (str): The name of the MIDI output port.
                channel (int): The MIDI channel to send the message on.
                program (int): The program number to change to.
            """
            message = self._create_pc_message(channel, program)
            logging.debug("Sending PC message: %s", message)
            self._send_message(port, message)

        def send_ccpc(self, port: str, cc_channel: int, cc_control: int, cc_value: int, pc_channel: int, pc_program: int) -> None:
            """
            Send both Control Change (CC) and Program Change (PC) messages to a MIDI target.

            Args:
                port (str): The name of the MIDI output port.
                cc_channel (int): The MIDI channel to send the CC message on.
                cc_control (int): The control number for the CC message.
                cc_value (int): The value for the CC message.
                pc_channel (int): The MIDI channel to send the PC message on.
                pc_program (int): The program number for the PC message.
            """
            cc_message = self._create_cc_message(cc_channel, cc_control, cc_value)
            pc_message = self._create_pc_message(pc_channel, pc_program)
            logging.debug("Sending CC message: %s", cc_message)
            logging.debug("Sending PC message: %s", pc_message)
            self._send_message(port, cc_message)
            self._send_message(port, pc_message)

        def _create_cc_message(self, channel: int, control: int, value: int) -> mido.Message:
            """
            Create a Control Change (CC) message.

            Args:
                channel (int): The MIDI channel to send the message on.
                control (int): The control number.
                value (int): The value to set the control to.

            Returns:
                mido.Message: The created CC message.
            """
            return mido.Message('control_change', channel=channel, control=control, value=value)

        def _create_pc_message(self, channel: int, program: int) -> mido.Message:
            """
            Create a Program Change (PC) message.

            Args:
                channel (int): The MIDI channel to send the message on.
                program (int): The program number to change to.

            Returns:
                mido.Message: The created PC message.
            """
            return mido.Message('program_change', channel=channel, program=program)

        def _send_message(self, port: str, message: mido.Message) -> None:
            """
            Send a MIDI message to a specific MIDI target.

            Args:
                port (str): The name of the MIDI output port.
                message (mido.Message): The MIDI message to send.
            """
            with mido.open_output(port) as output:
                output.send(message)
                logging.debug("Sent message: %s to target: %s", message, port)

    class Targets:
        """
        Targets class for managing desired MIDI output ports.

        "Targets" are the MIDI output ports you want commands to be sent to.
        Target names are saved in and loaded from the settings.yaml file.
        """
        def __init__(self, system) -> None:
            self._settings = Settings()
            self._system = system
            self._items = self._load_targets()

        def _load_targets(self) -> List[str]:
            """
            Load targets from settings if they match available ports.

            Returns:
                List[str]: A list of matched MIDI targets.
            """
            saved_targets = self._settings.midi_targets
            logging.debug("Saved MIDI targets: %s", saved_targets)

            matched_targets = []
            for target in saved_targets:
                if target in self._system.ports:
                    matched_targets.append(target)
                else:
                    logging.warning("MIDI target '%s' not matched to any available port.", target)
            return matched_targets

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

        def save(self) -> None:
            """
            Save the current list of MIDI targets to the settings.
            """
            settings_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'settings.yaml'))
            with open(settings_file, 'w') as file:
                yaml.safe_dump(self._items, file)
            logging.debug("MIDI targets saved: %s", self._items)

        def add(self, target_name: str) -> None:
            """
            Add a MIDI target to the list of targets if it is not already present and is available.

            Args:
                target_name (str): The name of the MIDI target to add.
            """
            if target_name in self._system.ports:
                if target_name not in self._items:
                    self._items.append(target_name)
                    self.save()
                    logging.debug("Added MIDI target: %s", target_name)
            else:
                logging.warning("Cannot add MIDI target '%s': not available.", target_name)

        def remove(self, target_name: str) -> None:
            """
            Remove a MIDI target from the list of targets if it is present.

            Args:
                target_name (str): The name of the MIDI target to remove.
            """
            if target_name in self._items:
                self._items.remove(target_name)
                self.save()
                logging.debug("Removed MIDI target: %s", target_name)

    class Commands:
        """
        Commands class for MIDI controllable commands to the Helix device.

        This class eliminates the need to understand MIDI and the specific MIDI messages and order needed to communicate with a Helix device.
        Instead, you simply call the commands you want (ex. change_to_setlist) and the class will take care of the rest.
        """
        def __init__(self, targets) -> None:
            self.targets = targets

        def change_to_setlist(self, setlist_index: int) -> None:
            """
            Change to a specific setlist on the Helix device.

            Args:
                setlist_index (int): The index of the setlist to change to.
            """
            for target in self.targets:
                self.targets.system.send_cc(port=target, channel=0, control=69, value=setlist_index)
                logging.debug("Changed to setlist %d on target %s", setlist_index, target)

        def change_to_preset(self, preset_index: int) -> None:
            """
            Change to a specific preset on the Helix device.

            Args:
                preset_index (int): The index of the preset to change to.
            """
            for target in self.targets:
                self.targets.system.send_pc(port=target, channel=0, program=preset_index)
                logging.debug("Changed to preset %d on target %s", preset_index, target)

        def change_to_snapshot(self, snapshot_index: int) -> None:
            """
            Change to a specific snapshot on the Helix device.

            Args:
                snapshot_index (int): The index of the snapshot to change to.
            """
            for target in self.targets:
                self.targets.system.send_cc(port=target, channel=0, control=69, value=snapshot_index)
                logging.debug("Changed to snapshot %d on target %s", snapshot_index, target)

        def next_preset(self) -> None:
            """
            Change to the next preset on the Helix device.
            """
            for target in self.targets:
                self.targets.system.send_cc(port=target, channel=0, control=72, value=64)
                logging.debug("Changed to next preset on target: %s", target)

        def previous_preset(self) -> None:
            """
            Change to the previous preset on the Helix device.
            """
            for target in self.targets:
                self.targets.system.send_cc(port=target, channel=0, control=72, value=0)
                logging.debug("Changed to previous preset on target: %s", target)

        def next_snapshot(self) -> None:
            """
            Change to the next snapshot on the Helix device.
            """
            for target in self.targets:
                self.targets.system.send_cc(port=target, channel=0, control=69, value=8)
                logging.debug("Changed to next snapshot on target: %s", target)

        def previous_snapshot(self) -> None:
            """
            Change to the previous snapshot on the Helix device.
            """
            for target in self.targets:
                self.targets.system.send_cc(port=target, channel=0, control=69, value=9)
                logging.debug("Changed to previous snapshot on target: %s", target)

        def toggle_toe(self) -> None:
            """
            Toggles the toe switch on the Helix device.
            """
            for device in self.devices:
                self.devices.system.send_cc(port=device, channel=0, control=59, value=0)
                logging.debug("Toggled toe switch on device: %s", device)

        def toggle_tuner(self) -> None:
            """
            Toggles the tuner on the Helix device.
            """
            for device in self.devices:
                self.devices.system.send_cc(port=device, channel=0, control=68, value=0)
                logging.debug("Toggled tuner on device: %s", device)