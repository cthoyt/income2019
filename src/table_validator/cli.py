# -*- coding: utf-8 -*-

"""Use tables with validation schemata to validate other tables."""

import sys
from typing import TextIO

import click

from table_validator.api import validate


@click.command()
@click.argument('template', type=click.File())
@click.argument('candidate', type=click.File())
def main(template: TextIO, candidate: TextIO):
    """Validate tables with other tables."""
    template = _parse_tsv(template)
    candidate = _parse_tsv(candidate)

    if validate(template, candidate):
        click.secho('valid', fg='green', bold=True)
        sys.exit(0)
    else:
        click.secho('invalid', fg='red')
        sys.exit(-1)


def _parse_tsv(file):
    return [
        list(line.strip().split('\t'))
        for line in file
    ]