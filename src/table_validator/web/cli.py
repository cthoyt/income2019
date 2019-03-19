# -*- coding: utf-8 -*-

"""CLI for the web interface to ``table_validator``."""

import click

from table_validator.api import parse_tsv
from table_validator.web.app import app


@click.command()
@click.option('--template', type=click.File(), default='template.tsv')
def main(template):
    """Run the web interface for the table validator."""
    app.config['table_template'] = parse_tsv(template)
    app.run(debug=True, host='0.0.0.0')
