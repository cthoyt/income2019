# -*- coding: utf-8 -*-

"""Parse the TSV template format with PyParsing then make a new parser."""

from pyparsing import Group, MatchFirst, Optional, Suppress, delimitedList, nestedExpr, pyparsing_common as ppc

from table_validator import parse_tsv

keyword = ppc.identifier + Suppress('=') + ppc.identifier
te_keywords = nestedExpr(content=delimitedList(keyword))
te_content = ppc.identifier + Optional(te_keywords)
template_command = nestedExpr(opener='{', closer='}', content=te_content)

cell = MatchFirst([
    Group(template_command)('command'),
    Group(template_command)('command') + ppc.identifier('text'),
    ppc.identifier('text'),
])

if __name__ == '__main__':
    with open('../../tests/repeat_template.tsv') as file:
        t = [
            [
                cell.parseString(col)
                for col in row
            ]
            for row in parse_tsv(file)
        ]

    for i, row in enumerate(t):
        for j, col in enumerate(row):
            print(i, j, col.asList())
