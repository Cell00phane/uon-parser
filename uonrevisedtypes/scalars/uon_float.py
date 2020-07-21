import numpy as np

from uonrevisedtypes.scalars.uon_numeric import UonNumeric


class UonFloat(UonNumeric):
    """A Uon type to represent floats.
    In reality, the float represented by this class are what
    we refer to as decimal in the uon specification.
    """
    def __init__(self, value, uon_type, precision, presentation_properties={}):
        super().__init__(value, uon_type, precision, presentation_properties)


class Float16(UonFloat):
    """
    https://stackoverflow.com/questions/38975770/python-numpy-float16-datatype-operations-and-float8
    """
    pass


class Float32(UonFloat):
    def __init__(self, value, presentation_properties={}):
        v = np.float32(value)
        super().__init__(v, "float32", 32, presentation_properties)

    def __repr__(self):
        return "Float32(self, {}, {}, {})".format(
            self.value, self.uon_type, self.precision)

    def to_binary(self):
        return b"\x23" + self.value.tobytes()


class Float64(UonFloat):
    def __init__(self, value, presentation_properties={}):
        v = np.float64(value)
        super().__init__(v, "float64", 64, presentation_properties)

    def __repr__(self):
        return "Float64(self, {}, {}, {})".format(
            self.value, self.uon_type, self.precision)

    def to_binary(self):
        return b"\x24" + self.value.tobytes()


class Float128(UonFloat):
    def __init__(self, value, presentation_properties={}):
        v = np.float128(value)
        super().__init__(v, "float128", 128, presentation_properties)

    def __repr__(self):
        return "Float128(self, {}, {}, {})".format(
            self.value, self.uon_type, self.precision)

    def to_binary(self):
        return b"\x25" + self.value.tobytes()


# l = [Float32, Float64, Float128]
# for f in l:
#     print(f.__name__,   f(3.02))
