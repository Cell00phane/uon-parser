from lark import Transformer, v_args
from lark.indenter import Indenter

from uonrevisedtypes.uon_null import UonNull
from uonrevisedtypes.uon_pair_key import UonPairKey, UonPairKeyProperties
from uonrevisedtypes.scalars.uon_float import Float64
from uonrevisedtypes.scalars.uon_integer import Integer64
from uonrevisedtypes.scalars.uon_string import UonString
from uonrevisedtypes.scalars.uon_bool import UonBoolean
from uonrevisedtypes.type_coercion import type_constructors
from uonrevisedtypes.collections.uon_dict import (
    UonMapping,
    UonDuplicateKeyError
)
from uonrevisedtypes.collections.uon_seq import UonSeq

from uonrevisedtypes.uon_custom_type import UonCustomType

from validation.properties.string.string_min_property import MinStringValidation
from validation.properties.string.string_max_property import MaxStringValidation
from validation.properties.number.number_min_property import MinNumberValidation
from validation.properties.number.number_max_property import MaxNumberValidation
from validation.types.string.string_type_validation import StringTypeValidation
from validation.types.number.int_type_validation import IntegerTypeValidation
from validation.types.number.float_type_validation import FloatTypeValidation
from validation.types.number.uint_type_validation import UintTypeValidation
from validation.types.boolean.bool_type_validation import BooleanTypeValidation
from validation.validator import Validator
from validation.schema import Schema


# TODO: multiline string as OPEN/CLOSED PAREN TYPES
class TreeIndenter(Indenter):
    NL_type = '_NL'
    OPEN_PAREN_types = ['LPAR', 'LSQB', 'LBRACE']
    CLOSE_PAREN_types = ['RPAR', 'RSQB', 'RBRACE']
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 8

