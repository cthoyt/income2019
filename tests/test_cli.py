# -*- coding: utf-8 -*-

"""Tests for the CLI for ``table_validator``."""

import os
import unittest

from click.testing import CliRunner

from table_validator.cli import main

HERE = os.path.dirname(__file__)
SIMPLE_TEMPLATE = os.path.join(HERE, 'simple_template.tsv')
SIMPLE_CANDIDATE = os.path.join(HERE, 'simple_candidate.tsv')
SIMPLE_CANDIDATE_INVALID = os.path.join(HERE, 'simple_candidate_invalid.tsv')


class TestCLI(unittest.TestCase):
    """Tests for the CLI for ``table_validator``."""

    def setUp(self):
        """Set up the test case."""
        super().setUp()
        self.runner = CliRunner()

    def test_valid(self):
        """Test using the CLI to validate a passing candidate."""
        args = [SIMPLE_TEMPLATE, SIMPLE_CANDIDATE]
        result = self.runner.invoke(main, args)
        self.assertEqual(0, result.exit_code)

    def test_invalid(self):
        """Test using the CLI to validate a failing candidate."""
        args = [SIMPLE_TEMPLATE, SIMPLE_CANDIDATE_INVALID]
        result = self.runner.invoke(main, args)
        self.assertEqual(-1, result.exit_code)
