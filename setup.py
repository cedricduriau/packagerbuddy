# stdlib modules
import os
from setuptools import setup


def get_default_configs():
    """
    Gets the default configuration files that ship with the repository.

    :rtype: list[str]
    """
    dirname = "configs"
    dir_configs = os.path.join(os.path.dirname(__file__), dirname)
    return [os.path.join(dirname, f) for f in os.listdir(dir_configs)]


setup(name="PackagerBuddy",
      version="0.1.0",
      description="JSON config based software packager.",
      license="MIT",
      author="C&eacute;dric Duriau",
      author_email="duriau.cedric@live.be",
      url="https://github.com/cedricduriau/PackagerBuddy",
      packages=["packagerbuddy"],
      scripts=["bin/packagerbuddy"],
      data_files=[("configs", get_default_configs())])
