# stlib
import os
from urllib.request import urlopen

# third party modules
import pytest

# package
from packagerbuddy import api


def test_get_filename_from_request(patch_url_handler):
    """Test getting the filename of an url from a request object."""
    # url with no filename in name, but in request content headers
    request = urlopen("http://valid.com")
    filename = api._get_filename_from_request(request)
    assert filename == "valid.tar"

    # url with filename in name, not in request content headers
    request = urlopen("http://filename.tar")
    filename = api._get_filename_from_request(request)
    assert filename == "filename.tar"


def test_normalize_path():
    """Test normalizing paths."""
    # ensure tilde is being resolved
    assert api._normalize_path("~/") == os.environ["HOME"]

    # ensure same level relative is being resolved
    assert api._normalize_path("/tmp/./test.txt") == "/tmp/test.txt"

    # ensure single level up relative is being resolved
    assert api._normalize_path("/tmp/dir/../test.txt") == "/tmp/test.txt"


def test_download():
    pass


def test_build_archive_name():
    """Test building the archive name of a specific software release."""
    assert api._build_archive_name("software", "version", ".ext") == "software-version.ext"


def test_get_tar_read_mode():
    """Test getting the tar file read modes."""
    assert api._get_tar_read_mode("/tmp/test.tar") == "r"
    assert api._get_tar_read_mode("/tmp/test.tar.gz") == "r:gz"
    assert api._get_tar_read_mode("/tmp/test.tar.bz2") == "r:bz2"


def test_untar():
    pass


def test_build_download_url():
    """Test building a download url."""
    api._build_download_url("http://valid.com/{version}", "1.0.0") == "http://valid.com/1.0.0"


def test_get_archive(patch_PB_DOWNLOAD):
    download_dir = os.environ["PB_DOWNLOAD"]
    assert api._get_archive("invalid", "1.0.0") is None
    archive = api._get_archive("valid", "1.0.0")
    assert archive == os.path.join(download_dir, "valid-1.0.0.tar.gz")


def test_split_ext():
    """Test splitting the extension of paths with supported extensions."""
    assert api._split_ext("/tmp/foo.tar") == ("/tmp/foo", ".tar")
    assert api._split_ext("/tmp/foo.tar.gz") == ("/tmp/foo", ".tar.gz")
    assert api._split_ext("/tmp/foo.tar.gz&response-content-type=application") == ("/tmp/foo", ".tar.gz")
    assert api._split_ext("/tmp/foo/1.2.3.tar") == ("/tmp/foo/1.2.3", ".tar")
    assert api._split_ext("/tmp/foo/1.2.3.tar.gz") == ("/tmp/foo/1.2.3", ".tar.gz")


def test_split_ext_fail():
    """Test splitting the extension of paths with unsupported extensions."""
    # no extension
    with pytest.raises(ValueError):
        api._split_ext("/tmp/foo/test")


def test_get_config_location(patch_PB_CONFIG):
    """Test getting the software configs location."""
    assert api.get_config_location() == os.environ["PB_CONFIG"]


def test_get_download_location(patch_PB_DOWNLOAD):
    """Test getting the software download location."""
    current_dir = os.path.dirname(__file__)
    expected = os.path.abspath(os.path.join(current_dir, "..", "test_source"))
    assert api.get_download_location() == expected


def test_get_install_location(patch_PB_INSTALL):
    """Test getting the software install location."""
    current_dir = os.path.dirname(__file__)
    expected = os.path.abspath(os.path.join(current_dir, "..", "test_install"))
    assert api.get_install_location() == expected


def test_get_scripts_location(patch_PB_SCRIPTS):
    """Test getting the post install scripts location."""
    current_dir = os.path.dirname(__file__)
    expected = os.path.abspath(os.path.join(current_dir, "..", "test_scripts"))
    assert api.get_scripts_location() == expected


def test_get_config(patch_PB_CONFIG):
    """Test getting the config for a valid software."""
    config = {"valid": "http://valid.com/{version}.tar"}
    assert api.get_config() == config


