# -*- coding: utf-8 -*-

"""Validator classes for ``table_validator``."""

from typing import TextIO, Union

from .api import parse_tsv, validate

__all__ = [
    'TemplateValidator',
]


class TemplateValidator:
    def __init__(self, template):
        if isinstance(template, str):  # is a path
            with open(template) as file:
                self.template = parse_tsv(file)
        elif isinstance(template, list):  # is pre-parsed
            self.template = template
        elif isinstance(template, TextIO):
            self.template = parse_tsv(template)

    def validate(self, candidate: Union[list, TextIO]) -> bool:
        if isinstance(candidate, list):
            return validate(self.template, candidate)
        return validate(self.template, parse_tsv(candidate))

    def __call__(self, candidate: Union[list, TextIO]) -> bool:
        return self.validate(candidate)
