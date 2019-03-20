# -*- coding: utf-8 -*-

"""CLI for the web interface to ``table_validator``."""

from typing import TextIO

import click

from table_validator import TemplateValidator
from table_validator.web.app import app

__all__ = [
    'main',
]


@click.command()
@click.option('--template', type=click.File(), default='template.tsv')
@click.option('--host')
@click.option('--port', type=int)
@click.option('--debug', is_flag=True)
def main(template: TextIO, host: str, port: int, debug: bool):
    """Run the web interface for the table validator."""
    app.config['table_validator'] = TemplateValidator(template)
    app.run(debug=debug, host=host, port=port)
