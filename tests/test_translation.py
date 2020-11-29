"""Test cases for the translation module."""
import pathlib

from ihsan.schema import IhsanType
from ihsan.translation import to_sdl
from ihsan.utils import read_adfh_file

ADFH = """
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

[[adfh.fields]]
id = "my awesome status" # this id only exist in ADFH file, make unique
name = "status"
type = "choice"
options = [ "rejected", "approved", "deny",]
mandatory = "no"

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

[[adfh.models.properties]]
model = "my awesome Item"
assign = "my awesome status"


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


def create_adfh_file(*, directory_path: pathlib.PosixPath) -> None:
    """Creating temporary ADFH file."""
    (pathlib.Path(directory_path) / "adfh.toml").write_text(ADFH)


def test_to_sdl_successfully(tmp_path: pathlib.PosixPath) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path)
    data, _ = read_adfh_file(file=pathlib.Path(tmp_path) / "adfh.toml")
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
