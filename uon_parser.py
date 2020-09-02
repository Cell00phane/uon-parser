from pathlib import Path
from lark import Lark

from transformer.uon_tree_transformer import (
    UonTreeToPython,
    UonIndenter
)

from serializer import python_to_uon

from binary.codec import decode_binary, decode_schema

import logging
logging.basicConfig(level=logging.DEBUG)

UON_GRAMMAR_FILE = Path('grammar/uon_grammar.lark')


"""
TODO: Specify that this project is only compatible with Python 3.x
For example the str type is used heavily in this project and is used to
represent what was both plain strings and unicode in pre-Python3. But
basestring is not available anymore in Python 3.x, str is now the type for
everything that is string in Python. If we use Python 2.x, we might get
some unexpected behavior if we encounter unicode strings.

Another example is the difference in the purposes of some built-in methods.
For example the built-in method __nonzero__ in Python2 that determines the
truth value of an object, is now simply __bool__ in Python3. Or the functioning
of other built-in methods like __eq__.

Another feature of Python3 is that dicts are now ordered as of Python 3.6.
"""


def load(input_, schemas={}, show_tree=False, debug=False):
    """Load raw UON input. Instantiates a UonParser instance and calls the corresponding
    load method. Data validation is done implicitly during tree transformation. 
    Takes an additional schemas argument and provides it to the UonParser instance,
    since this method isn't attached to a UonParser class. 

    Args:
        input_ (str): the raw UON input
        schemas (dict, optional): a dictionary of schemas to validate the input with. Defaults to {}.
        show_tree (bool, optional): flag whether to print the parse tree. Defaults to False.
        debug (bool, optional): flag whether to print out debug messages during the tree transformation. Defaults to False.

    Returns:
        Uon: The parsed and transformed Uon Python object
    """
    return UonParser(schemas=schemas).load(
        input_, show_tree=show_tree, debug=debug
    )


def load_from_file(filename, schemas={}, show_tree=False, debug=False):
    """Load UON input from file. Instantiates a UonParser instance and calls the corresponding
    load_from_file method. Data validation is done implicitly during tree transformation. 
    Takes an additional schemas argument and provides it to the UonParser instance,
    since this method isn't attached to a UonParser class.

    Args:
        filename (str): name of the UON file (path included).
        schemas (dict, optional): a dictionary of schemas to validate the input with. Defaults to {}.
        show_tree (bool, optional): flag whether to print the parse tree. Defaults to False.
        debug (bool, optional): flag whether to print out debug messages during the tree transformation. Defaults to False.

    Returns:
        Uon: The parsed and transformed Uon Python object
    """
    return UonParser(schemas=schemas).load_from_file(filename, 
                                                     show_tree=show_tree,
                                                     debug=debug)


def dump(input_):
    return UonParser().dump(input_)


def dump_to_file(input_, filename):
    UonParser().dump_to_file(input_, filename)


def validate(input_, schema_raw=None, show_tree=False, debug=False):
    parser = UonParser()

    if schema_raw is not None:
        # Schema will be saved in the parser
        parser.load(schema_raw, show_tree=show_tree, debug=debug)

    return parser.load(input_, show_tree=show_tree, debug=debug)


def to_binary(uon_input):
    """loads a raw UON input and encodes it to binary according to UON
    binary encoding specifications.

    Args:
        uon_input (str): the raw uon_input

    Returns:
        byte: UON binary encoded input
    """
    return UonParser().to_binary(uon_input)

def to_binary_from_file(filename):
    """Load UON Input from file and then encodes it to binary according
    to UON binary encoding specifications. File extension must be .uon.

    Args:
        filename (str): name of the UON file (path included).

    Returns:
        byte: UON binary encoded input
    """
    return UonParser().to_binary_from_file(filename)


def from_binary(binary_input, schemas={}):
    """Decodes a UON encoded bytestring.

    Args:
        binary_input (byte): bytestring of UON input
        schemas (dict, optional): provide the UonParser with schemas, to 
                                  validate user types. Defaults to {}.

    Returns:
        Uon: decoded Uon object
    """
    return UonParser(schemas).from_binary(binary_input)


