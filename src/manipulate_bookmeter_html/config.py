# Library by default
import configparser
import os
import errno

def get_config_path() -> str:
    config_path = "settings.conf"
    if not os.path.exists(config_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_path)
    return config_path

def get_config(section : str, attr : str):
    config = configparser.ConfigParser()
    config_path = get_config_path()
    config.read(config_path, encoding="utf-8")
    value = config.get(section, attr)
    if value == None:
        raise ValueError("section or attr is invalid.")
    return value

def get_config_items(section : str) -> dict:
    config = configparser.ConfigParser()
    config_path = get_config_path()
    config.read(config_path, encoding="utf-8")
    items = config.items(section)
    if items == None:
        raise ValueError("section is invalid.")
    return items
