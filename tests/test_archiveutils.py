# package
from packagerbuddy import installutils


def test_build_temporary_install_path(mock_settings_dir_install: None) -> None:
    installutils.build_temporary_install_path("foo", "bar") == "/tmp/installed/tmp-foo-bar"


def test_build_install_path(mock_settings_dir_install: None) -> None:
    installutils.build_install_path("foo", "bar") == "/tmp/installed/foo-bar"


def test_get_archive_name():
    config = {"foo": "https://example.com/{version}/original-foo.zip"}
    assert installutils.get_archive_name("foo", "bar", config) == "original-foo"
