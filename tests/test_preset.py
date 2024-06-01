import pytest
import os
from helixapi.helix import Helix
from helixapi.utils.constants import MAX_PRESETS
from helixapi.utils.standards import Standards

def test_preset_initialization():
    helix = Helix()
    assert len(helix.setlists[0].presets) == MAX_PRESETS


def test_preset_properties():
    # Test properties of Preset class
    helix = Helix()
    preset = helix.setlists[0].presets[0]

    assert preset.index == 0

    preset.name = "Test Preset"
    assert preset.name == "Test Preset"

    preset.tempo = 111
    assert preset.tempo == 111

def test_preset_export(temp_dir):
    # Test export_preset method
    helix = Helix()

    file_path=os.path.join(temp_dir, "exported_preset.hlx")

    assert not os.path.exists(file_path)
    helix.setlists[0].presets[0].export_preset(file_path=file_path)
    assert os.path.exists(file_path)

def test_preset_import(temp_dir, preset_template_path):
    # Test export_preset method
    helix = Helix()

    file_path=os.path.join(temp_dir, "exported_preset.hlx")

    # save old/original name
    old_name = helix.setlists[0].presets[0].name

    # change name
    new_name = "test 1"
    assert old_name != new_name
    helix.setlists[0].presets[0].name = new_name

    # export to later confirm name is changed
    helix.setlists[0].presets[0].export_preset(file_path=file_path)

    # import template and confirm old name
    helix.setlists[0].presets[0].import_preset(file_path=preset_template_path)
    assert helix.setlists[0].presets[0].name == old_name

    # import previous export and confirm new name
    helix.setlists[0].presets[0].import_preset(file_path=file_path)
    assert helix.setlists[0].presets[0].name == new_name

def test_preset_reset():
    # Test reset_preset method
    helix = Helix()

    old_name = helix.setlists[0].presets[0].name
    new_name = "test 1"
    helix.setlists[0].presets[0].name = new_name
    
    helix.setlists[0].presets[0].reset_preset()

    assert helix.setlists[0].presets[0].name == old_name

def test_preset_active():
    helix = Helix()

    # Check initial state
    assert helix.setlists[0].presets[0].active
    assert not helix.setlists[0].presets[1].active

    # test the active property
    helix.setlists[0].presets[1].active = True

    # make sure we didn't affect other presets
    assert not helix.setlists[1].presets[1].active

    # check previous was changed
    assert not helix.setlists[0].presets[0].active

    # check new one is active
    assert helix.setlists[0].presets[1].active

def test_preset_active_index():
    helix = Helix()

    # Check initial state
    assert helix.setlists[0].presets.active_index == 0
    assert not helix.setlists[0].presets.active_index == 1

    # test the active index property
    helix.setlists[0].presets.active_index = 1

    # make sure we didn't affect other presets
    assert not helix.setlists[1].presets.active_index == 1

    # check previous was changed
    assert not helix.setlists[0].presets.active_index == 0

    # check new one is active
    assert helix.setlists[0].presets.active_index == 1

def test_preset_active_item():
    helix = Helix()

    # Check initial state
    assert helix.setlists[0].presets.active_item == helix.setlists[0].presets[0]
    assert not helix.setlists[0].presets.active_item == helix.setlists[0].presets[1]

    # test the active property
    helix.setlists[0].presets.active_item = helix.setlists[0].presets[1]

    # make sure we didn't affect other presets
    assert not helix.setlists[1].presets.active_item == helix.setlists[1].presets[1]

    # check previous was changed
    assert not helix.setlists[0].presets.active_item == helix.setlists[0].presets[0]

    # check new one is active
    assert helix.setlists[0].presets.active_item == helix.setlists[0].presets[1]

def test_preset_snapshot_active(temp_dir, preset_template_path):
    helix = Helix()

    assert helix.setlists[0].presets[0]._active_snapshot_index == 0, "@current_snapshot index should be 0"
    helix.setlists[0].presets[0]._active_snapshot_index = 3
    assert helix.setlists[0].presets[0]._active_snapshot_index == 3, "@current_snapshot index should be 3"

    # export to later confirm index is changed
    file_path=os.path.join(temp_dir, "exported_preset.hlx")
    helix.setlists[0].presets[0].export_preset(file_path=file_path)

    # import template and confirm old index
    helix.setlists[0].presets[0].import_preset(file_path=preset_template_path)
    assert helix.setlists[0].presets[0]._active_snapshot_index == 0, "@current_snapshot index should be 0"

    # import previous export and confirm new name
    helix.setlists[0].presets[0].import_preset(file_path=file_path)
    assert helix.setlists[0].presets[0]._active_snapshot_index == 3, "@current_snapshot index should be 3"


def test_preset_standardize(mock_standards_yaml):

    # test with fixed stanadrds
    _ = Standards()
    Standards._standards_cache = mock_standards_yaml
    
    helix = Helix()

    name = "PreSet 1"
    helix.setlists[0].presets[0].name = name

    assert helix.setlists[0].presets[0].name == name
    assert not helix.setlists[0].presets[0].name.upper() == name
    assert not helix.setlists[0].presets[0].name.lower() == name
    assert not helix.setlists[0].presets[0].name.title() == name
    
    # Test standardize with uppercase casing
    Standards._standards_cache['preset']['casing'] = 'UPPERCASE'
    helix.setlists[0].presets[0].standardize()
    assert helix.setlists[0].presets[0].name == name.upper()

    # Test standardize with lowercase casing
    Standards._standards_cache['preset']['casing'] = 'LOWERCASE'
    helix.setlists[0].presets[0].standardize()
    assert helix.setlists[0].presets[0].name == name.lower()

    # Test standardize with titlecase casing
    Standards._standards_cache['preset']['casing'] = 'TITLECASE'
    helix.setlists[0].presets[0].standardize()
    assert helix.setlists[0].presets[0].name == name.title()

    # Test changing other keys wont affect this one
    Standards._standards_cache['setlist']['casing'] = 'UPPERCASE'
    assert helix.setlists[0].presets[0].name == name.title()

    helix.setlists[0].presets[0].name = "New Preset"
    helix.setlists[0].presets[0].standardize()
    assert helix.setlists[0].presets[0].name == "Preset"
