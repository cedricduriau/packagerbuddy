# stdlib
import os

# third party
import pytest

# package
from packagerbuddy import cli


def test_run():
    with pytest.raises(SystemExit) as exc:
        cli.run(["-h"])

    assert exc.value.code == 0


@pytest.mark.parametrize("args", [([]), (["-!"])])
def test_run_no_action(args: list[str]):
    with pytest.raises(SystemExit) as exc:
        cli.run(args)

    assert exc.value.code == 2


@pytest.mark.parametrize("exists", [(True), (False)])
def test_setup(exists: bool, monkeypatch: pytest.MonkeyPatch):
    def mock_os_path_exists(p: str) -> bool:
        return exists

    def mock_os_makedirs(p: str):
        return

    monkeypatch.setattr(os, "makedirs", mock_os_makedirs)
    monkeypatch.setattr(os.path, "exists", mock_os_path_exists)

    with pytest.raises(SystemExit) as exc:
        cli.run(["setup"])

    assert exc.value.code == 0
