# stdlib modules
import os
from setuptools import setup


def get_default_config():
    """
    Gets the default configuration file that ship with the repository.

    :rtype: str
    """
    path = os.path.join(os.path.dirname(__file__), "config", "software.json")
    return os.path.abspath(path)


setup(name="PackagerBuddy",
      version="1.0.1",
      description="JSON config based software packager.",
      license="MIT",
      author="C&eacute;dric Duriau",
      author_email="duriau.cedric@live.be",
      url="https://github.com/cedricduriau/PackagerBuddy",
      packages=["packagerbuddy"],
      scripts=["bin/packagerbuddy"],
      data_files=[("config", [get_default_config()])])
