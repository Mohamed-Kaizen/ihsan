"""Test cases for the manage module."""
import pathlib

from typer.testing import CliRunner

from ihsan.manage import app

runner = CliRunner()

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


def test_help_succeeds() -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "version" in result.output


def test_version_succeeds() -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "Ihsan" in result.stdout


def test_sdl_succeeds(tmp_path: pathlib.PosixPath) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path)
    data = pathlib.Path(tmp_path) / "adfh.toml"
    result = runner.invoke(app, ["sdl", data.as_posix()])

    assert "type Item" in result.stdout
    assert "type Company" in result.stdout
    assert "title: String!" in result.stdout
    assert "id: String" in result.stdout
    assert "is_done: Boolean" in result.stdout
    assert "view: Int" in result.stdout
    assert "type Query" in result.stdout
    assert "todoList: [Item]" in result.stdout
    assert "CompanyList: [Company]" in result.stdout
    assert "type Mutation" in result.stdout
    assert "todoAdd(title: String!, ): Item" in result.stdout
    assert "companyRemove(id: String, ): Company" in result.stdout
    assert "schema" in result.stdout
    assert "query: Query" in result.stdout
    assert "mutation: Mutation" in result.stdout


def test_sdl_fail(tmp_path: pathlib.PosixPath) -> None:
    """It exits with a status code of zero."""
    data = pathlib.Path(tmp_path) / "adfh.toml"
    result = runner.invoke(app, ["sdl", data.as_posix()])
    assert "File doesn't exist." in result.stdout


def test_sdl_output_succeeds(tmp_path: pathlib.PosixPath) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path)
    adfh_file = pathlib.Path(tmp_path) / "adfh.toml"
    sdl_output_file = pathlib.Path(tmp_path) / "test_sdl.gql"
    result = runner.invoke(
        app,
        ["sdl", adfh_file.as_posix(), "--output", sdl_output_file.as_posix()],
        input="y\n",
    )
    assert (
        "Use -> https://app.graphqleditor.com/ to test the schema :)" in result.stdout
    )
    assert sdl_output_file.exists() is True
