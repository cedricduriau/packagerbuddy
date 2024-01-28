# stdlib
import glob
import os
from urllib.request import urlopen

# package
from packagerbuddy import pathutils, settings


def build_archive_path(software: str, version: str, url: str) -> str:
    _, ext = pathutils.split_ext(url)
    basename = "-".join([software, version]) + ext
    dir_archive = os.path.join(settings.DIR_DOWNLOAD, basename)
    return dir_archive


def find_archive(software: str, version: str) -> str | None:
    result = glob.glob(f"{software}-{version}*", root_dir=settings.DIR_DOWNLOAD)
    if result:
        return os.path.join(settings.DIR_DOWNLOAD, result[0])
    return None


def download(software: str, version: str, config: dict[str, str]) -> str:
    template = config[software]
    url = template.format(version=version)
    archive = build_archive_path(software, version, url)

    result = urlopen(url)
    with open(archive, "wb+") as fp:
        fp.write(result.read())

    return archive
