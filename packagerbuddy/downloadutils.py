# stdlib
import glob
import os
from urllib.request import urlopen

# package
from packagerbuddy import settings


def build_archive_path(software: str, version: str, url: str) -> str:
    _, ext = os.path.splitext(url)
    basename = "-".join([software, version]) + ext
    dir_archive = os.path.join(settings.DIR_DOWNLOAD, basename)
    return dir_archive


def find_archive(software: str, version: str) -> str | None:
    result = glob.glob(f"{software}-{version}*", root_dir=settings.DIR_DOWNLOAD)
    if result:
        return os.path.join(settings.DIR_DOWNLOAD, result[0])
    return None


def download(url: str, dir_archive: str) -> str:
    result = urlopen(url)
    with open(dir_archive, "wb+") as fp:
        fp.write(result.read())
