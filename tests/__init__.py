import pytest

# You can import your test modules here
# For example:
# from tests.test_setlist import TestSetlist
# from tests.test_preset import TestPreset
# from tests.test_snapshot import TestSnapshot

if __name__ == "__main__":
    pytest.main(["-v", "--color=yes", "--cov=api"])
