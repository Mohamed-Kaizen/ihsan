"""Collection of utils."""
import pathlib
from typing import Dict, Tuple, Union

import toml
import yaml


def read_adfh_file(file: str) -> Tuple[Union[Dict, str], bool]:
    """Parse an ADFH file into dict."""
    file_path = pathlib.Path(file)
    file_name, file_extension = file_path.name.rsplit(".")

    if file_path.exists() and file_path.is_file():

        if file_extension in ["yaml", "yml"]:
            with open(file_path, "r") as f:
                data = yaml.safe_load(f)
            return data, False

        elif file_extension == "toml":
            data = toml.load(f"{file_path}")
            return data, False
        else:
            return "You can only pick toml or yaml file.", True
    return "File doesn't exist.", True
