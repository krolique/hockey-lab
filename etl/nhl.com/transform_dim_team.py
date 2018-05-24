# -*- coding: utf-8 -*-
"""
    Transform Dim Team
    ------------------

    Transforms team fact into a dim_team

"""

from json import dumps, loads
from sys import stdout, stdin

from dim_helpers import stream_header, translit_to_latin

#: fields the entity
ENTITY_FIELDS = ['full_name', 'short_name', 'abbreviation', 'location',
                 'division', 'conference', 'first_year_of_play', 'team_name']


#: name of the entity being emitted
ENTITY_NAME = 'dim_team'


def transform(message):
    """ Transforms an api message into a dim team message

    :param message: an api response element
    :type message: dict
    :returns: transformed message object
    :rtype: dict
    """

    full_name = translit_to_latin(value=message.get('name'))
    short_name = translit_to_latin(value=message.get('shortName'))
    team_name = translit_to_latin(value=message.get('teamName'))
    location_name = translit_to_latin(value=message.get('locationName'))
    abbreviation = translit_to_latin(value=message.get('abbreviation'))

    first_year = message.get('firstYearOfPlay')
    if first_year is not None:
        first_year = int(first_year)

    return {
        'full_name': full_name,
        'short_name': short_name,
        'team_name': team_name,
        'abbreviation': abbreviation,
        'location': location_name,
        'division': message.get('division').get('name'),
        'conference': message.get('conference').get('name'),
        'first_year_of_play': first_year
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
