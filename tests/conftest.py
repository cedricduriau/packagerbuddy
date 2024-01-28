# third party
import pytest

# package
from packagerbuddy import settings


@pytest.fixture
def mock_settings_dir_install(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "DIR_INSTALL", "/tmp/installed")
