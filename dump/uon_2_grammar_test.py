from pathlib import Path

from lark import Lark

from pprint import pprint

from transformer.uon_2_tree_transformer import UON2TreeToPython, TreeIndenter

uon_2_grammar_file = Path('grammar/old/uon_2_grammar.lark')

test_uon = """
a (description : A key) : d
b : 28
c : f
"""

test_grammar_nested_mappings_in_seq = """
-
  name: Mark McGwire
  hr:   65
  avg:  0.278
-
  name: Sammy Sosa
  hr:   63
  avg:  0.288
"""

test_uon_strings = """
a : !!str 28.5 I put numbers 28.5 or -28.5 in my string but this should still be parsed as a string
b : -28.5
c : 
    - 28
    - -28.5
"""

test_strings = """
a : 28 should be parsed as string
b : 28
"""

test_escaped_strings = """
'a' : 28 should be parsed as string
"b" : 28
"""

test_type_coercion = """
a : !!int64 5.876
"""

test_type_coercion_to_integer = """
a : !!int32 !!float64 58767638927.4
"""

# TODO: keep the types maybe?
test_successive_types = """
a : !!str !!int32 !!float64 !!int32 5
b (description : "No type"): 5
c :
    d : !!int64 !!float32 63.7
    e : !!str 2.0
"""

uon_parser_2 = Lark.open(uon_2_grammar_file, parser='lalr',
                         postlex=TreeIndenter(), start='start', debug=True)


def test():
    parse_tree = uon_parser_2.parse(test_uon)
    print(parse_tree.pretty(indent_str='  '))
    transformed = UON2TreeToPython().transform(parse_tree)
    print(transformed)
    with open("examples/Transform.txt", "w") as text_file:
        pprint(transformed, stream=text_file)


if __name__ == '__main__':
    test()
