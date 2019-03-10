# stdlib modules
import os
from setuptools import setup


setup(name="packagerbuddy",
      version="1.1.0",
      description="JSON config based software packager.",
      license="MIT",
      author="C&eacute;dric Duriau",
      author_email="duriau.cedric@live.be",
      url="https://github.com/cedricduriau/packagerbuddy",
      packages=["packagerbuddy"],
      scripts=["bin/packagerbuddy"],
      data_files=[(os.path.expanduser("~/.packagerbuddy/source"), []),
                  (os.path.expanduser("~/.packagerbuddy/installed"), []),
                  (os.path.expanduser("~/.packagerbuddy/config"), []),
                  (os.path.expanduser("~/.packagerbuddy/scripts"), [])])
