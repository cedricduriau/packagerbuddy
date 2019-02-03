# stdlib modules
from __future__ import absolute_import
import os
import sys
import json
import glob
import shutil
import urllib2
import tarfile
import subprocess


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


def _download(url, directory):
    """
    Downloads the content of an URL to a location.

    :param url: url to from
    :type url: str

    :param directory: directory to download to
    :type directory: str

    :return: full path of downloaded archive
    :rtype: str
    """
    request = urllib2.urlopen(url)
    try:
        headers = request.headers
        archive_name = headers["content-disposition"].split("filename=")[1]
    except KeyError:
        archive_name = os.path.basename(request.url)

    archive_path = os.path.join(directory, archive_name)
    with open(archive_path, "wb+") as fp:
        fp.write(request.read())

    return archive_path


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

    Contents of the tarfile will be extracted right now to the archive itself.

    :param archive: full path of tarfile to unpack
    :type archive: str

    :return: the path of the extracted content
    :rtype: str
    """
    # https://docs.python.org/2.7/library/tarfile.html#tarfile.open
    read_mode = "r"
    if archive.endswith("tar.gz"):
        read_mode += ":gz"
    elif archive.endswith("tar.bz2"):
        read_mode += ":bz2"

    directory = os.path.dirname(archive)
    with tarfile.open(archive, read_mode) as tar:
        tar.extractall(path=directory)
        return os.path.join(directory, tar.getnames()[0])


def _build_download_url(template, version):
    """
    Builds the software release download url.

    :param template: url template
    :type template: str

    :param version: software release
    :type version: str
    """
    return template.format(version=version)


def _get_archive(software, version):
    """
    Gets the downloaded source archive for a software version.

    :param software: software to get the downloaded source archive for
    :type software: str

    :param version: software release
    :type version: str
    """
    download_dir = get_download_location()
    archives = os.listdir(download_dir)
    prefix = "{}-{}.".format(software, version)

    for archive in archives:
        if archive.startswith(prefix):
            return os.path.join(download_dir, archive)

    return None


def _split_ext(path):
    """
    Splits a path from its extension.

    :param path: path to split
    :type path: str

    :return: path excluding extension and extension
    :rtype: str, str
    """
    # dump extra header data
    if "&" in path:
        path = path.split("&")[0]

    # assume non .tar extensions do not have any suffix/compression
    if ".tar" not in path:
        path_noext, ext = os.path.splitext(path)
    else:
        for i in {".tar.gz", ".tar.bz2", ".tar"}:
            if path.endswith(i):
                path_noext, ext = path.rstrip(i), i
                break

    if not ext:
        msg = "could not retrieve extension from path: {}"
        raise ValueError(msg.format(path))

    return path_noext, ext


# ============================================================================
# public
# ============================================================================
def get_config_location():
    """
    Returns the full path of the software config.

    :rtype: str
    """
    default = "~/.packagerbuddy/config/software.json"
    path_config = os.getenv("PB_CONFIG", default)
    return _normalize_path(path_config)


def get_download_location():
    """
    Returns the location the software will be downloaded to.

    :rtype: str
    """
    dir_download = os.getenv("PB_DOWNLOAD", "~/.packagerbuddy/source/")
    return _normalize_path(dir_download)


def get_install_location():
    """
    Returns the location the software will be installed in.

    :rtype: str
    """
    dir_install = os.getenv("PB_INSTALL", "~/.packagerbuddy/installed/")
    return _normalize_path(dir_install)


def get_scripts_location():
    """
    Returns the location of the post install scripts.

    :rtype: str
    """
    dir_scripts = os.getenv("PB_SCRIPTS", "~/.packagerbuddy/scripts/")
    return _normalize_path(dir_scripts)


def get_config():
    """
    Returns the software config.

    :rtype: dict
    """
    with open(get_config_location(), "r") as fp:
        return json.load(fp)


def install(software, version, force=False):
    """
    Installs a specific release of a software.

    :param software: software to install
    :type software: str

    :param version: release of software to install
    :type version: str

    :param force: set True to force the install procedure again
    :type force: bool
    """
    if is_software_installed(software, version) and not force:
        print("{} v{} is already installed".format(software, version))
        return

    # get config
    config = get_config()

    # validate config for software and version
    validate_config(config, software, version)

    # download
    print("downloading ...")
    download_dir = get_download_location()
    url = config[software].format(version=version)

    archive_path = _get_archive(software, version)
    if archive_path is None:
        # download
        source = _download(url, download_dir)

        # rename
        try:
            _, extension = _split_ext(url)
        except ValueError:
            _, extension = _split_ext(source)
        validate_extension(extension)

        archive_name = _build_archive_name(software, version, extension)
        archive_path = os.path.join(download_dir, archive_name)

        if os.path.basename(source) != archive_name:
            os.rename(source, archive_path)
    else:
        extension = _split_ext(archive_path)[1]
        archive_name = os.path.basename(archive_path)

    # extract
    print("extracting ...")
    target_name = archive_name.replace(extension, "").rstrip(".")
    target_path = os.path.join(download_dir, target_name)
    if not os.path.exists(target_path):
        # extract
        unpacked_dir = _untar(archive_path)

        # rename
        if not os.path.exists(target_path):
            os.rename(unpacked_dir, target_path)

    # install / move
    print("installing ...")
    install_dir = get_install_location()
    install_path = os.path.join(install_dir, os.path.basename(target_path))
    if not os.path.exists(install_path):
        shutil.move(target_path, install_path)

    # create .pbsoftware file
    cache_file = os.path.join(install_path, ".pbsoftware")
    if not os.path.exists(cache_file):
        open(cache_file, "w+").close()

    # run post install script
    script = get_script(software)
    if script:
        run_script(script, software, version, wd=install_path)


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
    cache_file = os.path.join(install_dir, target_name, ".pbsoftware")
    return os.path.exists(cache_file)


def get_installed_software():
    """
    Gets the paths of the installed software releases.

    :rtype: list[str]
    """
    install_dir = get_install_location()
    pb_package_files = glob.glob(os.path.join(install_dir, "*", ".pbsoftware"))
    return sorted(map(os.path.dirname, pb_package_files))


def get_suported_extensions():
    """
    Returns the supported software archive extensions.

    :rtype: set[str]
    """
    return {".tar", ".tar.gz", ".tar.bz"}


def validate_config(config, software, version):
    """
    Validates a software config.

    :param config: software config to validate
    :type config: dict

    :param software: software to validate in config
    :type config: str

    :param config: release of software to validate in config
    :type config: str

    :raises KeyError: if software is not in config
    :raises ValueError: if url is empty
    :raises ValueError: if url has no version placeholder
    :raises ValueError: if url is invalid
    :raises ValueError: if extension is not supported
    """
    # is software in config
    if software not in config:
        raise KeyError("software {!r} has no configuration".format(software))

    # is url empty
    url = config[software]
    if not url:
        raise ValueError("url for software {!r} is empty".format(software))

    # does url have version placeholder
    validate_template_url(url)

    # is url valid
    url = _build_download_url(url, version)
    try:
        result = urllib2.urlopen(url)
    except Exception as e:
        raise ValueError("invalid url {!r} for software {!r} "
                         "({})".format(url, software, str(e)))

    # is extension valid
    try:
        _path, ext = _split_ext(url)
    except ValueError:
        _path, ext = _split_ext(result.url)

    validate_extension(ext)


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
    name_by_version = {n.split("-")[-1]: n for n in paths_by_name
                       if n.startswith(software)}

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


def setup():
    """Ensures all default directories exist and default config is copied."""
    # create directories
    path_config = get_config_location()
    dir_download = get_download_location()
    dir_install = get_install_location()
    dir_scripts = get_scripts_location()

    for d in [dir_download, dir_install, dir_scripts]:
        if not os.path.exists(d):
            print("creating {}".format(d))
            os.makedirs(d)

    # copy config
    default_config = os.path.join(sys.prefix, "config", "software.json")
    if not os.path.exists(path_config):
        os.makedirs(os.path.dirname(path_config))
        print("copying {} -> {}".format(default_config, path_config))
        shutil.copy2(default_config, path_config)

    # copy scripts
    default_scripts = os.path.join(sys.prefix, "config")
    scripts = os.listdir(default_scripts)
    for script in scripts:
        dst_script = os.path.join(dir_scripts)
        if not os.path.exists(dst_script):
            src_script = os.path.join(default_scripts, script)
            print("copying {} -> {}".format(src_script, dst_script))
            shutil.copy2(src_script, dst_script)


def validate_template_url(url):
    """
    Validates a download url template.

    :param url: url to validate
    :type url: str

    :raises ValueError: if no version placeholder is present in url
    """
    format_key = r"{version}"
    if format_key not in url:
        msg = "no format key {!r} found in url {!r}"
        raise ValueError(msg.format(format_key, url))


def validate_software(software):
    """
    Validates a software name.

    :param software: software to validate
    :type software: str

    :raises ValueError: if software name is empty
    :raises ValueError: if software name is only consists of whitespace(s)
    """
    # empty
    if not software:
        raise ValueError("software cannot be empty")

    # only whitespace(s)
    if software.strip() == "":
        raise ValueError("software cannot be whitespace only")


def add_software(software, url):
    """
    Adds a software configuration.

    :param software: name of the software to add
    :type software: str

    :param url: download url template of the software
    :type url: str
    """
    validate_software(software)

    config = get_config()
    if software in config:
        print("software {!r} already added".format(software))
        return

    validate_template_url(url)
    config[software] = url

    # write out changes
    with open(get_config_location(), "w") as fp:
        json.dump(config, fp)


def remove_software(software):
    """
    Removes a software configuration.

    :param software: software to remove
    """
    config = get_config()

    try:
        config.pop(software)
    except KeyError:
        print("software {!r} is not present in config".format(software))
        return

    # write out changes
    with open(get_config_location(), "w") as fp:
        json.dump(config, fp)


def validate_extension(extension):
    """
    Validates an extension.

    :param extension: extension to validate
    :type extension: str

    :raises ValueError: if extension is not supported
    """
    valid_exts = get_suported_extensions()
    if extension not in valid_exts:
        msg = "invalid extension {!r}, valid extensions are: {}"
        raise ValueError(msg.format(extension, ", ".join(valid_exts)))


def get_script(software):
    """
    Gets the path of the post install script of a software.

    :rtype: str
    """
    dir_scripts = get_scripts_location()
    scripts = os.listdir(dir_scripts)

    for script in scripts:
        if script == software:
            return os.path.join(dir_scripts, script)

    return None


def run_script(script, software, version, wd=None):
    """
    Run a post install script for a specific software.

    :param script: post install script
    :type script: str

    :param software: software to run post install script for
    :type software: str

    :param version: version of the software to run post install script for
    :type version: str

    :param wd: working directory path to run the script from
    :type wd: str
    """
    cmd = [script, software, version]
    process = subprocess.Popen(" ".join(cmd),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=True,
                               cwd=wd)
    print("running post install script ...")
    stdout, stderr = process.communicate()
    if stdout:
        print(stdout)
    if stderr:
        print(stderr)
