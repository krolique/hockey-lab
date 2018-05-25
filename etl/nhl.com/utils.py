# -*- coding: utf-8 -*-
"""
    Utils
    -----

    contains common functionality that can't be grouped into a unifying
    theme... yet.

"""

from transliterate import translit, detect_language


def latinize(value):
    """ Replaces UTF-8 characters to their latin equivalents

    :param value: the string to transliterate
    :type value: str
    :returns: transliterated string
    :rtype: str
    """

    # when this library function fails to detect a language
    # there is nothing to transliterate
    if not detect_language(value):
        return value
    # using the reversed param in the function enables the function to
    # substitute UTF-8 to latin
    return translit(value, reversed=True)