def test_install():
    pass


def test_is_software_installed(patch_PB_INSTALL):
    """Test checking whether a software is installed or not."""
    assert api.is_software_installed("valid", "2.0.0") is True
    assert api.is_software_installed("valid", "1.0.0") is True
    assert api.is_software_installed("valid", "0.0.0") is False


def test_get_installed_software(patch_PB_INSTALL):
    """Test getting the installed software releases."""
    install_dir = os.environ["PB_INSTALL"]
    assert api.get_installed_software() == [
        os.path.join(install_dir, "valid-1.0.0"),
        os.path.join(install_dir, "valid-2.0.0"),
    ]


def test_get_suported_extensions():
    """Test getting the supported software archive extensions."""
    assert api.get_suported_extensions() == set([".tar", ".tar.gz", ".tar.bz2", ".tgz"])


def test_validate_config(patch_url_handler):
    """Test validating a valid software config."""
    config = {"valid": "http://valid.com/{version}.tar"}
    api.validate_config(config, "valid", "1.0.0")


def test_validate_config_fail(patch_url_handler):
    """Test validating invalid software configs."""
    version = "1.0.0"

    # missing key url
    with pytest.raises(KeyError):
        api.validate_config({"foo": None}, "valid", version)

    # no url value
    config = {"valid": None}
    with pytest.raises(ValueError):
        api.validate_config(config, "valid", version)

    # url without version placeholder format
    config = {"invalid": "http://invalid.com.tar"}
    with pytest.raises(ValueError):
        api.validate_config(config, "invalid", version)

    # invalid url
    config = {"valid": "http://invalid.com/{version}.tar"}
    with pytest.raises(ValueError):
        api.validate_config(config, "valid", version)

    # invalid extension, unsupported
    config = {"valid": "http://valid.com/{version}.FOO"}
    with pytest.raises(ValueError):
        api.validate_config(config, "valid", version)


def test_uninstall():
    pass


def test_validate_template_url():
    """Test validating an valid download template url."""
    api.validate_template_url("http://test.com/{version}")


def test_validate_template_url_fail():
    """Test validating an invalid download template url."""
    with pytest.raises(ValueError):
        api.validate_template_url("http://test.com/")


def test_validate_software():
    """Test validating a valid software name."""
    api.validate_software("test")


def test_validate_software_fail():
    """Test validating an invalid software name."""
    # empty
    with pytest.raises(ValueError):
        api.validate_software("")

    # whitespaces
    with pytest.raises(ValueError):
        api.validate_software(" ")


def test_add_software(patch_PB_CONFIG):
    """Test adding a software configuration."""
    config = api.get_config()
    assert "test" not in config

    # add twice
    api.add_software("test", "http://test.com/{version}")
    api.add_software("test", "http://test.com/{version}")

    config = api.get_config()
    assert "test" in config
    assert config["test"] == "http://test.com/{version}"
    api.remove_software("test")


def test_remove_software(patch_PB_CONFIG):
    """Test removing a software configuration."""
    api.add_software("test", "http://test.com/{version}")
    config = api.get_config()
    assert "test" in config

    # remove twice
    api.remove_software("test")
    api.remove_software("test")

    config = api.get_config()
    assert "test" not in config


def test_validate_extension():
    """Test validating a valid extension."""
    api.validate_extension(".tar")
    api.validate_extension(".tar.gz")


def test_validate_extension_fail():
    """Test validating an invalid extension."""
    with pytest.raises(ValueError):
        api.validate_extension("")

    with pytest.raises(ValueError):
        api.validate_extension(".foo")


def test_get_script(patch_PB_SCRIPTS):
    """Test getting the post install scripts of software packages."""
    assert api.get_script("invalid") is None
    scripts_dir = os.environ["PB_SCRIPTS"]
    assert api.get_script("valid") == os.path.join(scripts_dir, "valid")
