# stdlib
import os
import urllib2

# tool modules
from tests.mock_urllib2 import MockHTTPHandler

# third party modules
import pytest

ROOT_TESTS = os.path.dirname(__file__)


@pytest.fixture
def patch_PB_CONFIGS(monkeypatch):
    """Monkey patches the PB_CONFIGS environment variable."""
    os.environ["PB_CONFIGS"] = os.path.join(ROOT_TESTS, "test_configs")


@pytest.fixture
def patch_PB_DOWNLOAD(monkeypatch):
    """Monkey patches the PB_DOWNLOAD environment variable."""
    os.environ["PB_DOWNLOAD"] = os.path.join(ROOT_TESTS, "test_source")


@pytest.fixture
def patch_PB_INSTALL(monkeypatch):
    """Monkey patches the PB_INSTALL environment variable."""
    os.environ["PB_INSTALL"] = os.path.join(ROOT_TESTS, "test_install")


@pytest.fixture
def patch_urllib2(monkeypatch):
    """Monkey patches the urllib2 module to return custom requests."""
    my_opener = urllib2.build_opener(MockHTTPHandler)
    urllib2.install_opener(my_opener)
