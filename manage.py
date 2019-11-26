#!/usr/bin/env python
import click
from click.core import Command

from cermin.libs.misc import walk_modules


@click.group()
def cli():
    pass


for modules in walk_modules("soccer.commands"):
    for obj in vars(modules).values():
        if isinstance(obj, Command):
            cli.add_command(obj)

if __name__ == "__main__":
    cli()