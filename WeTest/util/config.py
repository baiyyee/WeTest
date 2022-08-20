import yaml
import json
import logging
from configobj import ConfigObj


def to_yaml(content: dict, path: str) -> str:

    with open(path, "w") as f:
        yaml.dump(content, f)

    logging.info(f"Save to: {path}")

    return path


def to_ini(content: dict, path: str) -> str:

    config = ConfigObj(path, encoding="UTF8")

    for section, data in content.items():
        config[section] = {}

        for k, v in data.items():
            config[section][k] = v

    config.write()

    logging.info(f"Save to: {path}")

    return path


def to_json(content: dict, path: str) -> str:

    with open(path, "w") as f:
        json.dump(content, f, indent=4, ensure_ascii=False)

    logging.info(f"Save to: {path}")

    return path


def read_yaml(path_or_buffer: str, type: str = "file") -> dict:

    if type.lower() == "string":
        return yaml.load(path_or_buffer, Loader=yaml.SafeLoader)

    else:
        with open(path_or_buffer, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)


def read_ini(path: str) -> ConfigObj:

    return ConfigObj(path, encoding="UTF8")


def read_json(path: str) -> dict:

    with open(path, "r") as f:
        return json.load(f)
