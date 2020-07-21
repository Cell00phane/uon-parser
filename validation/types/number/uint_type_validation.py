from validation.types.type_validation import (
    ValidationType, ValidationTypeError
)
from uonrevisedtypes.scalars.uon_uint import UonUint


class UintTypeValidation(ValidationType):

    def validate_type(self, input_):
        if (not isinstance(input_, UonUint)):
            raise ValidationTypeError(input_, "The following input {} type "
                                              "does not correspond to "
                                              "unsigned int".format(input_))

    def __repr__(self):
        return "UintTypeValidation()"

    def __str__(self):
        return "!uint"

    def to_binary(self):
        """Binary representation of unsigned integer type validation.

        Concatenate the type validation property's binary (\x19)
        to the uint type (\x30).

        Returns:
            bytes: binary representation of uint type validation
        """
        return b"\x19\x30"