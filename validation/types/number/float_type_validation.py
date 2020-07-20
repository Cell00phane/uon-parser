from validation.types.type_validation import (
    ValidationType, ValidationTypeError
)
from uonrevisedtypes.scalars.uon_float import UonFloat


class FloatTypeValidation(ValidationType):

    def validate_type(self, input_):
        if (not isinstance(input_, UonFloat)):
            raise ValidationTypeError(input_, "The following input {} type "
                                              "does not correspond to float"
                                              .format(input_))

    def __repr__(self):
        return "FloatTypeValidation()"

    def __str__(self):
        return "!float"
