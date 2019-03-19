# -*- coding: utf-8 -*-

"""Tests for ``table_validator``."""

import unittest
from typing import Any, List

from table_validator import validate

simple_template = [
    ['', 'C_A', 'C_B', 'C_C'],  # Header
    ['R_1', '{INT:REQUIRED}', '{INT:REQUIRED', '{INT:REQUIRED}'],
]


class TestTableValidator(unittest.TestCase):
    """Tests for ``table_validator``."""

    def assertValidCandidate(self, candidate: List[List[Any]], msg=None):
        self.assertTrue(validate(simple_template, candidate), msg=msg)

    def assertInvalidCandidate(self, candidate: List[List[Any]], msg=None):
        self.assertFalse(validate(simple_template, candidate), msg=msg)

    def test_missing_data(self):
        candidate = [
            ['', 'C_A', 'C_B', 'C_C'],  # Header
            ['R_1', None, None, None],  # missing data
        ]
        self.assertInvalidCandidate(candidate)

    def test_wrong_type(self):
        candidate = [
            ['', 'C_A', 'C_B', 'C_C'],  # Header
            ['R_1', 'a', 'b', 'c'],  # apparent but wrong types
        ]
        self.assertInvalidCandidate(candidate)

    def test_passes(self):
        candidate = [
            ['', 'C_A', 'C_B', 'C_C'],  # Header
            ['R_1', 1, 2, 3],  # apparent but correct type
        ]
        self.assertValidCandidate(candidate)


if __name__ == '__main__':
    unittest.main()
