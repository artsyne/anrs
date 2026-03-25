"""ANRS CLI entry point."""

import click
from rich.console import Console

from anrs import __version__
from anrs.init_cmd import init
from anrs.status import status
from anrs.harness_cmd import harness
from anrs.adapter import adapter

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="anrs")
def cli():
    """ANRS - AI-Native Repo Spec CLI.
    
    Initialize and manage ANRS-compliant repositories.
    """
    pass


cli.add_command(init)
cli.add_command(status)
cli.add_command(harness)
cli.add_command(adapter)


if __name__ == "__main__":
    cli()
