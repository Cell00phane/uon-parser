from pathlib import Path

from lark import Lark

from pprint import pprint

from transformer.uon_2_tree_transformer import UON2TreeToPython, TreeIndenter

uon_2_grammar_file = Path('grammar/uon_2_revised_grammar.lark')

test_json = """
{foo : 42,
bar: {
    hey: ho,
    boy: hood
},
l : [one, 2, three]}"""

test_uon = """
foo: 42
json:
    h:1
"""

uon_parser_2 = Lark.open(uon_2_grammar_file, parser='lalr',
                         postlex=TreeIndenter(), start='start', debug=True)


def test():
    parse_tree = uon_parser_2.parse(test_json)
    print(parse_tree.pretty(indent_str='  '))
    """ transformed = UON2TreeToPython().transform(parse_tree)
    print(transformed)
    with open("examples/Transform.txt", "w") as text_file:
        pprint(transformed, stream=text_file) """


if __name__ == '__main__':
    test()
