import pytest
from helixapi.helix import Helix
from helixapi.utils.constants import MAX_SNAPSHOTS

def test_snapshots_initialization():
    helix = Helix()
    assert len(helix.setlists[0].presets[0].snapshots) == MAX_SNAPSHOTS, "snapshots length should be {}".format(MAX_SNAPSHOTS)


def test_snapshots_swap():
    # Test swap method
    helix = Helix()
    name1 = helix.setlists[0].presets[0].snapshots[0].name
    name2 = helix.setlists[0].presets[0].snapshots[1].name
    assert name1 != name2   

    helix.setlists[0].presets[0].snapshots.swap(0, 1)
    assert helix.setlists[0].presets[0].snapshots[0].name == name2, "Swap failed"
    assert helix.setlists[0].presets[0].snapshots[1].name == name1, "Swap failed"

def test_snapshots_move():
    # Test move method
    helix = Helix()
    name1 = helix.setlists[0].presets[0].snapshots[0].name
    name2 = helix.setlists[0].presets[0].snapshots[1].name
    assert name1 != name2   

    helix.setlists[0].presets[0].snapshots.move(0, 1)
    assert helix.setlists[0].presets[0].snapshots[0].name == name2, "Move failed"
    assert helix.setlists[0].presets[0].snapshots[1].name == name1, "Move failed"

def test_snapshots_active():
    # Test active_setlist property
    helix = Helix()
    assert helix.setlists[0].presets[0].snapshots.active_index == 0, "Active setlist should be 0"

    helix.setlists[0].presets[0].snapshots.active_item = helix.setlists[0].presets[0].snapshots[1]
    assert helix.setlists[0].presets[0].snapshots.active_index == 1, "Active setlist should be 1"

def test_snapshots_clone():
    # Test clone method
    helix = Helix()

    helix.setlists[0].presets[0].snapshots[0].name = "test 1"
    assert helix.setlists[0].presets[0].snapshots[0].name != helix.setlists[0].presets[0].snapshots[1].name

    helix.setlists[0].presets[0].snapshots.clone(0, 1)

    assert helix.setlists[0].presets[0].snapshots[0].name == helix.setlists[0].presets[0].snapshots[1].name