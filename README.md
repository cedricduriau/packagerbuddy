# PackagerBuddy
[![platform](https://img.shields.io/badge/platform-linux--x64-lightgrey.svg)](https://img.shields.io/badge/platform-linux--x64-lightgrey.svg)
[![platform](https://img.shields.io/badge/platform-darwin--arm64-lightgrey.svg)](https://img.shields.io/badge/platform-darwin--arm64-lightgrey.svg)
[![license: GPL v3](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://img.shields.io/badge/Python-3.8+-blue.svg)

## Overview

PackagerBuddy is a JSON config based software packager written entirely in Python.

Use Cases

- I set up (virtual) machines often and want to have a quick way of setting up software.
- I run multiple versions of the same software package.
- I don't like how software auto-updates and installs a newer version 
of itself.

## Install

If you wish to install the current master, use the following command:

```sh
# latest master
pip install git+git://github.com/cedricduriau/packagerbuddy.git

# specific version
pip install git+git://github.com/cedricduriau/packagerbuddy.git@{RELEASE}
```

## Usage

### Setup

The setup command will create all directories required to function. By default these are installed in the user home directory. To change the default location, see see [Configure](##Configure).

```sh
packagerbuddy setup
```


### Add software
The add command requires two arguments. The `software` argument used as alias to interact with, and the `url` argument which needs to be an url containing a version placeholder.

```sh
packagerbuddy add --software codium --url https://github.com/VSCodium/vscodium/releases/download/{version}/VSCodium-linux-x64-{version}.tar.gz
```

### Remove software

The remove command requires a single argument, the `software` argument, which needs to match an already added software. To list the available software packages, see `avail` command below.

```sh
packagerbuddy remove --software codium
```

### List available software to install
The `avail` command prints all software names that are present in the config, supported by PackgerBuddy.

```sh
packagerbuddy avail
```

### Install software
The `install` command requires two arguments. The `software` argument which needs to match an alias in the software config and the `version` argument which needs to form an existing download url. If the requested software version has already been installed, the install will stop.

```sh
packagerbuddy install --software codium --version 1.44.0
```

Installing consists of five steps:

1. Download the software from the url in the configs to the designated download directory.
2. Unpack the downloaded content.
3. Install/move the unpacked content to the designated install directory.
4. Run the post install script from the designated scripts directory.

### List installed software
The `list` command prints all installed software. PackagerBuddy knows the difference between ordinary directories and software it installed thanks to a package file which is written out at install time.

```sh
packagerbuddy list
```

### Uninstalling
The `uninstall` command, well, does exactly that. It checks if the given software is installed at all and if so, proceeds to remove the file system contents in the designated install location.

The `version` argument is optional. If it is passed, only given version will be removed. If it is not passed, **all** versions will be uninstalled of given software. Beware of this feature.

```sh
# uninstall all versions
packagerbuddy uninstall --software codium

# uninstall specific version
packagerbuddy uninstall --software codium --version 1.44.0
```

## Configure

### Environment Variables

* `PB_CONFIG` : Path of the software config.
  * default: custom file in the user home. (`~/.packagerbuddy/config/software.json`)
* `PB_DOWNLOAD` : Directory the software will be downloaded to.
  * default: custom directory in the user home. (`~/.packagerbuddy/downloaded`)
* `PB_INSTALL`: Directory the software will be installed in.
  * default: custom directory in the user home. (`~/.packagerbuddy/installed`)
* `PB_SCRIPTS`: Directory of the post install scripts.
  * default: custom directory in the user home. (`~/.packagerbuddy/scripts`)

### Examples

If you want to try out the example shipping with the repository, run following commands from the root of this repo:

```sh
cp -R ./linux-x64/examples/* ~/.packagerbuddy/
cp -R ./darwin-arm64/examples/* ~/.packagerbuddy/
```
