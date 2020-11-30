"""Test cases for the utils module."""
import pathlib

from ihsan.utils import read_adfh_file


def create_adfh_file(
    *, directory_path: pathlib.PosixPath, adfh: str, file_extension: str = "toml"
) -> None:
    """Creating temporary ADFH file."""
    (pathlib.Path(directory_path) / f"adfh.{file_extension}").write_text(adfh)


def test_read_adfh_toml_file_successfully(
    tmp_path: pathlib.PosixPath, toml_adfh: str
) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path, adfh=toml_adfh)
    data = read_adfh_file(file=(pathlib.Path(tmp_path) / "adfh.toml").as_posix())
    assert type(data) == dict


def test_read_adfh_yaml_file_successfully(
    tmp_path: pathlib.PosixPath, yaml_adfh: str
) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path, file_extension="yaml", adfh=yaml_adfh)
    data = read_adfh_file(file=(pathlib.Path(tmp_path) / "adfh.yaml").as_posix())
    assert type(data) == dict


def test_read_adfh_toml_file_fail(tmp_path: pathlib.PosixPath, toml_adfh: str) -> None:
    """It exits with a status code of zero."""
    data = read_adfh_file(file=(pathlib.Path(tmp_path) / "adfh_file.toml").as_posix())
    assert type(data) == str
    assert data == "File doesn't exist."


def test_read_adfh_yaml_file_fail(tmp_path: pathlib.PosixPath, yaml_adfh: str) -> None:
    """It exits with a status code of zero."""
    data = read_adfh_file(file=(pathlib.Path(tmp_path) / "adfh_file.yaml").as_posix())
    assert type(data) == str
    assert data == "File doesn't exist."


def test_read_adfh_txt_file_fail(tmp_path: pathlib.PosixPath, toml_adfh: str) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path, adfh=toml_adfh, file_extension="txt")
    data = read_adfh_file(file=(pathlib.Path(tmp_path) / "adfh.txt").as_posix())
    assert type(data) == str
    assert data == "You can only pick toml or yaml file."
