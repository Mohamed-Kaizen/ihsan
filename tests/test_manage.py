"""Test cases for the manage module."""
import pathlib

from typer.testing import CliRunner

from ihsan.manage import app

runner = CliRunner()


def create_adfh_file(
    *, directory_path: pathlib.PosixPath, adfh: str, file_extension: str = "toml"
) -> None:
    """Creating temporary ADFH file."""
    (pathlib.Path(directory_path) / f"adfh.{file_extension}").write_text(adfh)


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


def test_sdl_succeeds(tmp_path: pathlib.PosixPath, toml_adfh: str) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path, adfh=toml_adfh)
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
    assert "todoDetail(id: String, ): Item" in result.stdout
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


def test_sdl_output_succeeds(tmp_path: pathlib.PosixPath, toml_adfh: str) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path, adfh=toml_adfh)
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


def test_json_succeeds(
    tmp_path: pathlib.PosixPath,
    toml_adfh: str,
) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path, adfh=toml_adfh)
    data = pathlib.Path(tmp_path) / "adfh.toml"
    result = runner.invoke(app, ["json", data.as_posix()])

    assert "adfh" in result.stdout


def test_json_fail(tmp_path: pathlib.PosixPath) -> None:
    """It exits with a status code of zero."""
    data = pathlib.Path(tmp_path) / "adfh.toml"
    result = runner.invoke(app, ["json", data.as_posix()])
    assert "File doesn't exist." in result.stdout


def test_json_output_succeeds(tmp_path: pathlib.PosixPath, toml_adfh: str) -> None:
    """It exits with a status code of zero."""
    create_adfh_file(directory_path=tmp_path, adfh=toml_adfh)
    adfh_file = pathlib.Path(tmp_path) / "adfh.toml"
    sdl_output_file = pathlib.Path(tmp_path) / "test_json.json"
    runner.invoke(
        app,
        ["json", adfh_file.as_posix(), "--output", sdl_output_file.as_posix()],
        input="y\n",
    )
    assert sdl_output_file.exists() is True
