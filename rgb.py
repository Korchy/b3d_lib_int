# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/b3d_lib_int

import math
import re
from mathutils import Vector


class RGB:

    __r = None
    __g = None
    __b = None

    __null_relevance = math.sqrt(3)*255   # rgb colors relevance = 0 when compare 2 rgb colors (diagonal of the rgb-cube 255x255x255)

    def __init__(self, r, g, b):
        if isinstance(r, int) and r >= 0 and r <= 255 and isinstance(g, int) and g >= 0 and g <= 255 and isinstance(b, int) and b >= 0 and b <= 255:
            self.__r = r
            self.__g = g
            self.__b = b
        if isinstance(r, float) and r >= 0.0 and r <= 1.0 and isinstance(g, float) and g >= 0.0 and g <= 1.0 and isinstance(b, float) and b >= 0.0 and b <= 1.0:
            self.__r = int(self.__from_linear(r) * 255)
            self.__g = int(self.__from_linear(g) * 255)
            self.__b = int(self.__from_linear(b) * 255)

    def __str__(self):
        return "RGB({},{},{})".format(self.__r, self.__g, self.__b)

    def __repr__(self):
        return "RGB({},{},{})".format(self.__r, self.__g, self.__b)

    @property
    def r(self):
        return self.__r

    @property
    def g(self):
        return self.__g

    @property
    def b(self):
        return self.__b

    @classmethod
    def fromstring(cls, rgb):
        if re.compile('^\d{1,3}-\d{1,3}-\d{1,3}$').match(rgb) is not None:
            # 123-123-123
            rgbarr = rgb.split('-')
            return cls(int(rgbarr[0]), int(rgbarr[1]), int(rgbarr[2]))
        elif re.compile('^\d{1,3}.\d{1,3}.\d{1,3}$').match(rgb) is not None:
            # 123.123.123
            rgbarr = rgb.split('.')
            return cls(int(rgbarr[0]), int(rgbarr[1]), int(rgbarr[2]))
        else:
            return None

    @staticmethod
    def rgb_to_linear(rgb):
        if isinstance(rgb, RGB):
            return list(map(__class__.__to_linear, [rgb.r, rgb.g, rgb.b]))

    def as_linear(self):
        return __class__.rgb_to_linear(self)

    @staticmethod
    def rgb_to_hex(rgb):
        return [hex(rgb.r)[2:].upper(), hex(rgb.g)[2:].upper(), hex(rgb.b)[2:].upper()]

    def as_hex(self):
        return __class__.rgb_to_hex(self)

    @classmethod
    def fromlist(cls, lst):
        # [0-255, 0-255, 0-255] or [0.0-1.0, 0.0-1.0, 0.0-1.0]
        return cls(lst[0], lst[1], lst[2])

    @staticmethod
    def rgb_to_vector(rgb):
        if isinstance(rgb, RGB):
            return Vector((rgb.r, rgb.g, rgb.b))

    def as_vector(self):
        return __class__.rgb_to_vector(self)

    @staticmethod
    def set_null_relevance(new_null_relevance):
        __class__.__null_relevance = new_null_relevance

    @staticmethod
    def relevance(rgb1, rgb2):
        # relevance 0...1 (between rgb1 and rgb2)
        if isinstance(rgb1, RGB) and isinstance(rgb2, RGB):
            relevancelengtn = (__class__.rgb_to_vector(rgb1) - __class__.rgb_to_vector(rgb2)).length
            return 1 - relevancelengtn / __class__.__null_relevance
        else:
            return 0

    @staticmethod
    def __from_linear(value):
        # value = 0...1 in linear scale (.5 = 127) -> return 0...1 in real acale (.5 = 188)
        if value <= 0.0031308:
            return 12.92 * value
        else:
            return 1.055 * value ** (1 / 2.4) - 0.055

    @staticmethod
    def __to_linear(value):
        # value = 0...255 in real scale (.5 = 188) -> return 0...1 in linear scale (.5 = 127)
        value /= 255
        if value <= 0.04045:
            return value / 12.92
        else:
            return ((value + 0.055) / 1.055) ** 2.4
