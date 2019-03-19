# -*- coding: utf-8 -*-

"""Tests for ``table_validator``."""

import unittest
from typing import Any, List

from table_validator import validate


class TableValidatorMixin(unittest.TestCase):
    """Tests for ``table_validator``."""

    TEMPLATE: List[List[Any]]

    def assertValidCandidate(self, candidate: List[List[Any]], msg=None):
        self.assertTrue(validate(self.TEMPLATE, candidate), msg=msg)

    def assertInvalidCandidate(self, candidate: List[List[Any]], msg=None):
        self.assertFalse(validate(self.TEMPLATE, candidate), msg=msg)


class TestTableValidator(TableValidatorMixin):
    """Tests for ``table_validator``."""

    TEMPLATE = [
        ['', 'C_A', 'C_B', 'C_C'],  # Header
        ['R_1', '{INT:REQUIRED}', '{INT:REQUIRED}', '{INT:REQUIRED}'],
    ]

    def test_missing_data(self):
        self.assertInvalidCandidate([
            ['', 'C_A', 'C_B', 'C_C'],  # Header
            ['R_1', None, None, None],  # missing data
        ])

    def test_wrong_type(self):
        self.assertInvalidCandidate([
            ['', 'C_A', 'C_B', 'C_C'],  # Header
            ['R_1', 'a', 'b', 'c'],  # apparent but wrong types
        ])

    def test_passes(self):
        self.assertValidCandidate([
            ['', 'C_A', 'C_B', 'C_C'],  # Header
            ['R_1', 1, 2, 3],  # apparent but correct type
        ])


if __name__ == '__main__':
    unittest.main()
