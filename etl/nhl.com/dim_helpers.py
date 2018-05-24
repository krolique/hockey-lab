# -*- coding: utf-8 -*-
"""
    Dim Helpers
    -----------

   Contains shared functionality for dimensional transformation modules

"""

from transliterate import translit, detect_language


def stream_header(name, fields):
    """ Returns dimensional entity stream header message

    :param name: name of the entity being streamed
    :type name: str
    :param fields: a collection of fields available in the entity
    :type fields: list
    :returns: a header describing messages properties in a stream
    :rtype: dict
    """

    return {
        'name': name,
        'fields': fields
    }


def translit_to_latin(value):
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
