# type: ignore
"""Test cases for the sdl utils module."""
import pathlib

import pytest
from pydantic import ValidationError

from ihsan.schema import IhsanType
from ihsan.sdl.utils import (
    find_action,
    find_field,
    find_model,
    get_all_field_with_certain_type,
)
from ihsan.utils import read_adfh_file


def create_adfh_file(
    *, directory_path: pathlib.PosixPath, adfh: str, adfh_extension: str = "toml"
) -> None:
    """Creating temporary ADFH file."""
    (pathlib.Path(directory_path) / f"adfh.{adfh_extension}").write_text(adfh)


# type: ignore
def test_find_action_successfully(tmp_path: pathlib.PosixPath, toml_adfh: str) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path, adfh=toml_adfh)
    data = read_adfh_file(file=(pathlib.Path(tmp_path) / "adfh.toml").as_posix())
    ihsan_type = IhsanType(**data)
    list_action = find_action(actions=ihsan_type.adfh.actions, keyword="show me list")
    remove_action = find_action(
        actions=ihsan_type.adfh.actions, keyword="let me remove"
    )
    add_action = find_action(actions=ihsan_type.adfh.actions, keyword="let me add")
    detail_action = find_action(
        actions=ihsan_type.adfh.actions, keyword="show me a certain item"
    )

    assert type(list_action) == list
    assert type(remove_action) == list
    assert type(add_action) == list
    assert type(detail_action) == list
    assert len(list_action) == 2
    assert len(remove_action) == 1
    assert len(add_action) == 1
    assert len(detail_action) == 1


def test_find_action_fail(tmp_path: pathlib.PosixPath, toml_adfh: str) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path, adfh=toml_adfh)
    data = read_adfh_file(file=(pathlib.Path(tmp_path) / "adfh.toml").as_posix())
    ihsan_type = IhsanType(**data)
    action = find_action(actions=ihsan_type.adfh.actions, keyword="list view")

    assert action == []


def test_find_field_successfully(tmp_path: pathlib.PosixPath, toml_adfh: str) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path, adfh=toml_adfh)
    data = read_adfh_file(file=(pathlib.Path(tmp_path) / "adfh.toml").as_posix())
    ihsan_type = IhsanType(**data)
    field = find_field(fields=ihsan_type.adfh.fields_list, field_id="my awesome id")
    assert field.id == "my awesome id"
    assert field.name == "id"
    assert field.type == "String"
    assert field.mandatory == ""
    assert field.options is None
    assert field.text is None


def test_find_field_fail(tmp_path: pathlib.PosixPath, toml_adfh: str) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path, adfh=toml_adfh)
    data = read_adfh_file(file=(pathlib.Path(tmp_path) / "adfh.toml").as_posix())
    ihsan_type = IhsanType(**data)
    with pytest.raises(ValidationError):
        assert find_field(
            fields=ihsan_type.adfh.fields_list, field_id="my not awesome id"
        )


def test_get_all_field_with_certain_type_successfully(
    tmp_path: pathlib.PosixPath, toml_adfh: str
) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path, adfh=toml_adfh)
    data = read_adfh_file(file=(pathlib.Path(tmp_path) / "adfh.toml").as_posix())
    ihsan_type = IhsanType(**data)
    fields = get_all_field_with_certain_type(
        fields=ihsan_type.adfh.fields_list, keyword="choice"
    )

    assert type(fields) == list
    assert fields[0].id == "my awesome status"
    assert fields[0].name == "status"
    assert fields[0].type == "choice"
    assert fields[0].options == ["rejected", "approved", "deny"]
    assert fields[0].mandatory == "no"


def test_get_all_field_with_certain_type_fail(
    tmp_path: pathlib.PosixPath, toml_adfh: str
) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path, adfh=toml_adfh)
    data = read_adfh_file(file=(pathlib.Path(tmp_path) / "adfh.toml").as_posix())
    ihsan_type = IhsanType(**data)
    fields = get_all_field_with_certain_type(
        fields=ihsan_type.adfh.fields_list, keyword="not choice"
    )

    assert fields == []


def test_find_model_successfully(tmp_path: pathlib.PosixPath, toml_adfh: str) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path, adfh=toml_adfh)
    data = read_adfh_file(file=(pathlib.Path(tmp_path) / "adfh.toml").as_posix())
    ihsan_type = IhsanType(**data)
    model = find_model(models=ihsan_type.adfh.models, model_id="my awesome Item")
    assert model.id == "my awesome Item"
    assert model.name == "Item"


def test_find_model_fail(tmp_path: pathlib.PosixPath, toml_adfh: str) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path, adfh=toml_adfh)
    data = read_adfh_file(file=(pathlib.Path(tmp_path) / "adfh.toml").as_posix())
    ihsan_type = IhsanType(**data)
    with pytest.raises(ValidationError):
        assert find_model(models=ihsan_type.adfh.models, model_id="my not awesome Item")
