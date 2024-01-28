# stdlib
import json
import os
import tempfile

# third party
import pytest

# package
from packagerbuddy import settings


# ==============================================================================
# fixtures
# ==============================================================================
@pytest.fixture
def fix_test_data() -> str:
    path = os.path.join(os.path.dirname(__file__), "data")
    return path


@pytest.fixture
def fix_dir_config(fix_test_data: str) -> str:
    path = os.path.join(fix_test_data, "config")
    return path


@pytest.fixture
def fix_file_config(fix_dir_config: str) -> str:
    path = os.path.join(fix_dir_config, "software.json")
    return path


@pytest.fixture
def fix_dir_downloaded(fix_test_data: str):
    path = os.path.join(fix_test_data, "downloaded")
    return path


@pytest.fixture
def fix_dir_installed(fix_test_data: str):
    path = os.path.join(fix_test_data, "installed")
    return path


@pytest.fixture
def fix_file_config_tmp(monkeypatch: pytest.MonkeyPatch) -> None:
    _, tmp_config = tempfile.mkstemp(suffix=".json", prefix="software")
    monkeypatch.setattr(settings, "FILE_CONFIG", tmp_config)

    with open(tmp_config, "w") as fp:
        json.dump({}, fp)

    return tmp_config


# ==============================================================================
# patches
# ==============================================================================
@pytest.fixture
def mock_settings_file_config(fix_file_config: str, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "FILE_CONFIG", fix_file_config)


@pytest.fixture
def mock_settings_dir_downloaded(fix_dir_downloaded: str, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "DIR_DOWNLOAD", fix_dir_downloaded)


@pytest.fixture
def mock_settings_dir_install(fix_dir_installed: str, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "DIR_INSTALL", fix_dir_installed)
