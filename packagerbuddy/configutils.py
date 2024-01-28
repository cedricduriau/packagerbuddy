# stdlib
import json

# package
from packagerbuddy import settings


def load() -> dict[str, str]:
    with open(settings.FILE_CONFIG, "r") as fp:
        return json.load(fp)


def dump(config: dict[str, str]) -> None:
    with open(settings.FILE_CONFIG, "w") as fp:
        json.dump(config, fp, indent=True, sort_keys=True)


def is_software_configured(config: dict, software: str) -> bool:
    return software in config


def add_software(config: dict[str, str], software: str, url: str) -> None:
    config[software] = url
    dump(config)


def remove_software(config: dict[str, str], software: str) -> None:
    config.pop(software)
    dump(config)
