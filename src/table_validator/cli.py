# -*- coding: utf-8 -*-

"""Use tables with validation schemata to validate other tables."""

import sys
from typing import TextIO

import click

from table_validator import TemplateValidator

__all__ = [
    'main',
]


@click.command()
@click.argument('template', type=click.File())
@click.argument('candidate', type=click.File())
def main(template: TextIO, candidate: TextIO):
    """Validate tables with other tables."""
    validate = TemplateValidator(template)
    if validate(candidate):
        click.secho('valid', fg='green', bold=True)
        sys.exit(0)
    else:
        click.secho('invalid', fg='red')
        sys.exit(-1)
