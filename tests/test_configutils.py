# third party
import json
import tempfile

import pytest

# package
from packagerbuddy import configutils, settings


def test_load(mock_settings_file_config: None) -> None:
    config = configutils.load()
    assert config == {"foo": r"https://example.com/{version}/foo.zip"}


def test_dump(monkeypatch: pytest.MonkeyPatch) -> None:
    _, tmp_config = tempfile.mkstemp(suffix=".json", prefix="software")
    monkeypatch.setattr(settings, "FILE_CONFIG", tmp_config)

    tmp_data = {"bar": r"https://example.com/{version}/bar.zip"}
    configutils.dump(tmp_data)

    with open(tmp_config, "r") as fp:
        config = json.load(fp)
        assert config == tmp_data


@pytest.mark.parametrize(["software", "configured"], [
    ("foo", True),
    ("bar", False),
])
def test_is_software_configured(
    software: str,
    configured: bool,
    mock_settings_file_config: None,
) -> None:
    config = configutils.load()
    assert configutils.is_software_configured(config, software) is configured


def test_add(fix_tmp_config: str) -> None:
    config = configutils.load()
    configutils.add_software(config, "bar", r"https://example.com/{version}/bar.zip")
    assert config["bar"] == r"https://example.com/{version}/bar.zip"


def test_remove(fix_tmp_config: str) -> None:
    config = configutils.load()
    configutils.add_software(config, "bar", r"https://example.com/{version}/bar.zip")
    assert "bar" in config
    configutils.remove_software(config, "bar")
    assert "bar" not in config
