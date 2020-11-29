"""Test cases for the utils module."""
import pathlib

from ihsan.schema import IhsanType
from ihsan.utils import find_action, find_field, find_model, read_adfh_file

TOML_ADFH = """
[adfh]
version = "1.0"

[[adfh.extra]]
type = "metadata"
name = "name"
value = "todo"
tags = ["oas"]

[[adfh.extra]]
type = "metadata"
name = "title"
value = "ToDo API"
tags = ["oas", "user"]

[[adfh.fields]] # It the same as fields in class, database, Rest API, Graphql, etc....
id = "my awesome id" # this id only exist in ADFH file, make unique
name = "id"
type = "unique id"
mandatory = "no"
text = "A unique for a todo"

[[adfh.fields]]
id = "my awesome title" # this id only exist in ADFH file, make unique
name = "title"
type = "text"
mandatory = "yes"
text = "The title of a todo"

[[adfh.fields]]
id = "my second awesome is done" # this id only exist in ADFH file, make unique
name = "is_done"
type = "checkbox"
mandatory = "no"

#[[adfh.fields]]
#id = "my awesome status" # this id only exist in ADFH file, make unique
#name = "status"
#type = "choice"
#options = [ "rejected", "approved", "deny",]
#mandatory = "no"

[[adfh.fields]]
id = "my awesome view" # this id only exist in ADFH file, make unique
name = "view"
type = "number"
mandatory = "no"
text = "count number of poeple that saw the todo"

[[adfh.models]] # It the same as recored, class, database model, etc....
id = "my awesome Item" # this id only exist in ADFH file, make unique
name = "Item"
text = "A todo item"

[[adfh.models.properties]] # It the same as class, rest api fields, etc....
model = "my awesome Item" # Telling that this property is blong to a model X.
assign = "my awesome id" # Assign the field for the model from adfh.fields.

[[adfh.models.properties]]
model = "my awesome Item"
assign = "my awesome title"

[[adfh.models]] # It the same as recored, class, database model, etc....
id = "my awesome Company" # this id only exist in ADFH file, make unique
name = "Company"
text = "A Company"

[[adfh.models.properties]] # It the same as class, rest api fields, etc....
model = "my awesome Company"
assign = "my second awesome is done"

[[adfh.models.properties]]
model = "my awesome Company"
assign = "my awesome view"

[[adfh.actions]] # Operations
id = "my awesome list of todo" # this id only exist in ADFH file, make unique
name = "todoList"
type = "show me list"  # Telling what kind of operation.
model = "my awesome Item" # Telling that this property is blong to a model X.
text = "list todo items"
tags = ["oas"]

[[adfh.actions]]
id = "my awesome list of company" # this id only exist in ADFH file, make unique
name = "CompanyList"
type = "show me list"
model = "my awesome Company"
text = "list of Company"
tags = ["oas"]

[[adfh.actions]]
id = "my awesome todo" # this id only exist in ADFH file, make unique
name = "todoDetail"
type = "show me a certain item"
model = "my awesome Item"
subject = "my awesome id"  # Telling to search with this field or lookup by that field. Note the field should be inside the model # noqa B950
text = "show the detail of a todo."
tags = ["oas"]

[[adfh.actions]]
id = "my awesome add todo" # this id only exist in ADFH file, make unique
name = "todoAdd"
type = "let me add"
model = "my awesome Item"
text = "creating new todo."
tags = ["oas"]

[[adfh.actions.input]]
action = "my awesome add todo"
assign = "my awesome title"

[[adfh.actions]]
id = "my awesome remove company" # this id only exist in ADFH file, make unique
name = "companyRemove"
type = "let me remove"
model = "my awesome Company"
subject = "my awesome id"
text = "removing a company."
tags = ["oas"]
"""

YAML_ADFH = """
adfh:
  actions:
  - id: my awesome list of todo
    model: my awesome Item
    name: todoList
    tags:
    - oas
    text: list todo items
    type: show me list
  - id: my awesome list of company
    model: my awesome Company
    name: CompanyList
    tags:
    - oas
    text: list of Company
    type: show me list
  - id: my awesome todo
    model: my awesome Item
    name: todoDetail
    subject: my awesome id
    tags:
    - oas
    text: show the detail of a todo.
    type: show me a certain item
  - id: my awesome add todo
    input:
    - action: my awesome add todo
      assign: my awesome title
    model: my awesome Item
    name: todoAdd
    tags:
    - oas
    text: creating new todo.
    type: let me add
  - id: my awesome remove company
    model: my awesome Company
    name: companyRemove
    subject: my awesome id
    tags:
    - oas
    text: removing a company.
    type: let me remove
  extra:
  - name: name
    tags:
    - oas
    type: metadata
    value: todo
  - name: title
    tags:
    - oas
    - user
    type: metadata
    value: ToDo API
  fields:
  - id: my awesome id
    mandatory: 'no'
    name: id
    text: A unique for a todo
    type: unique id
  - id: my awesome title
    mandatory: 'yes'
    name: title
    text: The title of a todo
    type: text
  - id: my second awesome is done
    mandatory: 'no'
    name: is_done
    type: checkbox
  - id: my awesome view
    mandatory: 'no'
    name: view
    text: count number of poeple that saw the todo
    type: number
  models:
  - id: my awesome Item
    name: Item
    properties:
    - assign: my awesome id
      model: my awesome Item
    - assign: my awesome title
      model: my awesome Item
    text: A todo item
  - id: my awesome Company
    name: Company
    properties:
    - assign: my second awesome is done
      model: my awesome Company
    - assign: my awesome view
      model: my awesome Company
    text: A Company
  version: '1.0'
"""