class UonParser:
    """ A parser for Uon. The parser saves all the schemas that it parses,
    for validation on further inputs.

    You should use this class if you want to hold on to the schemas that you
    provide it using load_schema() or schema_from_binary().
    These schemas will be used to validate further uon inputs
    automatically.
    """
    def __init__(self, schemas={}):
        self.parser = Lark.open(UON_GRAMMAR_FILE, parser='lalr',
                                postlex=UonIndenter(),
                                maybe_placeholders=True, start='start')
        self.transformer = UonTreeToPython()
        self.schemas = schemas

    def load(self, input_, show_tree=False, debug=False):
        """Load raw UON input. Data validation is done implicitly during tree transformation.

        Args:
            input_ (str): the raw UON input
            show_tree (bool, optional): flag whether to print the parse tree. Defaults to False.
            debug (bool, optional): flag whether to print out debug messages during the tree transformation. Defaults to False.

        Returns:
            Uon: The parsed and transformed Uon Python object
        """
        parse_tree = self.parser.parse(input_)
        if show_tree:
            logging.debug(parse_tree.pretty(indent_str=" "))
        self.transformer.debug = debug
        transformed = self.transformer.transform(parse_tree)

        # Revert transformer debug back to default
        self.transformer.debug = False
        return transformed

    def load_from_file(self, filename, show_tree=False, debug=False):
        """Load UON Input from file. File extension must be .uon.

        Args:
            filename (str): name of the UON file (path included).
            show_tree (bool, optional): flag whether to print the parse tree. Defaults to False.
            debug (bool, optional): flag whether to print out debug messages during the tree transformation. Defaults to False.

        Raises:
            ValueError: Not a valid .uon file

        Returns:
            Uon: The parsed from file and transformed Uon Python object
        """
        if not filename.endswith(".uon"):
            raise ValueError("Not a .uon file")
        with open(filename) as f:
            read_data = f.read()
            return self.load(read_data, show_tree=show_tree, debug=debug)

    def load_schema(self, schema_raw, show_tree=False, debug=False):
        """Same as load() except for schemas. However there is no verification
        that the input is actually a schema. You can use normal load() to 
        parse and add schemas as well.

        Args:
            schema_raw ([type]): [description]
            show_tree (bool, optional): [description]. Defaults to False.
            debug (bool, optional): [description]. Defaults to False.

        Returns:
            [type]: [description]
        """
        schema = self.load(schema_raw, show_tree=show_tree, debug=debug)
        self.schemas[schema.type_] = schema
        return schema

    def load_schema_from_file(self, filename, show_tree=False, debug=False):
        if not filename.endswith(".uon"):
            raise ValueError("Not a .uon file")
        with open(filename) as f:
            read_data = f.read()
            return self.load_schema(read_data, show_tree=show_tree,
                                    debug=debug)

    def dump(self, input_):
        return python_to_uon(input_)

    def dump_to_file(self, input_, filename):
        if not filename.endswith(filename):
            filename += ".uon"
        with open(filename, "w") as file_stream:
            file_stream.write(self.dump(input_))

    def to_binary(self, uon_input):
        """loads a raw UON input and encodes it to binary according to UON
        binary encoding specifications.

        Args:
            uon_input (str): the raw uon_input

        Returns:
            byte: UON binary encoded input
        """
        parsed_uon = self.load(uon_input)
        return parsed_uon.to_binary()
    
    def to_binary_from_file(self, filename):
        """Load UON Input from file and then encodes it to binary according
        to UON binary encoding specifications. File extension must be .uon.

        Args:
            filename (str): name of the UON file (path included).

        Returns:
            byte: UON binary encoded input
        """
        if not filename.endswith(".uon"):
            raise ValueError("Not a .uon file")
        with open(filename) as f:
            read_data = f.read()
            return self.to_binary(read_data)

    def from_binary(self, binary_input):
        """Decodes a UON encoded bytestring.

        Args:
            binary_input (byte): bytestring of UON input

        Returns:
            Uon: decoded Uon object
        """
        return decode_binary(binary_input, schemas=self.schemas)

    def schema_from_binary(self, binary_schema):
        schema = decode_schema(binary_schema)
        self.schemas[schema.type_] = schema
        return schema
