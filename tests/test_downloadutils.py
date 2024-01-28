# stdlib
import os

# third party
import pytest

# package
from packagerbuddy import downloadutils


def test_build_archive_path(fix_dir_downloaded: str, mock_settings_dir_downloaded: None) -> None:
    path = downloadutils.build_archive_path("foo", "bar", r"https://example.com/{version}/foo-bar.zip")
    assert path == os.path.join(fix_dir_downloaded, "foo-bar.zip")


@pytest.mark.parametrize(["software", "version", "found"], [
    ("foo", "0.1.0", True),
    ("foo", "0.3.0", False),
])
def test_find_archive(software: str, version: str, found: bool, mock_settings_dir_downloaded: None):
    archive = downloadutils.find_archive(software, version)
    assert bool(archive) is found
