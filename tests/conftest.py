# stdlib
import os

try:
    from urllib.request import build_opener, install_opener
except ImportError:
    from urllib2 import build_opener, install_opener

# tool modules
from tests.mock_urllib import MockHTTPHandler

# third party modules
import pytest


@pytest.fixture
def patch_PB_CONFIG(monkeypatch):
    """Monkey patches the PB_CONFIG environment variable."""
    directory = os.path.dirname(__file__)
    os.environ["PB_CONFIG"] = os.path.join(directory, "test_config", "software.json")


@pytest.fixture
def patch_PB_DOWNLOAD(monkeypatch):
    """Monkey patches the PB_DOWNLOAD environment variable."""
    directory = os.path.dirname(__file__)
    os.environ["PB_DOWNLOAD"] = os.path.join(directory, "test_source")


@pytest.fixture
def patch_PB_INSTALL(monkeypatch):
    """Monkey patches the PB_INSTALL environment variable."""
    directory = os.path.dirname(__file__)
    os.environ["PB_INSTALL"] = os.path.join(directory, "test_install")


@pytest.fixture
def patch_PB_SCRIPTS(monkeypatch):
    """Monkey patches the PB_SCRIPTS environment variable."""
    directory = os.path.dirname(__file__)
    os.environ["PB_SCRIPTS"] = os.path.join(directory, "test_scripts")


@pytest.fixture
def patch_url_handler(monkeypatch):
    """Monkey patches the urllib http handler to return a custom class."""
    my_opener = build_opener(MockHTTPHandler)
    install_opener(my_opener)
