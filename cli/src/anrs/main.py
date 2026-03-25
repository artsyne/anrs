"""ANRS CLI entry point."""

import click
from rich.console import Console

from anrs import __version__
from anrs.init_cmd import init
from anrs.status import status
from anrs.harness_cmd import harness
from anrs.adapter import adapter
from anrs.upgrade import upgrade
from anrs.doctor_cmd import doctor
from anrs.completion import completion

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
cli.add_command(upgrade)
cli.add_command(doctor)
cli.add_command(completion)


if __name__ == "__main__":
    cli()
