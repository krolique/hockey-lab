# -*- coding: utf-8 -*-
"""
    Transform Fact Game
    -------------------

    Transforms gamelog fact into fact_game

"""

from json import dumps, loads
from sys import stdout, stdin
from datetime import datetime

from dim_helpers import stream_header


#: fields the entity
ENTITY_FIELDS = ['date', 'hr', 'dec', 'os', 'opp', 'gf', 'ga', 'ppg',
                 'pp opp', 'ppga', 'ts', 'shga', 'sf', 'sa']


#: name of the entity being emitted
ENTITY_NAME = 'fact_game'


def transform(message):
    """ Transforms an api message into a dim team message

    :param message: an api response element
    :type message: dict
    :returns: transformed message object
    :rtype: dict
    """

    date = datetime.strptime(message.get('Date'), "%b %d '%y").isoformat()

    return {
        'date': date,
        'hr': message.get('H/R'),
        'dec': message.get('Dec'),
        'os': message.get('O/S'),
        'opp': message.get('Opp'),
        'gf': int(message.get('GF')),
        'ga': int(message.get('GA')),
        'ppg': int(message.get('PPG')),
        'pp opp': int(message.get('PP Opp')),
        'ppga': int(message.get('PPGA')),
        'ts': int(message.get('TS')),
        'shga': int(message.get('SHGA')),
        'sf': int(message.get('SF')),
        'sa': int(message.get('SA'))
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

    serialized = dumps(stream_header(name=ENTITY_NAME, fields=ENTITY_FIELDS))
    output_stream.write(f'{serialized}\n')
    for input_str in input_stream:
        message = loads(input_str)
        transformed = transform(message=message)
        serialized = dumps(transformed)
        output_stream.write(f'{serialized}\n')


if __name__ == '__main__':
    process_stream()
