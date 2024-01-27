#!/usr/bin/env python

# stdlib
import argparse
import json
import os

# package
from packagerbuddy import configutils, downloadutils, settings


# ==============================================================================
# actions
# ==============================================================================
def setup():
    dirs = [settings.DIR_CONFIG, settings.DIR_DOWNLOAD, settings.DIR_INSTALL]
    for d in dirs:
        if not os.path.exists(d):
            print(f"creating directory {d}")
            os.makedirs(d)

    if not os.path.exists(settings.FILE_CONFIG):
        with open(settings.FILE_CONFIG, "w") as fp:
            print(f"creating file {settings.FILE_CONFIG}")
            json.dump({}, fp)


def list_available_software() -> None:
    config = configutils.load()
    available = sorted(config.keys())
    print("\n".join(available))


def add_software(software: str, url: str) -> None:
    if not software.strip():
        print("no software provided")
        return

    if not url.strip():
        print("no url provided")
        return

    config = configutils.load()

    if configutils.is_software_configured(config, software):
        print("software already configured")
        return

    if r"{version}" not in url:
        print(r"no {version} format string found in url")

    configutils.add_software(config, software, url)


def remove_software(software: str) -> None:
    config = configutils.load()
    if not configutils.is_software_configured(config, software):
        print("software not found")
        return

    configutils.remove_software(config, software)


def download_software(software: str, version: str) -> None:
    archive = downloadutils.find_archive(software, version)
    if archive:
        print(archive)
        return

    config = configutils.load()
    template = config[software]
    url = template.format(version=version)
    archive = downloadutils.build_archive_path(software, version, url)
    downloadutils.download(url, archive)
    print(archive)


def install_software(software: str, version: str) -> None:
    archive = downloadutils.find_archive(software, version)
    if not archive:
        config = configutils.load()
        template = config[software]
        url = template.format(version=version)
        archive = downloadutils.build_archive_path(software, version, url)
        downloadutils.download(url, archive)

    # TODO: extract (into {software-version} dir if possible)
    # TODO: move into {software}

    print(archive)


# ==============================================================================
# parser
# ==============================================================================
def build_parser():
    """
    Builds the command line interface.

    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # ==========================================================================
    # setup
    # ==========================================================================
    help = "set up package content"
    parser_setup = subparsers.add_parser("setup", help=help)
    parser_setup.set_defaults(func=setup)

    # ==========================================================================
    # avail
    # ==========================================================================
    help = "list available software to download"
    parser_avail = subparsers.add_parser("avail", help=help)
    parser_avail.set_defaults(func=list_available_software)

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
    # parser settings
    # ==========================================================================
    parser.description = "JSON config based software packager."

    return parser


def run() -> None:
    parser = build_parser()
    namespace = parser.parse_args()
    kwargs = vars(namespace)

    try:
        func = kwargs.pop("func")
    except KeyError:
        print("Missing or incomplete action, see -h/--help")
        exit()

    try:
        func(**kwargs)
    except Exception as e:
        print(e)
