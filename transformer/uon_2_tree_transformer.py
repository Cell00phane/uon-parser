from lark import Transformer, v_args

from uonTypes.uon_pair_key import UonPairKey, UonPairKeyProperties
from uonTypes.uon_pair import UonPair


class UON2TreeToPython(Transformer):

    @v_args(inline=True)
    def name(self, string):
        print("visiting name: ", string)
        (s,) = string
        return s

    @v_args(inline=True)
    def escaped_string(self, s):
        print("visiting escaped string: ", s)
        (s,) = s
        return s[1:-1].replace('\\"', '"')

    def string(self, string):
        print("visiting string: ", string)
        s = ' '.join(string)
        print("joining string: ", s)
        return s

    @v_args(inline=True)
    def number(self, n):
        print("visiting number: ", n)
        return n

    # TODO map should contain the pair keyname as the key and the whole
    # pair as the value, since the pair key can contain properties
    def top_map(self, mapping):
        print("visiting tree_mapping: ", mapping)
        return dict(mapping)

    def top_seq(self, seq):
        print("visiting top_seq: ", seq)
        return seq

    def seq_item(self, items):
        print("visiting seq items: ", items)
        return items[0]

    def pair(self, pair):
        print("visiting pair: ", pair)
        return pair[0].keyname, UonPair(pair[0], pair[1])

    def pair_key(self, key):
        print("visiting pair_key: ", key)
        return UonPairKey(key[0], key[1] if 1 < len(key) else None)
    
    def key_properties(self, properties):
        """
        We will be receiving properties as a list of pairs.
        We transform the properties into a dictionary of properties names
        and their values. That way, if a certain property is repeated,
        it will keep only its last value.
        """
        print("visiting key_properties: ", properties, end="\n")
        properties = dict(properties)
        description = properties.get("description")
        optional = properties.get("optional", False)
        return UonPairKeyProperties(description, optional)

    @v_args(inline=True)
    def description(self, value):
        """
        Get the description and return it as a pair
        "description" : <description>
        """
        print("visiting description: ", value)
        return "description", value

    @v_args(inline=True)
    def optional(self, value):
        """
        Get the optional value and return it as a pair
        "optional" : <optional>
        """
        print("visiting optional: ", value)
        return "optional", value
        

    null = lambda self, _: None
    true = lambda self, _: True
    false = lambda self, _: False
