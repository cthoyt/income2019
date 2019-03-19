# -*- coding: utf-8 -*-

"""Use tables with validation schemata to validate other tables."""

from typing import TextIO

import click
import pandas as pd

from table_validator.api import parse_template


@click.command()
@click.argument('template', type=click.File())
@click.option('-c', '--candidate', type=click.File())
def main(template: TextIO, candidate: TextIO):
    """Validate tables with other tables."""
    click.echo(f'Template: {template.name}')
    df = pd.read_csv(template, sep='\t', header=None)

    template = df.values
    list(parse_template(template))

    if candidate:
        click.echo(f'Candidate: {candidate.name}')
