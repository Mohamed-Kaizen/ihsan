"""Pytest config file."""
import pytest


@pytest.fixture
def toml_adfh() -> str:
    """Fixture for ADFH in toml."""
    return """
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


@pytest.fixture
def yaml_adfh() -> str:
    """Fixture for ADFH in yaml."""
    return """
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
  - id: my awesome status
    mandatory: 'no'
    name: status
    options:
    - rejected
    - approved
    - deny
    type: choice
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
    - assign: my awesome status
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


@pytest.fixture
def toml_adfh_without_choice() -> str:
    """Fixture for ADFH without choice in toml."""
    return """
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


@pytest.fixture
def toml_adfh_with_choice_and_without_options() -> str:
    """Fixture for ADFH in toml."""
    return """
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
options = []
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
