import pytest
import os
from helixapi.bundle import Bundle
from helixapi.helix import Helix

def test_bundle_initialization(bundle_template_path):
    # Test initialization of Bundle class
    helix = Helix(file_path=bundle_template_path)
    assert helix.bundle

def test_bundle_name(bundle_template_path):
    # Test name property
    helix = Helix(file_path=bundle_template_path)
    assert helix.bundle.name.startswith("HX Edit Bundle")

def test_bundle_export(temp_dir):
    # Test export_bundle method
    helix = Helix()

    file_path=os.path.join(temp_dir, "exported_bundle.hlb")

    assert not os.path.exists(file_path)
    helix.bundle.export_bundle(file_path=file_path)
    assert os.path.exists(file_path)

def test_bundle_import(temp_dir, bundle_template_path):
    # Test export_bundle method
    helix = Helix()

    file_path=os.path.join(temp_dir, "exported_bundle.hlb")

    # save old/original name
    old_name = helix.setlists[0].name

    # change name
    new_name = "test 1"
    assert old_name != new_name
    helix.setlists[0].name = new_name

    # export to later confirm name is changed
    helix.bundle.export_bundle(file_path=file_path)

    # import template and confirm old name
    helix.bundle.import_bundle(file_path=bundle_template_path)
    assert helix.setlists[0].name == old_name

    # import previous export and confirm new name
    helix.bundle.import_bundle(file_path=file_path)
    assert helix.setlists[0].name == new_name
