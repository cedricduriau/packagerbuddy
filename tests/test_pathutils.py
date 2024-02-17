# third party
import pytest

# package
from packagerbuddy import pathutils


@pytest.mark.parametrize(
    ["path", "expected_root", "expected_ext"],
    [
        ("/root/dir/file.txt", "/root/dir/file.txt", ""),
        ("/root/dir/file.zip", "/root/dir/file", ".zip"),
        ("/root/dir/file.tar", "/root/dir/file", ".tar"),
        ("/root/dir/file.tar.gz", "/root/dir/file", ".tar.gz"),
        ("/root/dir/file.dot1.dot2.tar.gz", "/root/dir/file.dot1.dot2", ".tar.gz"),
    ],
)
def test_split_ext(path: str, expected_root: str, expected_ext: str) -> None:
    root, ext = pathutils.split_ext(path)
    assert root == expected_root
    assert ext == expected_ext
