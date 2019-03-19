# -*- coding: utf-8 -*-

"""API for ``table_validator``."""

import logging
from functools import partial
from typing import Any, Callable, Iterable, List, Tuple

import pandas as pd

logger = logging.getLogger(__name__)

EMOJI = '🔶'

DATA_TYPES = {
    'INT': int,
    'STR': str,
    'FLOAT': float,
}

Validator = Callable[[List[List[Any]], int, int], bool]


def parse_template(template) -> Iterable[Tuple[Validator, int, int]]:
    """Parse a template."""
    for i, row in enumerate(template):
        for j, cell in enumerate(row):
            if pd.isnull(cell):
                continue

            open_bracket = cell.find('{')
            if -1 == open_bracket:
                continue

            close_bracket = cell.find('}', open_bracket)
            if -1 == close_bracket:
                raise ValueError(f'ERROR in {i}, {j} {cell}: no right bracket')

            command = cell[open_bracket + 1: close_bracket]
            logger.debug(f'{EMOJI} command at ({i}, {j}): {command}')

            if command.startswith('INT'):
                yield [
                    (required_validator, i, j),
                    (int_validator, i, j),
                ]


def required_validator(candidate: List[List[Any]], row: int, column: int) -> bool:
    """Validate a cell for existence."""
    _row = candidate[row]
    return _row[column]


def type_validator(candidate: List[List[Any]], row: int, column: int, cls: type) -> bool:
    """Validate a cell for having the given type."""
    value = candidate[row][column]

    try:
        cls(value)
    except ValueError:
        return False
    else:
        return True


int_validator = partial(type_validator, cls=int)
float_validator = partial(type_validator, cls=float)


def validate(template: List[List[Any]], candidate: List[List[Any]]) -> bool:
    """Validate a candidate using a given template."""
    passed = True
    for rule in parse_template(template):
        if isinstance(rule, list):
            # multiple validations
            for validator, i, j in rule:
                if not validator(candidate, i, j):
                    print(f'failed at ({i}, {j}, {candidate[i][j]}: {validator}')
                    passed = False
                    break
        elif not rule(candidate, i, j):
            print(f'failed at ({i}, {j}, {candidate[i][j]}: {validator}')
            passed = False
    return passed