# TODO: use logging
# TODO: consider using UON Dictionary throughout
class UON2RevisedTreeToPython(Transformer):
    """
    A transformer for the parse tree generated by the uon 2 revised grammar.

    Note: Transformer methods receive parse trees (instances of lark.tree.Tree)
    and decide what to do with their content. Parse trees' children consist of 
    leaves (tokens) or other trees. Leaves represent the terminals in our 
    grammar. They are wrapped in Tokens (instances of lark.lexer.Token) where 
    'Token' is a subclass of python string. So you can use usual string methods
    on them like slicing.
    """
    def __init__(self):
        '''
        We save all the schemas we have in a dictionary. Whenever 
        a custom type is encountered it is validated before that dictionary.
        '''
        super().__init__()
        self.schemas = {}

    @v_args(inline=True)
    def name(self, string):
        print("visiting name: ", string)
        (s,) = string
        return UonString(s)
        
    def escaped_string(self, s):
        print("visiting escaped string: ", s)
        # (s,) = s
        # return s[1:-1].replace('\\"', '"')
        s = ' '.join(s)
        print("joining string: ", s)
        return UonString(s)

    def string(self, string):
        print("visiting string: ", string)
        s = ' '.join(string)
        print("joining string: ", s)
        return UonString(s)

    @v_args(inline=True)
    def decimal(self, n):
        print("visiting decimal: ", n)
        return Integer64(n)

    @v_args(inline=True)
    def float_number(self, n):
        print("visiting float: ", n)
        return Float64(n)

    @v_args(inline=True)
    def signed_number(self, n):
        print("visiting float: ", n)
        return Float64(n)

    @v_args(inline=True)
    def number(self, n):
        print("visiting number: ", n)
        return n

    # TODO: Custom exceptions (for example a mapping type expected instead of seq)
    # TODO: Duplicate key exception
    def yaml_mapping(self, mapping):
        print("visiting yaml mapping: ", mapping)
        return UonMapping(
            UON2RevisedTreeToPython.to_dictionary(mapping))

    def json_mapping(self, mapping):
        print("visiting json mapping: ", mapping)
        return UonMapping(
            UON2RevisedTreeToPython.to_dictionary(mapping))

    def yaml_seq(self, seq):
        print("visiting yaml seq: ", seq)
        return UonSeq(seq)
    
    def json_seq(self, seq):
        print("visiting json seq: ", seq)
        return UonSeq(seq)

    def seq_item(self, items):
        print("visiting seq items: ", items)
        return items[0]

    @v_args(inline=True)
    def pair(self, key, value):
        """
        We receive a pair (UonPairKey, UonObject).
        Presentation properties are received as part of the UonPairKey.
        We "transfer" them to be part of the value UonObject.
        We return a pair (key, UonObject) with the key being the 
        keyname (a string) of UonPairKey.
        """
        print("visiting yaml_pair: ", key, ": ", value)
        v = value
        v.presentation_properties = key.presentation_properties
        return key.keyname, v

    @v_args(inline=True)
    def json_pair(self, key, value):
        print("visiting json pair: ", key, ": ", value)
        v = value
        v.presentation_properties = key.presentation_properties
        return key.keyname, v

    def pair_key(self, key):
        """ Will receive a list of a UonString which contains the keyname and 
        optionally a dictionary of presentation properties. UonStrings can 
        serve as keys since they are hashable but inconvenient when we 
        will have to search the dictionary.
        Thus, we extract the value from the UonString so we get a dictionary 
        with keys that are just strings and thus that are easily searchable 
        (otherwise we would have to construct a UonString object each time 
        we'd like to search the dictionary).
        """
        print("visiting pair_key: ", key)
        return UonPairKey(key[0].value, key[1] if len(key) > 1 else {})
    
    def presentation_properties(self, properties):
        """
        We will be receiving properties as a list of pairs.
        We transform the properties into a dictionary of properties names
        and their values. That way, if a certain property is repeated,
        it will keep only its last value.
        """
        print("visiting presentation_properties: ", properties, end="\n")
        return dict(properties)

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
        
    def boolean_scalar(self, boolean):
        print("Visiting boolean_scalar: ", boolean)
        return boolean[1] if len(boolean) > 1 else boolean[0]

    @v_args(inline=True)
    def coercible_scalar(self, value):
        print("visiting coercible_scalar: ", value)
        return value
    
    def typed_scalar(self, value):
        '''
        Receive a typed scalar in the form of a list ["!<TYPE>"", <VALUE>]
        We extract <TYPE> from the first element and use it to find the
        corresponding constructor to coerce the type of <VALUE>
        '''
        print("visiting typed_scalar: ", value, " with type: ", value[0])
        return_value = type_constructors[value[0][1:]](value[1].value)
        return return_value
    
    @v_args(inline=True)
    def scalar_type(self, t):
        print("visiting scalar_type: ", t)
        return t

    # ======================== VALIDATION ========================
    @v_args(inline=True)
    def json_user_type(self, custom_type, attributes):
        print("visiting json_user_type {} with attributes {}".format(
            custom_type, attributes
        ))
        custom_object = UonCustomType(custom_type, attributes)
        schema = self.schemas.get(custom_type)
        if schema is not None:
            schema.validateSchema(custom_object)
        return custom_object

    @v_args(inline=True)
    def yaml_user_type(self, custom_type, attributes):
        print("visiting yaml_user_type {} with attributes {}".format(
            custom_type, attributes
        ))
        custom_object = UonCustomType(custom_type, attributes)
        schema = self.schemas.get(custom_type)
        if schema is not None:
            schema.validateSchema(custom_object)
        return custom_object

    @v_args(inline=True)
    def schema(self, custom_type, attributes):
        print("visiting schema: {} with attributes {}"
              .format(custom_type, attributes))
        schema_ = Schema(custom_type, dict(attributes))
        self.schemas[custom_type] = schema_
        return schema_

    def attributes(self, attributes_):
        print("visiting schema attributes: ", attributes_)
        # TODO: Make attributes a dictionary here instead of in schema above
        return attributes_

    @v_args(inline=True)
    def attribute(self, attribute_, validator):
        print("visiting schema attribute: {} with validator {}"
              .format(attribute_, validator))
        validator.presentation_properties = attribute_.presentation_properties
        return (attribute_.keyname, validator)

    @v_args(inline=True)
    def attribute_name(self, attribute_name_):
        print("visiting attribute_name: ", attribute_name_)
        return attribute_name_.value

    @v_args(inline=True)
    def boolean_validation(self, bool_type):
        """
        No properties for Boolean.
        """
        print("visiting boolean validation: ", bool_type)
        return Validator(BooleanTypeValidation(), {})
    
    @v_args(inline=True)
    def string_validation(self, str_type, string_validators):
        print("visiting string_validation: ", string_validators)
        return Validator(StringTypeValidation(), string_validators)

    def string_properties(self, properties):
        print("visiting string_properties: ", properties)
        return properties

    @v_args(inline=True)
    def string_min(self, min_):
        """ Here we receive decimals """
        print("visiting string_min: ", min_)
        return MinStringValidation(min_.value)

    @v_args(inline=True)
    def string_max(self, max_):
        """ Here we receive decimals """
        print("visiting string_max: ", max_)
        return MaxStringValidation(max_.value)

    @v_args(inline=True)
    def number_validation(self, num_type, number_validators):
        print("visiting number_validation: ", num_type, " ", number_validators)
        return Validator(num_type, number_validators)

    def number_properties(self, properties):
        print("visiting number_properties: ", properties)
        return properties

    @v_args(inline=True)
    def number_min(self, min_):
        print("visiting number_min: ", min_)
        return MinNumberValidation(min_.value)

    @v_args(inline=True)
    def number_max(self, max_):
        print("visiting number_max: ", max_)
        return MaxNumberValidation(max_.value)

    def float_type(self, type_):
        return FloatTypeValidation()
    
    def int_type(self, type_):
        return IntegerTypeValidation()
    
    def uint_type(self, type_):
        return UintTypeValidation()

    # ======================== UTILITY METHODS ========================
    def supply_schemas(self, schemas):
        self.schemas.update(schemas)

    @staticmethod
    def to_dictionary(tuples_list):
        """
        Construct a dictionary out of a list of tuples.
        The 1st element of the tuple serves as key and the second
        is the value. Throws an error if a duplicate key was found.
        """
        d = {}
        for k, v in tuples_list:
            try:
                d[k]
                # If d[k] passed, then a key with the same name exists.
                raise UonDuplicateKeyError("Key {} already exists".format(k))
            except KeyError:
                # Didn't find the key in the dictionary. We can add it.
                d[k] = v
        return d



    null = lambda self, _: UonNull()
    true = lambda self, _: UonBoolean(True)
    false = lambda self, _: UonBoolean(False)
