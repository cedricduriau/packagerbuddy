# stdlib
import os


def normalize_path(path: str) -> str:
    return os.path.abspath(os.path.expanduser(path))


DIR_PACKAGE = normalize_path("~/.packagerbuddy")
DIR_CONFIG = os.path.join(DIR_PACKAGE, "config")
DIR_DOWNLOAD = normalize_path(os.getenv("PB_DOWNLOAD", os.path.join(DIR_PACKAGE, "source")))
DIR_INSTALL = normalize_path(os.getenv("PB_INSTALL", os.path.join(DIR_PACKAGE, "installed")))
DIR_SCRIPTS = normalize_path(os.getenv("PB_SCRIPTS", os.path.join(DIR_PACKAGE, "scripts")))
FILE_CONFIG = normalize_path(os.getenv("PB_CONFIG", os.path.join(DIR_CONFIG, "software.json")))
EXTENSIONS: set[str] = {".tgz", ".tar", ".tar.gz", ".tar.bz2"}
