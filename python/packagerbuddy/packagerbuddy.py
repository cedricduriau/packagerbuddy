# stdlib modules
import os
import json
import glob
import shutil
import urllib2
import tarfile


# ============================================================================
# private
# ============================================================================
def _normalize_path(path):
    """
    Returns an absolute version of a path.

    :param path: path to normalize
    :type path: str

    :rtype: str
    """
    return os.path.abspath(os.path.expanduser(path))


def _read_environment_variable(name):
    """
    Returns the path as value of an environment variable.

    :raises EnvironmentError: if the environment variable is not set
    :raises ValueError: if the path in the environment variable does not exist

    :rtype: str
    """
    try:
        path = os.environ[name]
    except KeyError:
        raise EnvironmentError("environment variable {!r} is not set".format(name))

    return _normalize_path(path)


def _download(url, to):
    """
    Downloads the content of an URL to a location.

    :param url: url to from
    :type url: str

    :param to: full path to download to
    :type to: str

    :raises urllib2.HTTPError: if URL does not exist
    """
    try:
        f = urllib2.urlopen(url)
    except urllib2.HTTPError as e:
        if e.code == 404:
            # add custom message
            e.msg = "given software version does not exist"
        raise e

    with open(to, "wb") as local_f:
        local_f.write(f.read())


def _build_archive_name(software, version, extension):
    """
    Builds the name of an archive file for a software release.

    :param software: software to build archive file name for
    :type software: str

    :param version: release of software to build archive file name for
    :type version: str

    :param extension: extension of the archive file
    :type extension: str

    :rtype: str
    """
    return "{}-{}.{}".format(software, version, extension)


def _untar(archive):
    """
    Unpacks a tarfile.

    :param archive: full path of tarfile to unpack
    :type archive: str

    :return: the path of the extracted content
    :rtype: str
    """
    read_mode = "r"
    if archive.endswith("tar.gz"):
        read_mode += ":gz"
    elif archive.endswith("tar.bz"):
        read_mode += ":bz"

    directory = os.path.dirname(archive)
    with tarfile.open(archive, read_mode) as tar:
        # see warning: https://docs.python.org/2/library/tarfile.html#tarfile.TarFile.extractall
        tar.extractall(path=directory)
        return os.path.join(directory, tar.getnames()[0])


def _unpack(archive, extension):
    """
    Unpacks an archive file.

    :param archive: archive file to unpack
    :type archive: str

    :param extension: extension of the archive determining how to unpack it
    :type extension: str

    :return: path of the unpacked content
    :rtype: str
    """
    if "tar" in extension:
        return _untar(archive)


# ============================================================================
# public
# ============================================================================
def get_configs_location():
    """
    Returns the location of the software configs.

    :rtype: str
    """
    return _read_environment_variable("PB_CONFIGS")


def get_download_location():
    """
    Returns the location the software will be downloaded to.

    :rtype: str
    """
    return _read_environment_variable("PB_DOWNLOAD")


def get_install_location():
    """
    Returns the location the software will be installed in.

    :rtype: str
    """
    return _read_environment_variable("PB_INSTALL")


def build_config_name(software):
    """
    Builds the name of a software config.

    :param software: software to build the config name for
    :type software: str

    :rtype: str
    """
    return "config_{software}.json".format(software=software)


def get_config_path(name):
    """
    Gets the full path of a software config.

    :param name: name of the config to get full path for
    :type name: str

    :rtype: str
    """
    return os.path.join(get_configs_location(), name)


def get_config(software):
    """
    Returns the config for a software.

    :param software: software to get config for
    :type software: str

    :raises ValueError: if no config could be found for given software

    :rtype: dict
    """
    name = build_config_name(software)
    path = get_config_path(name)

    if not os.path.exists(path):
        raise ValueError("no config found for software {!r}".format(software))

    with open(path, "r") as fp:
        return json.load(fp)


def install(software, version):
    """
    Installs a specific release of a software.

    :param software: software to install
    :type software: str

    :param version: release of software to install
    :type version: str
    """
    if is_software_installed(software, version):
        print("{} v{} is already installed".format(software, version))
        return

    # get config
    config = get_config(software)
    template = config["url"]
    extension = config["extension"]

    # ensure download location exists
    download_dir = get_download_location()
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # download
    print("downloading ...")
    url = template.format(version=version)
    archive_name = _build_archive_name(software, version, extension)
    archive_path = os.path.join(download_dir, archive_name)
    if not os.path.exists(archive_path):
        _download(url, archive_path)

    # unpack
    print("unpacking ...")
    unpacked_dir = _unpack(archive_path, extension)

    # rename
    target_name = archive_name.replace(extension, "").rstrip(".")
    target_path = os.path.join(download_dir, target_name)
    if not os.path.exists(target_path):
        os.rename(unpacked_dir, target_path)

    # ensure install location exists
    install_dir = get_install_location()
    if not os.path.exists(install_dir):
        os.makedirs(install_dir)

    # install / move
    install_path = os.path.join(install_dir, os.path.basename(target_path))
    if not os.path.exists(install_path):
        print("installing ...")
        shutil.move(target_path, install_path)

    # create .pbsoftware file
    open(os.path.join(install_path, ".pbsoftware"), "w+").close()


def is_software_installed(software, version):
    """
    Returns whether a sofware release is already installed.

    :param software: software to check if it is already installed
    :type software: str

    :param version: release of the software to check if it is already installed
    :type version: str

    :rtype: bool
    """
    target_name = "-".join([software, version])
    install_dir = get_install_location()
    pb_package_file = os.path.join(install_dir, target_name, ".pbsoftware")
    return os.path.exists(pb_package_file)


def get_installed_software():
    """
    Gets the paths of the installed software releases.

    :rtype: list[str]
    """
    install_dir = get_install_location()
    pb_package_files = glob.glob(os.path.join(install_dir, "*", ".pbsoftware"))
    return map(os.path.dirname, pb_package_files)


def get_configs():
    """
    Gets the paths of the available software configs.

    :rtype: list[str]
    """
    configs_dir = get_configs_location()
    return glob.glob(os.path.join(configs_dir, "*.json"))


def get_software_from_config(config):
    """
    Gets the name of the software from a software config.

    :param config: software config to get name of software from
    :type config: str

    :rtype: str
    """
    name = os.path.splitext(os.path.basename(config))[0]
    return name.replace("config_", "")
