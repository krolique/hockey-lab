# -*- coding: utf-8 -*-
"""
    Facts Transformer
    -----------------

    Contains shared functio

"""

from json import dumps, loads
from sys import stdout, stdin

def transfomr(message):
    """ Transforms an api message into a

    :param message: an api response element
    :type message: dict
    :returns: transformed message object
    :rtype: dict
    """

    return {
        'full_name': message.get('name'),
        'short_name': message.get('shortName'),
        'team_name': message.get(''),
        'abbreviation': ,
        'location': '',
        'division': '',
        'conference': '',
        'first_year_of_play': ''
    }


def process_stream(input_stream=None, output_stream=None):
    """ Processes the input stream

    :param input_stream: the stream from which to iterate input from
    :type input_stream: FileObject
    :param output_stream: the stream to which to write to
    :type output_stream: FileObject
    """
    if not input_stream:
        input_stream = stdin

    if not output_stream:
        output_stream = stdout

    for input_str in input_stream:
        message = loads(input_str)
        sanitized = {k: sanitizer(value=v) for k, v in body.iteritems()}
        serialized = dumps(message)
        output_stream.write("{serialized}\n".format(serialized=serialized))


if __name__ == '__main__':
    process_stream()
