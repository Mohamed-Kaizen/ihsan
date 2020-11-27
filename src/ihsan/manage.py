"""Command-line interface."""
import typer
from rich.console import Console

from . import __version__

app = typer.Typer(help="Ihsan CLI.")


@app.command()
def version() -> None:
    """Show project Version."""
    console = Console()
    project_name = "Ihsan"
    console.print(f"{project_name} Version: {__version__}", style="bold green")


if __name__ == "__main__":  # pragma: no cover
    app()
