import struct

from uonrevisedtypes.scalars.uon_bool import UonBoolean
from uonrevisedtypes.scalars.uon_float import (
    Float32, Float64, Float128
)
from uonrevisedtypes.scalars.uon_uint import (
    Uint32, Uint64, Uint128
)
from uonrevisedtypes.scalars.uon_string import UonString

from binary.codec import decode_binary

# We use < since numpy byte encoding is little-endian.
float32_struct = struct.Struct("<f")
float64_struct = struct.Struct("<d")
int32_struct = struct.Struct("<i")
int64_struct = struct.Struct("<q")
uint32_struct = struct.Struct("<I")
uint64_struct = struct.Struct("<Q")
char_struct = struct.Struct("<b")

# ============================== ENCODING ==============================


class TestUonEncoding:
    def test_bool_to_binary(self):
        b = UonBoolean(True)
        assert b.to_binary() == b"\x14\x01"
        b = UonBoolean(False)
        assert b.to_binary() == b"\x14\x00"

    def test_float_to_binary(self):
        test_value = 64.0
        f = Float64(test_value)
        assert f.to_binary() == b"\x24" + float64_struct.pack(test_value)
        f = Float32(test_value)
        assert f.to_binary() == b"\x23" + float32_struct.pack(test_value)

    def test_uint_to_binary(self):
        test_value = 64
        f = Uint64(test_value)
        assert f.to_binary() == b"\x3a" + uint64_struct.pack(test_value)
        f = Uint32(test_value)
        assert f.to_binary() == b"\x39" + uint32_struct.pack(test_value)

    def test_string_to_binary(self):
        test_value = "Hello, world!"
        test_value_encoded = b"\x48\x65\x6c\x6c\x6f\x2c\x20\x77\x6f\x72\x6c\x64\x21"
        length_encoded = struct.pack("<H", len(test_value))
        test_value_binary = b"\x11" + length_encoded + test_value_encoded
        s = UonString(test_value)
        assert s.to_binary() == test_value_binary

# ============================== DECODING ==============================


class TestUonDecoding:
    def test_binary_to_bool(self):
        assert decode_binary(b"\x14\x01") == UonBoolean(True)

    def test_binary_to_float(self):
        test_value = b"\x24\x00\x00\x00\x00\x00\x00i@"
        assert decode_binary(test_value) == Float64(200.0)
        test_value = b"\x23\x00\x00HC"
        assert decode_binary(test_value) == Float32(200.0)

    def test_binary_to_uint(self):
        test_value = b"\x3a\xc8\x00\x00\x00\x00\x00\x00\x00"
        assert decode_binary(test_value) == Uint64(200)
        test_value = b"\x39\xc8\x00\x00\x00"
        assert decode_binary(test_value) == Uint32(200)

    def test_binary_to_string(self):
        test_value = b"\x11\r\x00Hello, world!"
        assert decode_binary(test_value) == UonString("Hello, world!")
