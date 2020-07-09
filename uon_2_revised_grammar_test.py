from pathlib import Path

from lark import Lark

from pprint import pprint

from transformer.uon_2_revised_tree_transformer import (
    UON2RevisedTreeToPython,
    TreeIndenter
)

from uonrevisedtypes.uon_custom_type import UonCustomType
from uonrevisedtypes.scalars.uon_uint import Uint64

uon_2_grammar_file = Path('grammar/uon_2_revised_grammar.lark')

test_true_false = """
old: !bool false
young(optional : false): true
old: true
"""

test_json = """
{foo : 42,
bar: {
    hey: ho,
    boy: hood
},
l : [one, 2, three]}
"""

test_uon_simple = """
foo (description: "A foo", optional: true): 42
h : 1
"""

test_uon = """
foo (description: "A foo", optional: true): 42
nested (description: "A dictionary"):
    h:1
"""

test_schema = """
!!person: schema {
    name(description: name of the person, optional: false): !str(min:3, max:25),
    age: !uint(min: 0, max: 125),
    minor: !bool
}
"""

test_schema_validation = """
{p: !!person {
        name: stephane,
        age: 25,
        minor: false
    }
}
"""

test_schema_validation_yaml = """
p: !!person
  name: stephane
  age: 25
"""

uon_parser_2 = Lark.open(uon_2_grammar_file, parser='lalr',
                         postlex=TreeIndenter(), start='start', debug=True)


def test():
    parse_tree = uon_parser_2.parse(test_schema_validation)
    print(parse_tree.pretty(indent_str='  '))
    transformed = UON2RevisedTreeToPython().transform(parse_tree)
    print(transformed)
    with open("examples/Transform.txt", "w") as text_file:
        pprint(transformed, stream=text_file)

    """ schema = transformed
    schema.validateSchema(UonCustomType(
        "person",
        {"name": "Guy", "age": Uint64(120)})) """


if __name__ == '__main__':
    test()
