import pytest
from helixapi.helix import Helix

def test_helix_initialization():
    # Test initialization of Helix class
    helix = Helix() 

    assert helix
    assert helix.bundle
    assert helix.setlists

def test_helix_file_initialization_by_path(bundle_template_path):
    # Test initialization of Helix class
    helix = Helix(file_path=bundle_template_path) 

    assert helix
    assert helix.bundle
    assert helix.setlists  
