# PackagerBuddy

[![Build Status](https://travis-ci.org/cedricduriau/packagerbuddy.svg?branch=master)](https://travis-ci.org/cedricduriau/packagerbuddy)
[![codecov](https://codecov.io/gh/cedricduriau/packagerbuddy/branch/master/graph/badge.svg)](https://codecov.io/gh/cedricduriau/packagerbuddy)
[![platform](https://img.shields.io/badge/platform-linux--64-lightgrey.svg)](https://img.shields.io/badge/platform-linux--64-lightgrey.svg)
[![python](https://img.shields.io/badge/python-2.7%20|%203.6-blue.svg)](https://img.shields.io/badge/python-2.7%20|%203.6-blue.svg)

## Overview

PackagerBuddy is a JSON config based software packager written entirely in Python for Linux.

Use Cases

- I set up (virtual) machines often and want to have a quick way of setting up software.
- I run multiple versions of the same software package.
- I don't like how software auto-updates and installs a newer version 
of itself.

## Install

If you wish to install the current master, use the following command:

`pip install git+git://github.com/cedricduriau/PackagerBuddy.git`

Or a specific release version:

`pip install git+git://github.com/cedricduriau/PackagerBuddy.git@1.0.1`


This will create all default directories and copy the default configuration file that ships with the repository. (see [Configure](#Configure))

## Usage

### Add software
The add command requires two arguments. The `software` argument used as alias to interact with, and the `url` argument which needs to be an url containing a version placeholder.

```
# short notation
packagerbuddy add -s foo -u http://foo.com/releases/{version}

# long notation
packagerbuddy add --software foo --url http://foo.com/releases/{version}
```

### Remove software

The remove command requires a single argument, the `software` argument, which needs to match an already added software. To list the available software packages, see `avail` command below.

```
# short notation
packagerbuddy remove -s foo

# long notiation
packagerbuddy remove --software foo
```

### Install software
The `install` command requires two arguments. The `software` argument which needs to match an alias in the software config and the `version` argument which needs to form an existing download url. If the requested software version has already been installed, the install will stop. If you wish to force an install 
again, the `force` flag covers this feature.

```
# short notation
packagerbuddy install -s foo -v 1.0.0
packagerbuddy install -s foo -v 1.0.0 -f

# long notation
packagerbuddy install --software foo --version 1.0.0
packagerbuddy install --software foo --version 1.0.0 --force
```

Installing consists of five steps:

1. Download the software from the url in the configs to the designated download directory.
2. Unpack the downloaded content.
3. Install/move the unpacked content to the designated install directory.
4. Create a package file inside the installed directory.
5. Run the post install script from the designated scripts directory.

### List installed software
The `list` command prints all installed software. PackagerBuddy knows the difference between ordinary directories and software it installed thanks to a package file which is written out at install time.
```
packagerbuddy list
```

### List software available to install
The `avail` command prints all software names that are present in the config, supported by PackgerBuddy.
```
packagerbuddy avail
```

### Uninstalling
The `uninstall` command, well, does exactly that. It checks if the given software is installed at all and if so, proceeds to remove the file system contents in the designated install location.

The `version` argument is optional. If it is passed, only given version will be removed. If it is not passed, **all** versions will be uninstalled of given software. Beware of this feature.

If you're the kind of person that prepares a batch of commands before running them and then feed those to a terminal, there is also a `--dry-run` flag for you to enjoy.
```
# short notation
packagerbuddy uninstall -s foo  # uninstalls all versions
packagerbuddy uninstall -s foo -v 1.0.0 # only uninstalls v1.0.0

# long notation
packagerbuddy uninstall --software foo # uninstalls all versions
packagerbuddy uninstall --software foo --version 1.0.0 # only uninstalls v1.0.0

# dry run just prints and does not remove anything at all
packagerbuddy uninstall --software foo --dry-run
```


## Configure

### Environment Variables

* `PB_CONFIG` : Path of the software config.
  * default: custom file in the user home. (`~/.packagerbuddy/config/software.json`)
* `PB_DOWNLOAD` : Directory the software will be downloaded to.
  * default: custom directory in the user home. (`~/.packagerbuddy/source`)
* `PB_INSTALL`: Directory the software will be installed in.
  * default: custom directory in the user home. (`~/.packagerbuddy/installed`)
* `PB_SCRIPTS`: Directory of the post install scripts.
  * default: custom directory in the user home. (`~/.packagerbuddy/scripts`)


### Examples

If you want to try out the example shipping with the repository, run following commands from the root of this repo:

* `cp examples/config/software.json ~/.packagerbuddy/config/`
* `cp examples/scripts/vscode ~/.packagerbuddy/scripts/`

This will allow you to install three software packages. One of them is `vscode` (Visual Studio Code), which has a post install script.
Check out the `vscode` post install script for its inner working.
Check out the [vscode release notes](https://code.visualstudio.com/updates) for a valid version number to install.
