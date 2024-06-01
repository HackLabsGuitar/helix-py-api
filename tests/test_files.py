import pytest
import os
from helixapi.utils.files import Files, FileType, TemplatePath

def test_files_filetype():
    assert FileType.BUNDLE.value == 'hlb'
    assert FileType.SETLIST.value == 'hls'
    assert FileType.PRESET.value == 'hlx'

def test_files_filetype_get_type():
    assert FileType.get_type('bundle.hlb') == FileType.BUNDLE
    assert FileType.get_type('setlist.hls') == FileType.SETLIST
    assert FileType.get_type('preset.hlx') == FileType.PRESET

def test_files_filetype_get_extension_by_name():
    assert FileType.get_extension_by_name('bundle') == 'hlb'
    assert FileType.get_extension_by_name('setlist') == 'hls'
    assert FileType.get_extension_by_name('preset') == 'hlx'

def test_files_filetype_get_member_by_name():
    assert FileType.get_member_by_name('bundle') == FileType.BUNDLE
    assert FileType.get_member_by_name('setlist') == FileType.SETLIST
    assert FileType.get_member_by_name('preset') == FileType.PRESET

def test_files_filetype_exists_by_name():
    assert FileType.exists_by_name('bundle') == True
    assert FileType.exists_by_name('setlist') == True
    assert FileType.exists_by_name('preset') == True
    assert FileType.exists_by_name('invalid') == False

def test_files_templatepath():
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'helixapi', 'templates', 'bundle.hlb'))
    template_path = TemplatePath.BUNDLE.value
    assert os.path.exists(template_path), f"{template_path} does not exist"

    assert template_path == file_path, f"{template_path} != {file_path}"

def test_files_templatepath_get_by_file_type():
    assert TemplatePath.get_by_file_type(FileType.BUNDLE) == TemplatePath.BUNDLE.value
    assert TemplatePath.get_by_file_type(FileType.SETLIST) == TemplatePath.SETLIST.value
    assert TemplatePath.get_by_file_type(FileType.PRESET) == TemplatePath.PRESET.value

def test_files_templatepath_get_by_file_path():
    assert TemplatePath.get_by_file_path('bundle.hlb') == TemplatePath.BUNDLE.value
    assert TemplatePath.get_by_file_path('setlist.hls') == TemplatePath.SETLIST.value
    assert TemplatePath.get_by_file_path('preset.hlx') == TemplatePath.PRESET.value

def test_files_templatepath_get_by_file_type_name():
    assert TemplatePath.get_by_file_type_name('bundle') == TemplatePath.BUNDLE.value
    assert TemplatePath.get_by_file_type_name('setlist') == TemplatePath.SETLIST.value
    assert TemplatePath.get_by_file_type_name('preset') == TemplatePath.PRESET.value

def test_files_check_existing_file():
    file_path = os.path.join(os.path.dirname(__file__), '..', 'helixapi', 'templates', 'bundle.hlb')
    Files._check_existing_file(file_path)

def test_files_check_existing_file_no_path():
    with pytest.raises(Exception, match="File path not provided"):
        Files._check_existing_file("")

def test_files_check_existing_file_no_file():
    file_path = os.path.join(os.path.dirname(__file__), '..', 'helixapi', 'templates', 'does_not_exist.hlb')
    with pytest.raises(Exception, match="File does not exist"):
        Files._check_existing_file(file_path)