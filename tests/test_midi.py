import pytest

def test_midi_initialization():
    from helixapi.helix import Helix    

    helix = Helix()
    assert len(helix.midi.system.ports) >= 0, helix.midi.system.ports