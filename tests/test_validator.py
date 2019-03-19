# -*- coding: utf-8 -*-

"""Tests for ``table_validator``."""

import unittest
from typing import Any, List

from table_validator import validate


class TableValidatorMixin(unittest.TestCase):
    """Tests for ``table_validator``."""

    TEMPLATE: List[List[Any]]

    def assertValidCandidate(self, candidate: List[List[Any]], msg=None):  # noqa:N802
        """Assert that the given candidate passes validation against the template."""
        self.assertTrue(validate(self.TEMPLATE, candidate), msg=msg)

    def assertInvalidCandidate(self, candidate: List[List[Any]], msg=None):  # noqa:N802
        """Assert that the given candidate does not pass validation against the template."""
        self.assertFalse(validate(self.TEMPLATE, candidate), msg=msg)


class TestSimpleValidator(TableValidatorMixin):
    """Tests for ``table_validator``."""

    TEMPLATE = [
        ['', 'C_A', 'C_B', 'C_C'],  # Header
        ['R_1', '{INT:REQUIRED}', '{INT:REQUIRED}', '{INT:REQUIRED}'],
    ]

    def test_missing_data(self):
        """Test when required data is missing."""
        self.assertInvalidCandidate([
            ['', 'C_A', 'C_B', 'C_C'],  # Header
            ['R_1', 1, None, None],  # missing data
        ])
        self.assertInvalidCandidate([
            ['', 'C_A', 'C_B', 'C_C'],  # Header
            ['R_1', None, 1, None],  # missing data
        ])
        self.assertInvalidCandidate([
            ['', 'C_A', 'C_B', 'C_C'],  # Header
            ['R_1', None, None, 1],  # missing data
        ])
        self.assertInvalidCandidate([
            ['', 'C_A', 'C_B', 'C_C'],  # Header
            ['R_1', None, None, None],  # missing data
        ])

    def test_wrong_type(self):
        """Test when data is apparent but has the wrong type."""
        self.assertInvalidCandidate([
            ['', 'C_A', 'C_B', 'C_C'],
            ['R_1', 'a', 'b', 'c'],
        ])

    def test_passes(self):
        """Test data that is apparent and has the correct type."""
        self.assertValidCandidate([
            ['', 'C_A', 'C_B', 'C_C'],  # Header
            ['R_1', 1, 2, 3],  # apparent but correct type
        ])


class TestRepeatValidator(TableValidatorMixin):
    """Tests for ``table_validator``."""

    TEMPLATE = [
        ['', 'C_A', 'C_B', 'C_C'],  # Header
        ['{REPEAT_ROW}R', '{INT(REQUIRED=TRUE)}', '{INT(REQUIRED=TRUE)}', '{INT(REQUIRED=TRUE)}'],
        ['R_X', '{INT:REQUIRED}', '{INT:REQUIRED}', '{INT:REQUIRED}'],
    ]

    def test_no_repeat(self):
        """Test when a repeat is not used."""
        self.assertValidCandidate([
            ['', 'C_A', 'C_B', 'C_C'],  # Header
            ['R_1', 1, 2, 3],  # apparent but correct type
        ])

    def test_repeat_once(self):
        """Test when a repeat is only used once."""
        self.assertValidCandidate([
            ['', 'C_A', 'C_B', 'C_C'],  # Header
            ['R', 1, 2, 3],
            ['R_X', 7, 8, 9],
        ])

    def test_repeat_twice(self):
        """Test when a repeat is used multiple times."""
        self.assertValidCandidate([
            ['', 'C_A', 'C_B', 'C_C'],  # Header
            ['R', 1, 2, 3],
            ['R', 4, 5, 6],
            ['R_X', 7, 8, 9],
        ])

    def test_missing_data(self):
        """Test when a repeat is used but a validation error occurs within."""
        self.assertInvalidCandidate([
            ['', 'C_A', 'C_B', 'C_C'],  # Header
            ['R', 1, 2, 3],
            ['R', 4, None, 6],
            ['R_X', 7, 8, 9],  # missing data
        ])
        self.assertInvalidCandidate([
            ['', 'C_A', 'C_B', 'C_C'],  # Header
            ['R', 1, 2, 3],
            ['R', 4, 5, 6],
            ['R_X', 7, None, 9],  # missing data
        ])


if __name__ == '__main__':
    unittest.main()
