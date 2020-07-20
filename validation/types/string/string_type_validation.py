from validation.types.type_validation import (
    ValidationType, ValidationTypeError
)

from uonrevisedtypes.scalars.uon_string import UonString


class StringTypeValidation(ValidationType):

    def validate_type(self, input_):
        if (not isinstance(input_, UonString)):
            raise ValidationTypeError(input_, "The following input {} type "
                                              "does not correspond to string"
                                              .format(input_))

    def __repr__(self):
        return "StringTypeValidation()"

    def __str__(self):
        return "!str"
