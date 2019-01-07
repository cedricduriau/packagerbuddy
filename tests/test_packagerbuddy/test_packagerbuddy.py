# stlib modules
from __future__ import absolute_import
import os

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


def test_download():
    pass


def test_build_archive_name():
    """Test building the archive name of a specific software release."""
    assert packagerbuddy._build_archive_name("software", "version", "ext") == "software-version.ext"


def test_untar():
    pass


def test_build_download_url():
    """Test building a download url."""
    packagerbuddy._build_download_url("http://valid.com/{version}", "1.0.0") == "http://valid.com/1.0.0"


def test_get_archive(patch_PB_DOWNLOAD):
    download_dir = os.environ["PB_DOWNLOAD"]
    assert packagerbuddy._get_archive("invalid", "1.0.0") is None
    archive = packagerbuddy._get_archive("valid", "1.0.0")
    assert archive == os.path.join(download_dir, "valid-1.0.0.tar.gz")


def test_split_ext():
    assert packagerbuddy._split_ext("/tmp/foo.tar") == ("/tmp/foo", ".tar")
    assert packagerbuddy._split_ext("/tmp/foo.tar.gz") == ("/tmp/foo", ".tar.gz")
    assert packagerbuddy._split_ext("/tmp/foo.tar.gz&response-content-type=application") == ("/tmp/foo", ".tar.gz")


def test_get_config_location(patch_PB_CONFIG):
    """Test getting the software configs location."""
    assert packagerbuddy.get_config_location() == os.environ["PB_CONFIG"]


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


def test_get_config(patch_PB_CONFIG):
    """Test getting the config for a valid software."""
    config = {"valid": "http://valid.com/{version}.tar"}
    assert packagerbuddy.get_config() == config


def test_install():
    pass


def test_is_software_installed(patch_PB_INSTALL):
    """Test checking whether a software is installed or not."""
    assert packagerbuddy.is_software_installed("valid", "2.0.0") is True
    assert packagerbuddy.is_software_installed("valid", "1.0.0") is True
    assert packagerbuddy.is_software_installed("valid", "0.0.0") is False


def test_get_installed_software(patch_PB_INSTALL):
    """Test getting the installed software releases."""
    install_dir = os.environ["PB_INSTALL"]
    assert packagerbuddy.get_installed_software() == [os.path.join(install_dir, "valid-1.0.0"),
                                                      os.path.join(install_dir, "valid-2.0.0")]


def test_get_suported_extensions():
    """Test getting the supported software archive extensions."""
    assert packagerbuddy.get_suported_extensions() == set([".tar", ".tar.gz", ".tar.bz"])


def test_validate_config(patch_urllib2):
    """Test validating a valid software config."""
    config = {"valid": "http://valid.com/{version}.tar"}
    packagerbuddy.validate_config(config, "valid", "1.0.0")


def test_validate_config_fail(patch_urllib2):
    """Test validating invalid software configs."""
    version = "1.0.0"

    # missing key url
    with pytest.raises(KeyError):
        packagerbuddy.validate_config({"foo": None}, "valid", version)

    # no url value
    config = {"valid": None}
    with pytest.raises(ValueError):
        packagerbuddy.validate_config(config, "valid", version)

    # url without version placeholder format
    config = {"invalid": "http://invalid.com.tar"}
    with pytest.raises(ValueError):
        packagerbuddy.validate_config(config, "invalid", version)

    # invalid url
    config = {"valid": "http://invalid.com/{version}.tar"}
    with pytest.raises(ValueError):
        packagerbuddy.validate_config(config, "valid", version)

    # invalid extension, unsupported
    config = {"valid": "http://valid.com/{version}.FOO"}
    with pytest.raises(ValueError):
        packagerbuddy.validate_config(config, "valid", version)


def test_uninstall():
    pass


def test_validate_template_url():
    """Test validating an valid download template url."""
    packagerbuddy.validate_template_url("http://test.com/{version}")


def test_validate_template_url_fail():
    """Test validating an invalid download template url."""
    with pytest.raises(ValueError):
        packagerbuddy.validate_template_url("http://test.com/")


def test_validate_software():
    """Test validating a valid software name."""
    packagerbuddy.validate_software("test")


def test_validate_software_fail():
    """Test validating an invalid software name."""
    # empty
    with pytest.raises(ValueError):
        packagerbuddy.validate_software("")

    # whitespaces
    with pytest.raises(ValueError):
        packagerbuddy.validate_software(" ")


def test_add_software(patch_PB_CONFIG):
    """Test adding a software configuration."""
    config = packagerbuddy.get_config()
    assert "test" not in config

    # add twice
    packagerbuddy.add_software("test", "http://test.com/{version}")
    packagerbuddy.add_software("test", "http://test.com/{version}")

    config = packagerbuddy.get_config()
    assert "test" in config
    assert config["test"] == "http://test.com/{version}"
    packagerbuddy.remove_software("test")


def test_remove_software(patch_PB_CONFIG):
    """Test removing a software configuration."""
    packagerbuddy.add_software("test", "http://test.com/{version}")
    config = packagerbuddy.get_config()
    assert "test" in config

    # remove twice
    packagerbuddy.remove_software("test")
    packagerbuddy.remove_software("test")

    config = packagerbuddy.get_config()
    assert "test" not in config
