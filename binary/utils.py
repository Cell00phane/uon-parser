import struct

EOL = b"\x00"

# Integer limit unsigned short
STRING_LENGTH_MAX_VALUE = 65535

DATA_TYPE_ENCODERS = {
    "float16": (16, struct.Struct("<e")),
    "float32": (32, struct.Struct("<f")),
    "float64": (64, struct.Struct("<d")),
    "int16": (16, struct.Struct("<h")),
    "int32": (32, struct.Struct("<i")),
    "int64": (64, struct.Struct("<q")),
    "uint16": (16, struct.Struct("<H")),
    "uint32": (32, struct.Struct("<I")),
    "uint64": (64, struct.Struct("<Q"))
}


def encode_string(input_string):
    """Encode the string value in binary using utf-8
    as well as its length (valuable info when decoding 
    later on). Length will be encoded as an unsigned
    short (max 65535).
    """
    input_string_encoded = input_string.encode("utf-8")
    length = len(input_string_encoded)
    length_encoded = struct.pack("<H", length)
    return length_encoded + input_string_encoded


def encode_presentation_properties(presentation_properties):
    """Encode the presentation properties

    Each presentation property has its own binary representation.
    This method will be updated as more presentation properties
    are supported.

    For example the description keyword corresponds to b"\x04"
    and the description value will be string encoded, and the whole
    will be the description presentation property encoded.

    If there are no presentation properties the empty binary string
    is returned. Otherwise it's b"\x1e" followed by the binary encoding
    of each presentation property key-value pair.

    Note: Order matters, description is encoded and then optional in this case.

    Args:
        presentation_properties (dict): the presentation properties
    Returns:
        bytes: the binary representation of the presentation
                properties.
    """
    result = b""
    if presentation_properties == {}:
        return result
    description = presentation_properties.get("description")
    if description is not None:
        result += b"\x04" + encode_string(description)
    optional = presentation_properties.get("optional")
    if optional is not None:
        result += b"\x05" + (b"\x01" if optional else b"\x00")
    return b"\x1e" + result


def decode_number(binary_input, num_type):
    precision, dtype_struct = DATA_TYPE_ENCODERS[num_type]
    number_of_bytes = int(precision/8)
    encoded_number, rest = (binary_input[:number_of_bytes],
                            binary_input[number_of_bytes:])
    return dtype_struct.unpack(encoded_number)[0], rest


def encode_number(value, num_type):
    precision, dtype_struct = DATA_TYPE_ENCODERS[num_type]
    return dtype_struct.pack(value)
