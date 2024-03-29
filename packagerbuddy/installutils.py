# stdlib
import glob
import os
import shutil
import tarfile
import zipfile
from typing import Callable

# package
from packagerbuddy import pathutils, settings


def build_temporary_install_path(software: str, version: str) -> str:
    basename = f"tmp-{software}-{version}"
    path = os.path.join(settings.DIR_INSTALL, basename)
    return path


def build_install_path(software: str, version: str) -> str:
    path = build_temporary_install_path(software, version)
    path = path.replace("tmp-", "")
    return path


def is_software_installed(software: str, version: str) -> bool:
    path = build_install_path(software, version)
    exists = os.path.exists(path)
    return exists


def get_archive_name(software: str, version: str, config: dict[str, str]) -> str:
    template = config[software]
    url = template.format(version=version)
    basename = os.path.basename(url)
    _, ext = pathutils.split_ext(basename)
    archive_name = basename.replace(ext, "")
    return archive_name


def unzip(archive: str, target: str) -> None:
    with zipfile.ZipFile(archive, "r") as fp:
        fp.extractall(target)


def untar(archive: str, target: str) -> None:
    read_mode = "r"
    if archive.endswith(".tgz") or archive.endswith(".tar.gz"):
        read_mode += ":gz"
    elif archive.endswith("tar.bz2"):
        read_mode += ":bz2"

    with tarfile.open(archive, read_mode) as tar:
        tar.extractall(path=target)


def unarchive(archive: str, target: str) -> None:
    _, ext = pathutils.split_ext(archive)
    map_extension_func: dict[str, Callable] = {
        ".zip": unzip,
        ".tar": untar,
        ".tgz": untar,
        ".tar.gz": untar,
        ".tar.bz2": untar,
    }
    func = map_extension_func[ext]
    func(archive, target)


def cleanup(config: dict[str, str], software: str, version: str) -> None:
    dir_temp = build_temporary_install_path(software, version)
    dir_install = build_install_path(software, version)
    archive_name = get_archive_name(software, version, config)
    contents = os.listdir(dir_temp)
    if len(contents) == 1 and contents[0] == archive_name:
        shutil.copytree(os.path.join(dir_temp, archive_name), dir_install, dirs_exist_ok=True)
        shutil.rmtree(dir_temp)
    else:
        os.rename(dir_temp, dir_install)


def find_installed_software(software: str | None = None, version: str | None = None) -> list[str]:
    glob_path = build_install_path(software or "*", version or "*")
    result = glob.glob(glob_path)
    result.sort()
    return result


def uninstall_software(dir_install: str) -> None:
    shutil.rmtree(dir_install)
