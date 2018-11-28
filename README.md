PackagerBuddy
==============

[![Build Status](https://travis-ci.org/cedricduriau/packagerbuddy.svg?branch=master)](https://travis-ci.org/cedricduriau/packagerbuddy)
[![codecov](https://codecov.io/gh/cedricduriau/packagerbuddy/branch/master/graph/badge.svg)](https://codecov.io/gh/cedricduriau/packagerbuddy)

Overview
--------
PackagerBuddy is a JSON config based software packager written entirely in Python.

Use Cases
--------
- I set up (virtual) machines often and want to have a quick way of setting up software.
- I run multiple versions of the same software package.
- I don't like how software auto-updates and installs a newer version 
of itself.

Usage
--------
### Install software
The `install` command requires two arguments. The `software` argument which needs to match an existing config and the `version` argument which needs to form an existing download url. If the requested software version has already been installed, the install will stop. If you wish to force an install 
again, the `force` flag covers this feature.

```
# short notation
packagerbuddy install -s foo -v 1.0.0
packagerbuddy install -s foo -v 1.0.0 -f

# long notation
packagerbuddy install --software foo --version 1.0.0
packagerbuddy install --software foo --version 1.0.0 --force

# foo needs to match with a config named config_foo.json
# 1.0.0 needs to form an existing url, formatted into the config url
# see example in configure section of README for more details
```

Installing consists of four steps:

1. Download the software from the url in the configs to the designated download directory.
2. Unpack the downloaded content based on the extension in the config.
3. Install/move the unpacked content to the designated install directory.
4. Create a package file inside the installed directory.

### List installed software
The `list` command prints all installed software. PackagerBuddy knows the difference between ordinary directories and software it installed thanks to a package file which is written out at install time.
```
packagerbuddy list
```

### List software available to install
The `avail` command prints all software names that PackagerBuddy holds a config for.
```
packagerbuddy avail
```

### Uninstalling
The `uninstall` command well, does exactly that. It checks if the given software is installed at all and if so, proceeds to remove the file system contents in the designated install location.

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


Configure
--------

### Environment Variables

* `PB_CONFIGS` : Directory the software configs are located. 
  * default: configs directory of this repository (`./configs`)
* `PB_DOWNLOAD` : Directory the software will be downloaded to.
  * default: custom directory in the user home. (`~/software/.source`)
* `PB_INSTALL`: Directory the software will be installed in.
  * default: custom directory in the user home. (`~/software/.installed`)

### Configs

Software configuration files are small and easy to set up.
They consist of two keys, the download url template and an extension.

```
// example config_foo.json
{
    "url": "https://software.com/{version}",
    "extension": "tar.gz"
}
```

* `url`: Web address triggering the download of a release of the software, with the release version replaced by a {version} placeholder.
* `extension`: Extension of the content of the web adress determining how to unpack the content.

TIPS-N-TRICKS: You can figure out the download url of a software by going the standard route, browse to the download page and when you found a link that triggers the automatic download, right click on that link and open it in a new page. You can then evaluate safely the address and figure out where to replace the release version with the {version} placeholder.