# stdlib
import os
import urllib2

# tool modules
from tests.mock_urllib2 import MockHTTPHandler

# third party modules
import pytest

ROOT_TESTS = os.path.dirname(__file__)


@pytest.fixture
def patch_PB_CONFIG(monkeypatch):
    """Monkey patches the PB_CONFIG environment variable."""
    os.environ["PB_CONFIG"] = os.path.join(ROOT_TESTS, "test_config", "software.json")


@pytest.fixture
def patch_PB_DOWNLOAD(monkeypatch):
    """Monkey patches the PB_DOWNLOAD environment variable."""
    os.environ["PB_DOWNLOAD"] = os.path.join(ROOT_TESTS, "test_source")


@pytest.fixture
def patch_PB_INSTALL(monkeypatch):
    """Monkey patches the PB_INSTALL environment variable."""
    os.environ["PB_INSTALL"] = os.path.join(ROOT_TESTS, "test_install")


@pytest.fixture
def patch_PB_SCRIPTS(monkeypatch):
    """Monkey patches the PB_SCRIPTS environment variable."""
    os.environ["PB_SCRIPTS"] = os.path.join(ROOT_TESTS, "test_scripts")


@pytest.fixture
def patch_urllib2(monkeypatch):
    """Monkey patches the urllib2 module to return custom requests."""
    my_opener = urllib2.build_opener(MockHTTPHandler)
    urllib2.install_opener(my_opener)
