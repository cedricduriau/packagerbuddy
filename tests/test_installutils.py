# stdlib
import os

# third party
import pytest

# package
from packagerbuddy import installutils


def test_build_temporary_install_path(fix_dir_installed: str, mock_settings_dir_install: None):
    path = installutils.build_temporary_install_path("foo", "bar")
    expected = os.path.join(fix_dir_installed, "tmp-foo-bar")
    assert path == expected


def test_build_install_path(fix_dir_installed: str, mock_settings_dir_install: None):
    path = installutils.build_install_path("foo", "bar")
    expected = os.path.join(fix_dir_installed, "foo-bar")
    assert path == expected


def test_get_archive_name():
    software = "foo"
    version = "bar"
    config = {"foo": "https://example.com/{version}/software.zip"}
    name = installutils.get_archive_name(software, version, config)
    assert name == "software"


@pytest.mark.parametrize(
    ["software", "version", "expected"],
    [
        (None, None, 2),
        ("foo", None, 1),
        ("bar", None, 1),
        ("bar", "0.1.0", 1),
        ("foo", "0.1.0", 1),
        ("foo", "0.3.0", 0),
    ],
)
def test_find_installed_software(
    software: str | None,
    version: str | None,
    expected: int,
    mock_settings_dir_install: None,
):
    result = installutils.find_installed_software(software, version)
    assert len(result) == expected
