class Validator:
    def __init__(self, type_validation, properties_validations):
        self.type_validation = type_validation
        self.properties_validations = properties_validations

    def validate(self, input_):
        self.type_validation.validate_type(input_)
        for property_validation in self.properties_validations:
            property_validation.validate_property(input_)

    def __repr__(self):
        return "Validator({}, {})".format(
            self.type_validation, self.properties_validations)


class ValidationError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
