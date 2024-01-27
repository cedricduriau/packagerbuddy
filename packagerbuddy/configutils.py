# stdlib
import json

# package
from packagerbuddy import settings


def load() -> dict[str, str]:
    with open(settings.FILE_CONFIG, "r") as fp:
        return json.load(fp)


def is_software_configured(config: dict, software: str) -> bool:
    return software in config


def add_software(config: dict, software: str, url: str) -> None:
    config[software] = url
    with open(settings.FILE_CONFIG, "w") as fp:
        json.dump(config, fp)


def remove_software(config: dict, software: str) -> None:
    config = load()
    config.pop(software)
    with open(settings.FILE_CONFIG, "w") as fp:
        json.dump(config, fp)
