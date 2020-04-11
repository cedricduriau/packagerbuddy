# stdlib modules
import os
import sys
from setuptools import setup
from setuptools import find_packages

# tool modules
f = os.path.abspath(__file__)
package_dir = os.path.join(os.path.dirname(f), "python")
sys.path.insert(0, package_dir)
from packagerbuddy import __version__  # noqa

requirements_dev = ["flake8==3.6.*",
                    "radon==2.4.*",
                    "pytest==4.0.*",
                    "pytest-cov==2.*",
                    "codecov==2.0.*"]


setup(name="packagerbuddy",
      version=__version__,
      description="JSON config based software packager.",
      license="GPLv3",
      author="C&eacute;dric Duriau",
      author_email="duriau.cedric@live.be",
      url="https://github.com/cedricduriau/packagerbuddy",
      packages=find_packages(where="python"),
      package_dir={"": "python"},
      scripts=["bin/packagerbuddy"],
      extras_require={"dev": requirements_dev},
      data_files=[(os.path.expanduser("~/.packagerbuddy/source"), []),
                  (os.path.expanduser("~/.packagerbuddy/installed"), []),
                  (os.path.expanduser("~/.packagerbuddy/config"), []),
                  (os.path.expanduser("~/.packagerbuddy/scripts"), [])])
