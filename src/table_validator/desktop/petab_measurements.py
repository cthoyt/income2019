# -*- coding: utf-8 -*-

"""Run to validate with PETab with ``python -m table_validator.desktop.petab_measurements``"""

import io
import logging

import click
import pandas as pd

from petab.lint import check_measurement_df
from .validation_drop_target import ValidationDropTarget, run_with_validator

logger = logging.getLogger(__name__)


class MeasurementValidationDropTarget(ValidationDropTarget):
    @staticmethod
    def preprocess_response(data):
        return pd.read_csv(io.StringIO(data), sep='\t')


def validate(df: pd.DataFrame) -> bool:
    try:
        check_measurement_df(df)
    except (AssertionError, ValueError, KeyError):
        return False
    else:
        return True


@click.command()
@click.option('-v', '--verbose', is_flag=True)
def main(verbose: bool):
    """Run the table_validator Desktop App."""
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
        logger.setLevel(logging.DEBUG)

    run_with_validator(validate=validate, cls=MeasurementValidationDropTarget)


if __name__ == '__main__':
    main()
