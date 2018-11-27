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
    """
    f = urllib2.urlopen(url)
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


def _build_config_name(software):
    """
    Builds the name of a software config.

    :param software: software to build the config name for
    :type software: str

    :rtype: str
    """
    return "config_{software}.json".format(software=software)


def _get_config_path(name):
    """
    Gets the full path of a software config.

    :param name: name of the config to get full path for
    :type name: str

    :rtype: str
    """
    return os.path.join(get_configs_location(), name)


def _build_download_url(template, version):
    """
    Builds the software release download url.

    :param template: url template
    :type template: str

    :param version: software release
    :type version: str
    """
    return template.format(version=version)


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


def get_config(software):
    """
    Returns the config for a software.

    :param software: software to get config for
    :type software: str

    :raises ValueError: if no config could be found for given software

    :rtype: dict
    """
    name = _build_config_name(software)
    path = _get_config_path(name)

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

    # validate config
    validate_config(config, version)

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
    return sorted(map(os.path.dirname, pb_package_files))


def get_configs():
    """
    Gets the paths of the available software configs.

    :rtype: list[str]
    """
    configs_dir = get_configs_location()
    return sorted(glob.glob(os.path.join(configs_dir, "*.json")))


def get_software_from_config(name):
    """
    Gets the name of the software from a software config path or filename.

    :param name: path of filename of a software config
    :type name: str

    :rtype: str
    """
    validate_config_name(name)
    name = os.path.splitext(os.path.basename(name))[0]
    return name.replace("config_", "")


def get_suported_extensions():
    """
    Returns the supported software archive extensions.

    :rtype: set[str]
    """
    return {"tar", "tar.gz", "tar.bz"}


def validate_config_name(name):
    """
    Validates the name of a software config.

    :raises ValueError: if the software config name does not start with _config
    :raises ValueError: if the software config name does not end with .json
    """
    name = os.path.basename(name)

    if not name.startswith("config_"):
        raise ValueError("invalid name {!r}, does not start with 'config_'".format(name))

    if not name.endswith(".json"):
        raise ValueError("invalid name {!r}, does not end with '.json'".format(name))


def validate_config(config, version):
    """
    Validates a software config.

    :param config: software config to validate
    :type config: dict

    :raises KeyError: if url key is missing
    :raises KeyError: if extension key is missing
    :raises ValueError: if url is empty
    :raises ValueError: if url has no version placeholder
    :raises ValueError: if url is invalid
    :raises ValueError: if extension is empty
    :raises ValueError: if extension starts with a dot
    :raises ValueError: if extension is not supported
    """
    # keys
    req_keys = ["url", "extension"]
    for k in req_keys:
        if k not in config:
            raise KeyError("missing key {!r}".format(k))

    # url
    url = config["url"]
    if not url:
        raise ValueError("url is empty")

    format_key = r"{version}"
    if format_key not in url:
        raise ValueError("invalid url {!r}, needs to contain a {!r} placeholder".format(url, format_key))

    try:
        url = _build_download_url(url, version)
        urllib2.urlopen(url)
    except Exception as e:
        raise ValueError("invalid url {} ({})".format(url, str(e)))

    # extension
    ext = config["extension"]
    if not ext:
        raise ValueError("extension is empty")

    if ext.startswith("."):
        raise ValueError("invalid extension {!r}, cannot include leading dot".format(ext))

    valid_exts = get_suported_extensions()
    if ext not in valid_exts:
        raise ValueError("invalid extension {!r}, valid extensions are: {}".format(ext, ", ".join(valid_exts)))


def uninstall(software, version=None, dry_run=False):
    """
    Uninstalls one or all versions of a software.

    :param software: name of the softare to uninstall
    :type software: str

    :param version: release of the softare to uninstall, if not given, all
                    releases will be uninstalled
    :type version: str

    :param dry_run: set True to skip the actual file system content
    :type dry_run: bool
    """
    if dry_run:
        print("!DRY-RUN MODE!")

    # get installed software paths
    installed = get_installed_software()

    # group paths by name for easy lookup
    paths_by_name = {os.path.basename(p): p for p in installed}

    # group names by version for easy lookup
    name_by_version = {n.split("-")[-1]: n for n in paths_by_name}

    # get how many versions of software to uninstall
    to_uninstall = name_by_version.keys()
    if version and version in name_by_version:
        to_uninstall = [version]

    for v in to_uninstall:
        name = name_by_version[v]
        path = paths_by_name[name]

        print("uninstalling {} ...".format(name))
        if not dry_run:
            shutil.rmtree(path)
