import pytest
from helixapi.helix import Helix
from helixapi.utils.constants import MAX_SETLISTS

def test_setlists_initialization():
    helix = Helix()
    assert len(helix.setlists) == MAX_SETLISTS, "Setlists length should be {}".format(MAX_SETLISTS)


def test_setlists_swap():
    # Test swap method
    helix = Helix()
    name1 = helix.setlists[0].name
    name2 = helix.setlists[1].name
    assert name1 != name2   

    helix.setlists.swap(0, 1)
    assert helix.setlists[0].name == name2, "Swap failed"
    assert helix.setlists[1].name == name1, "Swap failed"

def test_setlists_move():
    # Test move method
    helix = Helix()
    name1 = helix.setlists[0].name
    name2 = helix.setlists[1].name
    assert name1 != name2   

    helix.setlists.move(0, 1)
    assert helix.setlists[0].name == name2, "Move failed"
    assert helix.setlists[1].name == name1, "Move failed"

def test_setlists_active():
    # Test active_setlist property
    helix = Helix()
    assert helix.setlists.active_index == 0, "Active setlist should be 0"

    helix.setlists.active_item = helix.setlists[1]
    assert helix.setlists.active_index == 1, "Active setlist should be 1"

def test_setlists_clone():
    # Test clone method
    helix = Helix()

    helix.setlists[0].name = "test 1"
    assert helix.setlists[0].name != helix.setlists[1].name

    helix.setlists.clone(0, 1)

    assert helix.setlists[0].name == helix.setlists[1].name
