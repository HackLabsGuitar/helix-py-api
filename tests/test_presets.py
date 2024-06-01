import pytest
from helixapi.helix import Helix
from helixapi.utils.constants import MAX_PRESETS

def test_presets_initialization():
    helix = Helix()
    assert len(helix.setlists[0].presets) == MAX_PRESETS, "presets length should be {}".format(MAX_PRESETS)


def test_presets_swap():
    # Test swap method
    helix = Helix()
    name1 = "preset 1"
    helix.setlists[0].presets[0].name = name1
    name2 = "preset 2"
    helix.setlists[0].presets[1].name = name2
    assert name1 != name2   

    helix.setlists[0].presets.swap(0, 1)
    assert helix.setlists[0].presets[0].name == name2, "Swap failed"
    assert helix.setlists[0].presets[1].name == name1, "Swap failed"

def test_presets_move():
    # Test move method
    helix = Helix()
    name1 = "preset 1"
    helix.setlists[0].presets[0].name = name1
    name2 = "preset 2"
    helix.setlists[0].presets[1].name = name2
    assert name1 != name2    

    helix.setlists[0].presets.move(0, 1)
    assert helix.setlists[0].presets[0].name == name2, "Move failed"
    assert helix.setlists[0].presets[1].name == name1, "Move failed"

def test_presets_active():
    # Test active_setlist property
    helix = Helix()
    assert helix.setlists[0].presets.active_index == 0, "Active preset should be 0"

    helix.setlists[0].presets.active_item = helix.setlists[0].presets[1]
    assert helix.setlists[0].presets.active_index == 1, "Active preset should be 1"

def test_presets_clone():
    # Test clone method
    helix = Helix()

    helix.setlists[0].presets[0].name = "test 1"
    assert helix.setlists[0].presets[0].name != helix.setlists[0].presets[1].name

    helix.setlists[0].presets.clone(0, 1)

    assert helix.setlists[0].presets[0].name == helix.setlists[0].presets[1].name