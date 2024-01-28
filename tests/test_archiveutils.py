# third party
import pytest

# package
from packagerbuddy import archiveutils


def test_build_temporary_install_path(mock_settings_dir_install: None) -> None:
    archiveutils.build_temporary_install_path("foo", "bar") == "/tmp/installed/tmp-foo-bar"


def test_build_install_path(mock_settings_dir_install: None) -> None:
    archiveutils.build_install_path("foo", "bar") == "/tmp/installed/foo-bar"


@pytest.mark.parametrize(
    ["path", "expected_root", "expected_ext"],
    [
        ("/root/dir/file.zip", "/root/dir/file", ".zip"),
        ("/root/dir/file.tar", "/root/dir/file", ".tar"),
        ("/root/dir/file.tar.gz", "/root/dir/file", ".tar.gz"),
        ("/root/dir/file.dot1.dot2.tar.gz", "/root/dir/file.dot1.dot2", ".tar.gz"),
    ],
)
def test_split_ext(path: str, expected_root: str, expected_ext: str) -> None:
    root, ext = archiveutils.split_ext(path)
    assert root == expected_root
    assert ext == expected_ext


def test_get_archive_name():
    config = {"foo": "https://example.com/{version}/original-foo.zip"}
    assert archiveutils.get_archive_name("foo", "bar", config) == "original-foo"
