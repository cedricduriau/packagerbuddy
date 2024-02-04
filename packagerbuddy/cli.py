#!/usr/bin/env python

# stdlib
import argparse
import os

# package
from packagerbuddy import configutils, downloadutils, installutils, settings


# ==============================================================================
# actions
# ==============================================================================
def setup():
    dirs = [
        settings.DIR_CONFIG,
        settings.DIR_DOWNLOAD,
        settings.DIR_INSTALL,
        settings.DIR_SCRIPTS,
    ]
    for d in dirs:
        if not os.path.exists(d):
            print(f"creating directory {d}")
            os.makedirs(d)

    if not os.path.exists(settings.FILE_CONFIG):
        print(f"creating file {settings.FILE_CONFIG}")
        configutils.dump({})


def list_available_software() -> None:
    config = configutils.load()
    available = sorted(config.keys())
    print("\n".join(available))


def add_software(software: str, url: str) -> None:
    if not software.strip():
        print("no software provided")
        exit(1)

    if not url.strip():
        print("no url provided")
        exit(1)

    config = configutils.load()

    if configutils.is_software_configured(config, software):
        print("software already configured")
        exit(1)

    if r"{version}" not in url:
        print(r"no {version} format string found in url")
        exit(1)

    configutils.add_software(config, software, url)


def remove_software(software: str) -> None:
    if not software.strip():
        print("no software provided")
        exit(1)

    config = configutils.load()
    if not configutils.is_software_configured(config, software):
        print("software not found")
        exit(1)

    configutils.remove_software(config, software)


def download_software(software: str, version: str) -> None:
    if not software.strip():
        print("no software provided")
        exit(1)

    config = configutils.load()
    if not configutils.is_software_configured(config, software):
        print("software not found")
        exit(1)

    archive = downloadutils.find_archive(software, version)
    if archive is not None:
        print(archive)
        return

    archive = downloadutils.download(software, version, config)
    print(archive)


def install_software(software: str, version: str) -> None:
    if not software.strip():
        print("no software provided")
        exit(1)

    config = configutils.load()
    if not configutils.is_software_configured(config, software):
        print("software not found")
        exit(1)

    if installutils.is_software_installed(software, version):
        dir_install = installutils.build_install_path(software, version)
        print(dir_install)
        return

    archive = downloadutils.find_archive(software, version)
    if archive is None:
        archive = downloadutils.download(software, version, config)

    dir_temp = installutils.build_temporary_install_path(software, version)
    os.makedirs(dir_temp, exist_ok=True)

    installutils.unarchive(archive, dir_temp)

    dir_install = installutils.build_install_path(software, version)
    os.makedirs(dir_install, exist_ok=True)

    installutils.cleanup(config, software, version)

    print(dir_install)


def list_installed_software(software: str | None = None, version: str | None = None) -> None:
    installed = installutils.find_installed_software(software=software, version=version)
    print("\n".join(installed))


# ==============================================================================
# parser
# ==============================================================================
def build_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # ==========================================================================
    # setup
    # ==========================================================================
    help = "set up package content"
    parser_setup = subparsers.add_parser("setup", help=help)
    parser_setup.set_defaults(func=setup)

    # ==========================================================================
    # add
    # ==========================================================================
    help = "add a software configuration"
    parser_add = subparsers.add_parser("add", help=help)
    parser_add.set_defaults(func=add_software)

    # required arguments
    req_args = parser_add.add_argument_group("required arguments")

    help = "name of the software"
    req_args.add_argument("-s", "--software", help=help)

    help = "download url template"
    req_args.add_argument("-u", "--url", help=help)

    # ==========================================================================
    # remove
    # ==========================================================================
    help = "remove a software configuration"
    parser_remove = subparsers.add_parser("remove", help=help)
    parser_remove.set_defaults(func=remove_software)

    # required arguments
    req_args = parser_remove.add_argument_group("required arguments")
    req_args.add_argument("-s", "--software", help="name of the software")

    # ==========================================================================
    # avail
    # ==========================================================================
    help = "list available software to download"
    parser_avail = subparsers.add_parser("avail", help=help)
    parser_avail.set_defaults(func=list_available_software)

    # ==========================================================================
    # download
    # ==========================================================================
    help = "download software"
    parser_download = subparsers.add_parser("download", help=help)
    parser_download.set_defaults(func=download_software)

    # required arguments
    req_args = parser_download.add_argument_group("required arguments")

    help = "name of the software"
    req_args.add_argument("-s", "--software", help=help)

    help = "version of the software"
    req_args.add_argument("-v", "--version", help=help)

    # ==========================================================================
    # install
    # ==========================================================================
    help = "install software"
    parser_install = subparsers.add_parser("install", help=help)
    parser_install.set_defaults(func=install_software)

    # required arguments
    req_args = parser_install.add_argument_group("required arguments")

    help = "name of the software"
    req_args.add_argument("-s", "--software", help=help)

    help = "version of the software"
    req_args.add_argument("-v", "--version", help=help)

    # ==========================================================================
    # list
    # ==========================================================================
    help = "list installed software"
    parser_list = subparsers.add_parser("list", help=help)
    parser_list.set_defaults(func=list_installed_software)

    # optional arguments
    opt_args = parser_list.add_argument_group("optional arguments")

    help = "name of the software"
    opt_args.add_argument("-s", "--software", help=help, required=False)

    help = "version of the software"
    opt_args.add_argument("-v", "--version", help=help, required=False)

    # ==========================================================================
    # parser settings
    # ==========================================================================
    parser.description = "JSON config based software packager."

    return parser


def run(args: list[str] | None = None) -> None:
    parser = build_parser()
    namespace = parser.parse_args(args)
    kwargs = vars(namespace)

    try:
        func = kwargs.pop("func")
    except KeyError:
        print("packagerbuddy: error: missing action, see -h/--help")
        exit(2)

    func(**kwargs)
    exit(0)
