# -*- coding: utf-8 -*-
"""
    Transform Dim Division
    ----------------------

    Transforms team facts into a dim division stream

"""

from json import dumps, loads
from sys import stdout, stdin

from dim_helpers import stream_header

#: fields on the entity
ENTITY_FIELDS = ['name']


#: name of the entity being emitted
ENTITY_NAME = 'dim_division'


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

    serialized = dumps(stream_header(name=ENTITY_NAME, fields=ENTITY_FIELDS))
    output_stream.write(f'{serialized}\n')
    divisions = set()
    for input_str in input_stream:
        message = loads(input_str)
        divisions.add(message.get('division').get('name'))

    for division in divisions:
        serialized = dumps({'name': division})
        output_stream.write(f'{serialized}\n')


if __name__ == '__main__':
    process_stream()
