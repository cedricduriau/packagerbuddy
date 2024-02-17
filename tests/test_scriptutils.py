# stdlib
import os

# package
from packagerbuddy import scriptutils


def test_find_scripts(
    mock_settings_dir_scripts: None,
    fix_dir_scripts: str,
) -> None:
    scripts = scriptutils.find_scripts("foo", "0.1.0")
    assert scripts == [
        os.path.join(fix_dir_scripts, "foo"),
        os.path.join(fix_dir_scripts, "foo-0.1.0"),
    ]
