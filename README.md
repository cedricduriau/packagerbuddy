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

Configure
--------
`PB_CONFIGS` : Directory the software configs are located. Defalt value is the configs directory of this repository (`./configs`)

`PB_DOWNLOAD` : Directory the software will be downloaded to. Default value is a custom directory in the user home. (`~/software/source`)

`PB_INSTALL`: Directory the software will be downloaded to. Default value is a custom directory in the user home. (`~/software/installed`)
