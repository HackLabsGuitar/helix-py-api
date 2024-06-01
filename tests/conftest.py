import os
import pytest
import yaml


@pytest.fixture(scope="session")
def temp_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("temp")

@pytest.fixture(scope="module")
def template_dir():
    """Fixture to provide the path to the template directory."""
    return os.path.join(os.path.dirname(__file__), "../helixapi/templates")

@pytest.fixture(scope="module")
def bundle_template_path():
    """Fixture to provide the path to bundle template."""
    return os.path.join(os.path.dirname(__file__), "../helixapi/templates/bundle.hlb")

@pytest.fixture(scope="module")
def setlist_template_path():
    """Fixture to provide the path to the setlist template."""
    return os.path.join(os.path.dirname(__file__), "../helixapi/templates/setlist.hls")

@pytest.fixture(scope="module")
def preset_template_path():
    """Fixture to provide the path to the preset template."""
    return os.path.join(os.path.dirname(__file__), "../helixapi/templates/preset.hlx")

def read_template_file(template_dir, file_name):
    """Utility function to read and parse the contents of a template file."""
    file_path = os.path.join(template_dir, file_name)
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="module")
def bundle_template_data(template_dir):
    """Fixture to provide the data from the bundle template file."""
    return read_template_file(template_dir, "bundle.hlb")

@pytest.fixture(scope="module")
def setlist_template_data(template_dir):
    """Fixture to provide the data from the setlist template file."""
    return read_template_file(template_dir, "setlist.hls")

@pytest.fixture(scope="module")
def preset_template_data(template_dir):
    """Fixture to provide the data from the preset template file."""
    return read_template_file(template_dir, "preset.hlx")

@pytest.fixture(scope="module")
def bundle_template_path(template_dir):
    """Fixture to provide the path to the bundle template file."""
    return os.path.join(template_dir, "bundle.hlb")

@pytest.fixture(scope="module")
def setlist_template_path(template_dir):
    """Fixture to provide the path to the setlist template file."""
    return os.path.join(template_dir, "setlist.hls")

@pytest.fixture(scope="module")
def preset_template_path(template_dir):
    """Fixture to provide the path to the preset template file."""
    return os.path.join(template_dir, "preset.hlx")

@pytest.fixture
def mock_standards_yaml():
    standards_yaml_content = """
    setlist:
      casing: UPPERCASE
      replacements:
        " ":
          - "_"
        
    preset:
      casing: UPPERCASE
      replacements:
        " ":
          - "_"
        "Preset":
          - "New Preset"

    snapshot:
      casing: UPPERCASE
      replacements:
        " ":
          - "_"
        "Solo":
          - "lead"
    """
    return yaml.safe_load(standards_yaml_content)