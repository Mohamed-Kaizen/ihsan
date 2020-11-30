# type: ignore
"""Test cases for the sdl core module."""
import pathlib

from ihsan.schema import IhsanType
from ihsan.sdl.core import to_sdl
from ihsan.utils import read_adfh_file


def create_adfh_file(
    *, directory_path: pathlib.PosixPath, adfh: str, adfh_extension: str = "toml"
) -> None:
    """Creating temporary ADFH file."""
    (pathlib.Path(directory_path) / f"adfh.{adfh_extension}").write_text(adfh)


def test_to_sdl_successfully(tmp_path: pathlib.PosixPath, toml_adfh: str) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path, adfh=toml_adfh)
    data = read_adfh_file(file=(pathlib.Path(tmp_path) / "adfh.toml").as_posix())
    ihsan_type = IhsanType(**data)
    sdl_output = to_sdl(schema=ihsan_type)

    assert "enum StatusType" in sdl_output
    assert "REJECTED" in sdl_output
    assert "APPROVED" in sdl_output
    assert "DENY" in sdl_output
    assert "type Item" in sdl_output
    assert "type Company" in sdl_output
    assert "title: String!" in sdl_output
    assert "id: String" in sdl_output
    assert "status: StatusType" in sdl_output
    assert "is_done: Boolean" in sdl_output
    assert "view: Int" in sdl_output
    assert "type Query" in sdl_output
    assert "todoList: [Item]" in sdl_output
    assert "CompanyList: [Company]" in sdl_output
    assert "todoDetail(id: String, ): Item" in sdl_output
    assert "type Mutation" in sdl_output
    assert "todoAdd(title: String!, ): Item" in sdl_output
    assert "companyRemove(id: String, ): Company" in sdl_output
    assert "schema" in sdl_output
    assert "query: Query" in sdl_output
    assert "mutation: Mutation" in sdl_output


def test_to_sdl_without_actions_successfully(
    tmp_path: pathlib.PosixPath, toml_adfh: str
) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path, adfh=toml_adfh)
    data = read_adfh_file(file=(pathlib.Path(tmp_path) / "adfh.toml").as_posix())
    data["adfh"].pop("actions")
    ihsan_type = IhsanType(**data)
    sdl_output = to_sdl(schema=ihsan_type)

    assert "enum StatusType" in sdl_output
    assert "REJECTED" in sdl_output
    assert "APPROVED" in sdl_output
    assert "DENY" in sdl_output
    assert "type Item" in sdl_output
    assert "type Company" in sdl_output
    assert "title: String!" in sdl_output
    assert "id: String" in sdl_output
    assert "status: StatusType" in sdl_output
    assert "is_done: Boolean" in sdl_output
    assert "view: Int" in sdl_output
    assert "schema" in sdl_output
    assert "query: Query" in sdl_output
    assert "mutation: Mutation" in sdl_output


def test_to_sdl_without_choice_successfully(
    tmp_path: pathlib.PosixPath, toml_adfh_without_choice: str
) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path, adfh=toml_adfh_without_choice)
    data = read_adfh_file(file=(pathlib.Path(tmp_path) / "adfh.toml").as_posix())
    ihsan_type = IhsanType(**data)
    sdl_output = to_sdl(schema=ihsan_type)

    assert "type Item" in sdl_output
    assert "type Company" in sdl_output
    assert "title: String!" in sdl_output
    assert "id: String" in sdl_output
    assert "is_done: Boolean" in sdl_output
    assert "view: Int" in sdl_output
    assert "schema" in sdl_output
    assert "query: Query" in sdl_output
    assert "mutation: Mutation" in sdl_output


def test_to_sdl_choice_without_options_successfully(
    tmp_path: pathlib.PosixPath, toml_adfh_with_choice_and_without_options: str
) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(
        directory_path=tmp_path, adfh=toml_adfh_with_choice_and_without_options
    )
    data = read_adfh_file(file=(pathlib.Path(tmp_path) / "adfh.toml").as_posix())
    ihsan_type = IhsanType(**data)
    sdl_output = to_sdl(schema=ihsan_type)

    assert "type Item" in sdl_output
    assert "type Company" in sdl_output
    assert "title: String!" in sdl_output
    assert "id: String" in sdl_output
    assert "is_done: Boolean" in sdl_output
    assert "view: Int" in sdl_output
    assert "schema" in sdl_output
    assert "query: Query" in sdl_output
    assert "mutation: Mutation" in sdl_output
