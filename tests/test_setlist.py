import pytest
import os
from helixapi.helix import Helix
from helixapi.utils.standards import Standards

def test_setlist_initialization():
    helix = Helix()

    # Assert that setlists is not empty
    assert len(helix.setlists) > 0, "Setlists should not be empty"

    # Assert that the first item exists and is not None
    assert helix.setlists[0] is not None, "The first item in setlists should exist"

def test_setlist_properties():
    # Test properties of setlist class
    helix = Helix()
    setlist = helix.setlists[0]

    assert setlist.index == 0

    setlist.name = "Test setlist"
    assert setlist.name == "Test setlist", "Should be able to set name"

    setlist.tempo = 111
    assert setlist.tempo == 111, "Should be able to set tempo"

def test_setlist_export(temp_dir):
    # Test export_setlist method
    helix = Helix()

    file_path=os.path.join(temp_dir, "exported_setlist.hls")

    assert not os.path.exists(file_path), "Exported file should not already exist"
    helix.setlists[0].export_setlist(file_path=file_path)
    assert os.path.exists(file_path), "Exported file should exist"

def test_setlist_import(temp_dir, setlist_template_path):
    # Test export_setlist method
    helix = Helix()

    file_path=os.path.join(temp_dir, "exported_setlist.hls")

    # save old/original name
    old_name = helix.setlists[0].name

    # change name
    new_name = "test 1"
    assert old_name != new_name, "Old name should not match new name"
    helix.setlists[0].name = new_name

    # export to later confirm name is changed
    helix.setlists[0].export_setlist(file_path=file_path)

    # import template and confirm old name
    helix.setlists[0].import_setlist(file_path=setlist_template_path)
    assert helix.setlists[0].name == old_name, "Old name should match new name"

    # import previous export and confirm new name
    helix.setlists[0].import_setlist(file_path=file_path)
    assert helix.setlists[0].name == new_name, "New name should match old name"

def test_setlist_reset():
    # Test reset_setlist method
    helix = Helix()

    old_name = helix.setlists[0].name
    new_name = "test 1"
    helix.setlists[0].name = new_name
    
    helix.setlists[0].reset_setlist()

    assert helix.setlists[0].name == old_name

def test_setlist_active():
    helix = Helix()

    assert helix.setlists[0].active
    assert helix.setlists.active_index == 0
    assert helix.setlists.active_item == helix.setlists[0]

    assert not helix.setlists[1].active
    assert not helix.setlists.active_index == 1
    assert not helix.setlists.active_item == helix.setlists[1]

    helix.setlists[1].active = True

    assert not helix.setlists[0].active
    assert not helix.setlists.active_index == 0
    assert not helix.setlists.active_item == helix.setlists[0]

    assert helix.setlists[1].active
    assert helix.setlists.active_index == 1
    assert helix.setlists.active_item == helix.setlists[1]

def test_setlist_standardize(mock_standards_yaml):

    # test with fixed stanadrds
    _ = Standards()
    Standards._standards_cache = mock_standards_yaml
    
    helix = Helix()

    name = "SetList 1"
    helix.setlists[0].name = name

    assert helix.setlists[0].name == name
    assert not helix.setlists[0].name.upper() == name
    assert not helix.setlists[0].name.lower() == name
    assert not helix.setlists[0].name.title() == name
    
    # Test standardize with uppercase casing
    Standards._standards_cache['setlist']['casing'] = 'UPPERCASE'
    helix.setlists[0].standardize()
    assert helix.setlists[0].name == name.upper()

    # Test standardize with lowercase casing
    Standards._standards_cache['setlist']['casing'] = 'LOWERCASE'
    helix.setlists[0].standardize()
    assert helix.setlists[0].name == name.lower()

    # Test standardize with titlecase casing
    Standards._standards_cache['setlist']['casing'] = 'TITLECASE'
    helix.setlists[0].standardize()
    assert helix.setlists[0].name == name.title()

    # Test changing other keys wont affect this one
    Standards._standards_cache['preset']['casing'] = 'UPPERCASE'
    assert helix.setlists[0].name == name.title()