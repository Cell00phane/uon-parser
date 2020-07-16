import pprint

from uonrevisedtypes.uon_base import UonBase

from binary.utils import EOL


class UonSeq(UonBase):
    def __init__(self, seq, presentation_properties={}):
        super().__init__(seq, "seq", presentation_properties)

    def __str__(self):
        return pprint.pformat(self.value)

    def __repr__(self):
        return "UonSeq({})".format(pprint.pformat(self.value))

    def to_binary(self):
        encoded_seq = b""
        for v in self.value:
            encoded_seq += v.to_binary()
        return b"\x01" + encoded_seq + EOL
