import pytest
import os
from helixapi.helix import Helix
from helixapi.utils.constants import MAX_SNAPSHOTS
from helixapi.snapshot import LEDColor
from helixapi.utils.standards import Standards

def test_snapshot_initialization():
    helix = Helix()
    assert len(helix.setlists[0].presets[0].snapshots) == MAX_SNAPSHOTS


def test_snapshot_properties():
    # Test properties of snapshot class
    helix = Helix()
    snapshot = helix.setlists[0].presets[0].snapshots[0]

    assert snapshot.index == 0

    snapshot.name = "Test snapshot"
    assert snapshot.name == "Test snapshot"

    snapshot.ledcolor = LEDColor.RED
    assert snapshot.ledcolor == LEDColor.RED

def test_snapshot_active():
    helix = Helix()

    assert helix.setlists[0].presets[0].snapshots[0].active
    assert helix.setlists[0].presets[0].snapshots.active_index == 0
    assert helix.setlists[0].presets[0].snapshots.active_item == helix.setlists[0].presets[0].snapshots[0]

    assert not helix.setlists[0].presets[0].snapshots[1].active
    assert not helix.setlists[0].presets[0].snapshots.active_index == 1
    assert not helix.setlists[0].presets[0].snapshots.active_item == helix.setlists[0].presets[0].snapshots[1]

    helix.setlists[0].presets[0].snapshots[1].active = True

    assert not helix.setlists[0].presets[0].snapshots[0].active
    assert not helix.setlists[0].presets[0].snapshots.active_index == 0
    assert not helix.setlists[0].presets[0].snapshots.active_item == helix.setlists[0].presets[0].snapshots[0]

    assert helix.setlists[0].presets[0].snapshots[1].active
    assert helix.setlists[0].presets[0].snapshots.active_index == 1
    assert helix.setlists[0].presets[0].snapshots.active_item == helix.setlists[0].presets[0].snapshots[1]

def test_preset_standardize(mock_standards_yaml):

    # test with fixed stanadrds
    _ = Standards()
    Standards._standards_cache = mock_standards_yaml
    
    helix = Helix()

    name = "SnapShot 1"
    helix.setlists[0].presets[0].snapshots[0].name = name

    assert helix.setlists[0].presets[0].snapshots[0].name == name
    assert not helix.setlists[0].presets[0].snapshots[0].name.upper() == name
    assert not helix.setlists[0].presets[0].snapshots[0].name.lower() == name
    assert not helix.setlists[0].presets[0].snapshots[0].name.title() == name
    
    # Test standardize with uppercase casing
    Standards._standards_cache['snapshot']['casing'] = 'UPPERCASE'
    helix.setlists[0].presets[0].snapshots[0].standardize()
    assert helix.setlists[0].presets[0].snapshots[0].name == name.upper()

    # Test standardize with lowercase casing
    Standards._standards_cache['snapshot']['casing'] = 'LOWERCASE'
    helix.setlists[0].presets[0].snapshots[0].standardize()
    assert helix.setlists[0].presets[0].snapshots[0].name == name.lower()

    # Test standardize with titlecase casing
    Standards._standards_cache['snapshot']['casing'] = 'TITLECASE'
    helix.setlists[0].presets[0].snapshots[0].standardize()
    assert helix.setlists[0].presets[0].snapshots[0].name == name.title()

    # Test changing other keys wont affect this one
    Standards._standards_cache['snapshot']['casing'] = 'UPPERCASE'
    assert helix.setlists[0].presets[0].snapshots[0].name == name.title()

    helix.setlists[0].presets[0].snapshots[0].name = "Lead"
    helix.setlists[0].presets[0].snapshots[0].standardize()
    assert helix.setlists[0].presets[0].snapshots[0].name == "SOLO"