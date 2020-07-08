from abc import ABC, abstractmethod


class UonBase(ABC):
    """
    Represents the basic UON type.

    We provide a getter and a setter for _presentation_properties (we
    prefix it with an underscore to denote that it's a private variable)
    by the means of the built-in @property decorator. That way 
    we can add custom behavior when getting or setting this attribute, 
    while avoiding to have to write boilerplate code like 
    get_presentation_properties() or set_presentation_properties().

    # TODO: When deserializing verify that the keys of the presentation 
    properties dict correspond to the accepted set of properties
    like description or optional.
    """
    def __init__(self, value, uon_type, presentation_properties={}):
        self.value = value
        self.uon_type = uon_type
        self._presentation_properties = presentation_properties

    @property
    def presentation_properties(self):
        """ Return the presentation properties of this uon object."""
        return self._presentation_properties

    @presentation_properties.setter
    def presentation_properties(self, dict_):
        """ Set the presentation properties of this uon object. """
        self._presentation_properties = dict_

    @abstractmethod
    def to_binary(self):
        pass
