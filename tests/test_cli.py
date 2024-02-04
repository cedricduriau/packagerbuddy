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


@pytest.mark.parametrize(
    ["software", "url", "exit_code", "configured"],
    [
        ("", "", 1, False),
        (" ", "", 1, False),
        ("foo", " ", 1, False),
        ("foo", "bar", 0, True),
        ("foo", r"https://example.com/{version}/foo.zip", 0, False),
    ],
)
def test_add_software(
    software: str,
    url: str,
    exit_code: int,
    configured: bool,
    capsys,
    monkeypatch: pytest.MonkeyPatch,
):
    mock_config: dict = {}
    if configured:
        mock_config[software] = url

    def mock_configutils_load() -> dict:
        return mock_config

    def mock_configutils_dump(config: dict):
        return

    monkeypatch.setattr(configutils, "load", mock_configutils_load)
    monkeypatch.setattr(configutils, "dump", mock_configutils_dump)

    with pytest.raises(SystemExit) as exc:
        cli.run(["add", "-s", software, "-u", url])

    assert exc.value.code == exit_code
    out, _err = capsys.readouterr()

    if exit_code == 0:
        assert mock_config[software] == url