def create_adfh_file(
    *,
    directory_path: pathlib.PosixPath,
    file_extension: str = "toml",
    adfh_text: str = TOML_ADFH,
) -> None:
    """Creating temporary ADFH file."""
    (pathlib.Path(directory_path) / f"adfh.{file_extension}").write_text(adfh_text)


def test_read_adfh_toml_file_successfully(tmp_path: pathlib.PosixPath) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path)
    data, is_error = read_adfh_file(file=pathlib.Path(tmp_path) / "adfh.toml")
    assert is_error is False
    assert type(data) == dict


def test_read_adfh_yaml_file_successfully(tmp_path: pathlib.PosixPath) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(
        directory_path=tmp_path, file_extension="yaml", adfh_text=YAML_ADFH
    )
    data, is_error = read_adfh_file(file=pathlib.Path(tmp_path) / "adfh.yaml")
    assert is_error is False
    assert type(data) == dict


def test_read_adfh_toml_file_fail(tmp_path: pathlib.PosixPath) -> None:
    """It exits with a status code of zero."""
    data, is_error = read_adfh_file(file=pathlib.Path(tmp_path) / "adfh_file.toml")
    assert is_error is True
    assert type(data) == str
    assert data == "File doesn't exist."


def test_read_adfh_yaml_file_fail(tmp_path: pathlib.PosixPath) -> None:
    """It exits with a status code of zero."""
    data, is_error = read_adfh_file(file=pathlib.Path(tmp_path) / "adfh_file.yaml")
    assert is_error is True
    assert type(data) == str
    assert data == "File doesn't exist."


def test_read_adfh_txt_file_fail(tmp_path: pathlib.PosixPath) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path, file_extension="txt")
    data, is_error = read_adfh_file(file=pathlib.Path(tmp_path) / "adfh.txt")
    assert is_error is True
    assert type(data) == str
    assert data == "You can only pick toml or yaml file."


def test_find_action_successfully(tmp_path: pathlib.PosixPath) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path)
    data, _ = read_adfh_file(file=pathlib.Path(tmp_path) / "adfh.toml")
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


def test_find_action_fail(tmp_path: pathlib.PosixPath) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path)
    data, _ = read_adfh_file(file=pathlib.Path(tmp_path) / "adfh.toml")
    ihsan_type = IhsanType(**data)
    action = find_action(actions=ihsan_type.adfh.actions, keyword="list view")

    assert action == []


def test_find_field_successfully(tmp_path: pathlib.PosixPath) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path)
    data, _ = read_adfh_file(file=pathlib.Path(tmp_path) / "adfh.toml")
    ihsan_type = IhsanType(**data)
    field = find_field(fields=ihsan_type.adfh.fields_list, field_id="my awesome id")
    assert field.id == "my awesome id"
    assert field.name == "id"
    assert field.type == "String"
    assert field.mandatory == ""
    assert field.options is None
    assert field.text is None


def test_find_field_fail(tmp_path: pathlib.PosixPath) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path)
    data, _ = read_adfh_file(file=pathlib.Path(tmp_path) / "adfh.toml")
    ihsan_type = IhsanType(**data)
    field = find_field(fields=ihsan_type.adfh.fields_list, field_id="my not awesome id")
    assert "loc" in field
    assert "id" in field
    assert "name" in field
    assert "type" in field


def test_find_model_successfully(tmp_path: pathlib.PosixPath) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path)
    data, _ = read_adfh_file(file=pathlib.Path(tmp_path) / "adfh.toml")
    ihsan_type = IhsanType(**data)
    model = find_model(models=ihsan_type.adfh.models, model_id="my awesome Item")
    assert model.id == "my awesome Item"
    assert model.name == "Item"


def test_find_model_fail(tmp_path: pathlib.PosixPath) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path)
    data, _ = read_adfh_file(file=pathlib.Path(tmp_path) / "adfh.toml")
    ihsan_type = IhsanType(**data)
    model = find_model(models=ihsan_type.adfh.models, model_id="my not awesome Item")
    assert "loc" in model
    assert "id" in model
    assert "name" in model
    assert "type" in model
