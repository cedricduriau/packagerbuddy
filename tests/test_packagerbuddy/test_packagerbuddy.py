# stlib modules
from __future__ import absolute_import
import os
import uuid

# tool modules
from packagerbuddy import packagerbuddy

# third party modules
import pytest


def test_normalize_path():
    """Test normalizing paths."""
    # ensure tilde is being resolved
    assert packagerbuddy._normalize_path("~/") == os.environ["HOME"]

    # ensure same level relative is being resolved
    assert packagerbuddy._normalize_path("/tmp/./test.txt") == "/tmp/test.txt"

    # ensure single level up relative is being resolved
    assert packagerbuddy._normalize_path("/tmp/dir/../test.txt") == "/tmp/test.txt"


def test_read_environment_variable():
    """Test reading the valid of a valid env var."""
    # set test env var
    os.environ["TEST"] = "/tmp"

    # get env var value
    assert packagerbuddy._read_environment_variable("TEST") == "/tmp"

    # function returns normalized result so trailing sep should be gone
    os.environ["TEST"] = "/tmp/"
    assert packagerbuddy._read_environment_variable("TEST") == "/tmp"

    # remove env var
    os.environ.pop("TEST")


def test_read_environment_variable_fail():
    """Test reading the valid of an invalid env var."""
    # reading from fictional env var with unique name based on uuid4
    with pytest.raises(EnvironmentError):
        assert packagerbuddy._read_environment_variable(str(uuid.uuid4()))


def test_download():
    pass


def test_build_archive_name():
    """Test building the archive name of a specific software release."""
    assert packagerbuddy._build_archive_name("software", "version", "ext") == "software-version.ext"


def test_untar():
    pass


def test_unpack():
    pass


def test_get_configs_location(patch_PB_CONFIGS):
    """Test getting the software configs location."""
    current_dir = os.path.dirname(__file__)
    expected = os.path.abspath(os.path.join(current_dir, "..", "test_configs"))
    assert packagerbuddy.get_configs_location() == expected


def test_get_download_location(patch_PB_DOWNLOAD):
    """Test getting the software download location."""
    current_dir = os.path.dirname(__file__)
    expected = os.path.abspath(os.path.join(current_dir, "..", "test_source"))
    assert packagerbuddy.get_download_location() == expected


def test_get_install_location(patch_PB_INSTALL):
    """Test getting the software install location."""
    current_dir = os.path.dirname(__file__)
    expected = os.path.abspath(os.path.join(current_dir, "..", "test_install"))
    assert packagerbuddy.get_install_location() == expected


def test_build_config_name():
    """Test buidling a software config name."""
    assert packagerbuddy._build_config_name("test") == "config_test.json"


def test_get_config_path(patch_PB_CONFIGS):
    """Test getting the path of a software config."""
    name = "config_valid.json"
    current_dir = os.path.dirname(__file__)
    expected = os.path.abspath(os.path.join(current_dir, "..", "test_configs", name))
    assert packagerbuddy._get_config_path(name) == expected


def test_get_config(patch_PB_CONFIGS):
    """Test getting the config for a valid software."""
    assert packagerbuddy.get_config("valid") == {"url": "www.cedricduriau.be", "extension": "cat"}


def test_get_config_fail(patch_PB_CONFIGS):
    """Test getting the config for an invalid software."""
    with pytest.raises(ValueError):
        packagerbuddy.get_config(uuid.uuid4())


def test_install():
    pass


def test_is_software_installed(patch_PB_INSTALL):
    """Test checking whether a software is installed or not."""
    assert packagerbuddy.is_software_installed("valid", "1.0.0") is True
    assert packagerbuddy.is_software_installed("valid", "0.0.0") is False


def test_get_installed_software(patch_PB_INSTALL):
    """Test getting the installed software releases."""
    assert packagerbuddy.get_installed_software() == [os.path.join(os.environ["PB_INSTALL"], "valid-1.0.0")]


def test_get_configs(patch_PB_CONFIGS):
    """Test getting the available software configs."""
    assert packagerbuddy.get_configs() == [os.path.join(os.environ["PB_CONFIGS"], "config_valid.json")]


def test_get_software_from_config():
    """Test getting the name of a software from a software config."""
    assert packagerbuddy.get_software_from_config("config_foo.json") == "foo"
    assert packagerbuddy.get_software_from_config("~/config_foo-bar.json") == "foo-bar"
    assert packagerbuddy.get_software_from_config("../config_fu.manchu.json") == "fu.manchu"


def test_get_suported_extensions():
    """Test getting the supported software archive extensions."""
    assert packagerbuddy.get_suported_extensions() == set(["tar", "tar.gz", "tar.bz"])


def test_validate_config_name():
    """Test validating valid software config names."""
    # path
    packagerbuddy.validate_config_name("~/config_foo.json") == "foo"

    # filename
    packagerbuddy.validate_config_name("config_bar.json") == "bar"


def test_validate_config_name_fail():
    """Test validating invalid software config names."""
    # path does not start with config_
    with pytest.raises(ValueError):
        packagerbuddy.validate_config_name("~/foo.json")

    # path does not end with .json
    with pytest.raises(ValueError):
        packagerbuddy.validate_config_name("~/config_foo.yml")

    # filename does not start with config_
    with pytest.raises(ValueError):
        packagerbuddy.validate_config_name("foo.json")

    # filename does not end with .json
    with pytest.raises(ValueError):
        packagerbuddy.validate_config_name("config_foo.yml")


def test_validate_config(patch_urllib2):
    """Test validating a valid software config."""
    config = {"url": "http://valid.com", "extension": "tar"}
    packagerbuddy.validate_config(config)


def test_validate_config_fail(patch_urllib2):
    """Test validating invalid software configs."""
    # missing key url
    with pytest.raises(KeyError):
        packagerbuddy.validate_config({"extension": None})

    # missing key extension
    with pytest.raises(KeyError):
        packagerbuddy.validate_config({"url": None})

    # no url value
    with pytest.raises(ValueError):
        packagerbuddy.validate_config({"url": None, "extension": None})

    # invalid url
    with pytest.raises(ValueError):
        packagerbuddy.validate_config({"url": "http://invalid.com", "extension": None})

    # no extension
    with pytest.raises(ValueError):
        packagerbuddy.validate_config({"url": "http://valid.com", "extension": None})

    # invalid extension, leading dot
    with pytest.raises(ValueError):
        packagerbuddy.validate_config({"url": "http://valid.com", "extension": ".tar"})

    # invalid extension, unsupported
    with pytest.raises(ValueError):
        packagerbuddy.validate_config({"url": "http://valid.com", "extension": "foo"})
