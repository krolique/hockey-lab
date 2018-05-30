# -*- coding: utf-8 -*-
"""
    Dim Helpers
    -----------

   Contains shared functionality for dimensional transformation modules

"""


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
