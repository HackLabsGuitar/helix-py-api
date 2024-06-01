import os
import yaml
import logging
import copy
from .files import TemplatePath

class DataManager:
    _mapping_cache = None
    _preset_cache = None

    def __init__(self, cls, data, metadata, setlist_index=None, preset_index=None, snapshot_index=None):
        script_dir = os.path.dirname(__file__)
        if DataManager._mapping_cache is None:
            file_path = os.path.join(script_dir, 'mappings.yaml')
            with open(file_path, 'r') as file:
                DataManager._mapping_cache = yaml.safe_load(file)['data']

        self.mapping = DataManager._mapping_cache
        self.mapping_key = cls.__name__.lower()
        self.setlist_index = setlist_index
        self.preset_index = preset_index
        self.snapshot_index = snapshot_index
        self.data = data
        self.metadata = metadata

    def get_data(self, key):
        path = self.mapping[self.mapping_key][key]
        return self._navigate_path(path)

    def set_data(self, key, value):
        path = self.mapping[self.mapping_key][key]
        self._navigate_path(path, value)

    def _navigate_path(self, path, value=None):
        keys = path.split('.')
        data = self.data

        for i, key in enumerate(keys):
            if key == 'setlist_index':
                key = self.setlist_index
            elif key == 'preset_index':
                key = self.preset_index
                if not data[key]:
                    # If the value is empty and it's a preset, load template data
                    if DataManager._preset_cache is None:
                        file_path = TemplatePath.PRESET.value
                        with open(file_path, 'r') as file:
                            DataManager._preset_cache = yaml.safe_load(file)
                    data[key] = copy.deepcopy(DataManager._preset_cache)
            elif key == 'snapshot_snapshot_index':
                key = f"snapshot{self.snapshot_index}"

            if i == len(keys) - 1:
                if value is not None:
                    data[key] = value
                return data[key]
            else:
                data = data[key]