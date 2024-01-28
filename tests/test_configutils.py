# stdlib
import json

# third party
import pytest

# package
from packagerbuddy import configutils


def test_load(mock_settings_file_config: None) -> None:
    config = configutils.load()
    assert config == {"foo": r"https://example.com/{version}/foo.zip"}


def test_dump(fix_file_config_tmp: str) -> None:
    tmp_data = {"bar": r"https://example.com/{version}/bar.zip"}
    configutils.dump(tmp_data)

    with open(fix_file_config_tmp, "r") as fp:
        config = json.load(fp)
        assert config == tmp_data


@pytest.mark.parametrize(
    ["software", "configured"],
    [
        ("foo", True),
        ("bar", False),
    ],
)
def test_is_software_configured(
    software: str,
    configured: bool,
    mock_settings_file_config: None,
) -> None:
    config = configutils.load()
    assert configutils.is_software_configured(config, software) is configured


def test_add(fix_file_config_tmp: str) -> None:
    config = configutils.load()
    configutils.add_software(config, "bar", r"https://example.com/{version}/bar.zip")
    assert config["bar"] == r"https://example.com/{version}/bar.zip"


def test_remove(fix_file_config_tmp: str) -> None:
    config = configutils.load()
    configutils.add_software(config, "bar", r"https://example.com/{version}/bar.zip")
    assert "bar" in config
    configutils.remove_software(config, "bar")
    assert "bar" not in config
