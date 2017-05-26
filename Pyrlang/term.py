from __future__ import print_function

import struct

from future.utils import python_2_unicode_compatible
from builtins import chr

from Pyrlang.Dist import util

ATOM_MARKER = "pyrlang.Atom"
PID_MARKER = "pyrlang.Pid"


@python_2_unicode_compatible
class Atom:
    def __repr__(self) -> str:
        return "atom'%s'" % self.text_

    def __str__(self):
        return self.text_

    def __init__(self, text: str) -> None:
        self.text_ = text

    def equals(self, other) -> bool:
        return isinstance(other, Atom) and self.text_ == other.text_

    __eq__ = equals

    def __ne__(self, other):
        return not self.equals(other)

    def __hash__(self):
        return hash((ATOM_MARKER, self.text_))


class List:
    """ Erlang list which stores elements in a Python list, can have a tail
        for improper list representation, and can be interpreted as Python
        string optionally
    """

    def __repr__(self) -> str:
        if self.tail_ == []:
            return str(self.elements_)

        elements = ", ".join(str(e) for e in self.elements_)
        return "[%s | %s]" % (elements, self.tail_)

    def __init__(self) -> None:
        self.elements_ = []
        self.tail_ = []

    def __str__(self) -> str:
        return self.__repr__()

    def append(self, x):
        self.elements_.append(x)

    def set_tail(self, t):
        self.tail_ = t

    def as_unicode(self):
        return "".join([chr(x) for x in self.elements_])


class Pid:
    def __init__(self, node, id, serial, creation) -> None:
        self.node_ = node
        self.id_ = id
        self.serial_ = serial
        self.creation_ = creation

    def __repr__(self) -> str:
        return "Pid<%d.%d.%d>@%s" % (self.creation_, self.id_, self.serial_,
                                     self.node_.text_)

    def __str__(self) -> str:
        return self.__repr__()

    def equals(self, other) -> bool:
        return isinstance(other, Pid) \
               and self.node_ == other.node_ \
               and self.id_ == other.id_ \
               and self.serial_ == other.serial_ \
               and self.creation_ == other.creation_

    __eq__ = equals

    def __ne__(self, other):
        return not self.equals(other)

    def __hash__(self):
        return hash((PID_MARKER, self.node_,
                     self.id_, self.serial_, self.creation_))


class Reference:
    def __init__(self, node, creation, id) -> None:
        self.node_ = node
        self.id_ = id
        self.creation_ = creation

    def __repr__(self) -> str:
        # Assume that ref has only 3 32-bit words (actually id size is not
        # specified in docs and can be a different multiple of 4)
        v = struct.unpack(">III", self.id_)
        return "Ref<%d,%d,%d,%d>@%s" % \
               (self.creation_, v[0], v[1], v[2], self.node_.text_)

    def __str__(self) -> str:
        return self.__repr__()


class Binary:
    """ Represents a bytes object, with last byte optionally incomplete.
        Bit objects have last_byte_bits < 8
    """
    def __init__(self, data: bytes, last_byte_bits: int = 8) -> None:
        self.bytes_ = data
        self.last_byte_bits_ = last_byte_bits

    def __repr__(self) -> str:
        lbb = self.last_byte_bits_
        if lbb == 8:
            return "<<%s>>" % util.dec_bytes(self.bytes_, ",")
        else:
            return "<<%s:%d>>" % (util.dec_bytes(self.bytes_, ","), lbb)

    def __str__(self) -> str:
        return self.__repr__()

    def equals(self, other) -> bool:
        return isinstance(other, Binary) \
               and self.bytes_ == other.bytes_ \
               and self.last_byte_bits_ == other.last_byte_bits_

    __eq__ = equals

    def __ne__(self, other):
        return not self.equals(other)


__all__ = ['Atom', 'Pid', 'Binary', 'Reference']