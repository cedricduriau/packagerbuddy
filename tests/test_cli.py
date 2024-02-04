# stdlib
import os

# third party
import pytest

# package
from packagerbuddy import cli, configutils


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


def test_list_available_software(capsys, monkeypatch: pytest.MonkeyPatch):
    def mock_configutils_load() -> dict:
        return {"a": "foo", "b": "bar"}

    monkeypatch.setattr(configutils, "load", mock_configutils_load)

    with pytest.raises(SystemExit) as exc:
        cli.run(["avail"])

    assert exc.value.code == 0
    out, _err = capsys.readouterr()
    assert out == "\n".join(["a", "b"]) + "\n"
