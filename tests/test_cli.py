# stdlib
import os
import shutil

# third party
import pytest

# package
from packagerbuddy import cli, configutils, downloadutils


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


def test_list_available_software(
    mock_settings_file_config: None,
    capsys,
    monkeypatch: pytest.MonkeyPatch,
):
    with pytest.raises(SystemExit) as exc:
        cli.run(["avail"])

    assert exc.value.code == 0
    out, _err = capsys.readouterr()
    assert out == "foo" + "\n"


@pytest.mark.parametrize(
    ["software", "url", "exit_code", "error"],
    [
        (" ", "", 1, "no software provided"),
        ("foo", " ", 1, "no url provided"),
        ("foo", "bar", 1, "software already configured"),
        ("bar", "bar", 1, r"no {version} format string found in url"),
        ("bar", r"https://example.com/{version}/bar.zip", 0, ""),
    ],
)
def test_add_software(
    software: str,
    url: str,
    exit_code: int,
    error: str,
    capsys,
    mock_settings_file_config: None,
    monkeypatch: pytest.MonkeyPatch,
):
    def mock_configutils_dump(config: dict):
        return

    monkeypatch.setattr(configutils, "dump", mock_configutils_dump)

    with pytest.raises(SystemExit) as exc:
        cli.run(["add", "-s", software, "-u", url])

    assert exc.value.code == exit_code
    out, _err = capsys.readouterr()

    if exit_code != 0:
        assert out == error + "\n"


@pytest.mark.parametrize(
    ["software", "exit_code", "error"],
    [
        (" ", 1, "no software provided"),
        ("bar", 1, "software not found"),
        ("foo", 0, ""),
    ],
)
def test_remove_software(
    software: str,
    exit_code: bool,
    error: str,
    capsys,
    mock_settings_file_config: None,
    monkeypatch: pytest.MonkeyPatch,
):
    def mock_dump(config: dict) -> None:
        return

    monkeypatch.setattr(configutils, "dump", mock_dump)

    with pytest.raises(SystemExit) as exc:
        cli.run(["remove", "-s", software])

    assert exc.value.code == exit_code
    out, _err = capsys.readouterr()

    if exit_code != 0:
        assert out == error + "\n"


@pytest.mark.parametrize(
    ["software", "version", "exit_code", "error"],
    [
        (" ", "0.1.0", 1, "no software provided"),
        ("bar", "0.1.0", 1, "software not found"),
        ("foo", "0.1.0", 0, ""),
        ("foo", "0.3.0", 0, ""),
    ],
)
def test_download_software(
    software: str,
    version: str,
    exit_code: int,
    error: str,
    capsys,
    fix_dir_downloaded: str,
    mock_settings_file_config: None,
    mock_settings_dir_download: None,
    monkeypatch: pytest.MonkeyPatch,
):
    def mock_downloadutils_download(software: str, version: str, config: dict | None = None) -> str:
        path = os.path.join(fix_dir_downloaded, f"{software}-{version}.zip")
        return path

    monkeypatch.setattr(downloadutils, "download", mock_downloadutils_download)

    with pytest.raises(SystemExit) as exc:
        cli.run(["download", "-s", software, "-v", version])

    assert exc.value.code == exit_code
    out, _err = capsys.readouterr()

    if exit_code == 0:
        assert out == mock_downloadutils_download(software, version) + "\n"
    else:
        assert out == error + "\n"


@pytest.mark.parametrize(
    ["software", "version", "exit_code", "error"],
    [
        (" ", "0.1.0", 1, "no software provided"),
        ("bar", "0.1.0", 1, "software not found"),
        ("foo", "0.1.0", 0, ""),
        ("foo", "0.2.0", 0, ""),
    ],
)
def test_install_software(
    software: str,
    version: str,
    exit_code: int,
    error: str,
    capsys,
    fix_dir_installed: str,
    mock_settings_file_config: None,
    mock_settings_dir_download: None,
    mock_settings_dir_install: None,
):
    path = os.path.join(fix_dir_installed, f"{software}-{version}")
    cleanup = not os.path.exists(path)

    with pytest.raises(SystemExit) as exc:
        cli.run(["install", "-s", software, "-v", version])

    assert exc.value.code == exit_code
    out, _err = capsys.readouterr()

    if exit_code == 0:
        assert out == path + "\n"
        if cleanup:
            shutil.rmtree(path)
    else:
        assert out == error + "\n"


@pytest.mark.parametrize(
    ["software", "version", "count"],
    [
        ("", "", 2),
        ("foo", "", 1),
        ("bar", "", 1),
        ("foo", "0.1.0", 1),
    ],
)
def test_list_installed_software(
    software: str,
    version: str,
    count: int,
    capsys,
    mock_settings_dir_install: None,
):
    with pytest.raises(SystemExit) as exc:
        cli.run(["list", "-s", software, "-v", version])

    assert exc.value.code == 0
    out, _err = capsys.readouterr()

    assert len(out.rstrip("\n").split("\n")) == count
