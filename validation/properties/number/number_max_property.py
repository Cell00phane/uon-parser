import struct

from validation.properties.number.number_property_validation import (
    NumberPropertiesValidation)
from validation.properties.property import ValidationPropertyError


class MaxNumberValidation(NumberPropertiesValidation):
    def __init__(self, maximum):
        self.maximum = maximum

    def validate_property(self, input_):
        if (input_.value > self.maximum):
            raise MaxNumberValidationError(input_,
                                           "The following input {} "
                                           "is bigger than {}"
                                           .format(input_, self.maximum))

    def __repr__(self):
        return "MaxNumberValidation({})".format(self.maximum)

    def __str__(self):
        return f"max: {self.maximum}"

    def to_binary(self):
        """Binary representation of number max property.

        Concatenate the max keyword (\0x8) to \x15 reserved for 
        numeric types.

        Numeric ranges are encoded on a double precision float.
        
        Returns:
            bytes: binary representation of number max property
        """
        return b"\x15\x08" + struct.pack("<d", self.maximum)


class MaxNumberValidationError(ValidationPropertyError):
    def __init__(self, expression, message):
        super().__init__(expression, message)
